import tensorflow as tf
import numpy as np
from gym.envs.registration import make
import argparse
import pprint as pp
from ddpg.logger import Logger
from ddpg.memory import SARSTMemory, EpisodicHerSARSTMemory
from ddpg.regionTree2 import TreeMemory
import datetime
from ddpg.networks import ActorNetwork, HuberLossCriticNetwork
from ddpg.ddpgAgent import DDPG_agent
from ddpg.noise import OrnsteinUhlenbeckActionNoise
from gym.spaces import Box
from ddpg.util import load, boolean_flag
from gym.wrappers import Monitor

def main(args):
    """Despite following the directives of https://keras.io/getting-started/faq/#how-can-i-obtain-reproducible-results-using-keras-during-development, fully reproducible results could not be obtained. See here : https://github.com/keras-team/keras/issues/2280 for any improvements"""

    # Storing logger output in files with names corresponding to parameters used
    params = args['env'] + '_' + \
             args['memory'] + '_' + \
             args['strategy'] + '_' + \
             args['sampler'] + '_' + \
             args['alpha'] + '_' + \
             args['delta'] + '_' + \
             args['activation'] + '_' + \
             args['invert_grads'] + '_' + \
             args['target_clip'] + '_' + \
             args['sigma']
    now = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

    # Two loggers are defined to retrieve information by step or by episode. Only episodic information is displayed to stdout.
    log_dir = args['log_dir']+params+'/'+now
    logger_step = Logger(dir=log_dir+'/log_steps', format_strs=['stdout', 'json'])
    logger_episode = Logger(dir=log_dir+'/log_episodes', format_strs=['stdout', 'json'])

    # os.environ['PYTHONHASHSEED'] = '0'
    # if args['random_seed'] is not None:
    #     np.random.seed(int(args['random_seed']))
    #     rn.seed(int(args['random_seed']))
    #     tf.set_random_seed(int(args['random_seed']))

    # Make calls EnvRegistry.make, which builds the environment from its specs defined in gym.envs.init end then builds a timeLimit wrapper around the environment to set the max amount of steps to run
    train_env = make(args['env'])
    test_env = make(args['env'])
    # test_env = Monitor(test_env, directory=save_dir)

    # Wraps each environment in a goal_wrapper to override basic env methods and be able to access goal space properties, or modify the environment simulation according to sampled goals. The wrapper classes paths corresponding to each environment are defined in gym.envs.int
    if train_env.spec._goal_wrapper_entry_point is not None:
        wrapper_cls = load(train_env.spec._goal_wrapper_entry_point)
        train_env = wrapper_cls(train_env)
        test_env = wrapper_cls(test_env)

    #TODO integrate the choice of memory in environments specs in gym.env.init
    if args['memory'] == 'sarst':
        memory = SARSTMemory(train_env, limit=int(1e6))
    elif args['memory'] == 'hsarst':
        memory = EpisodicHerSARSTMemory(train_env, limit=int(1e6), strategy=args['strategy'])
    else:
        raise Exception('No existing memory defined')

    low = np.concatenate([train_env.observation_space.low, train_env.goal_space.low])
    high = np.concatenate([train_env.observation_space.high, train_env.goal_space.high])
    state_space = Box(low, high)

    memory = TreeMemory(state_space, train_env.state_to_goal, memory, max_regions=64, n_split=10, split_min=0, lambd = 1, maxlen = 300, n_cp = 30)
    # memory.init_grid_1D(64)

    # Noise for the actor in vanilla ddpg
    actor_noise = OrnsteinUhlenbeckActionNoise(mu=np.zeros(train_env.action_dim), sigma=float(args['sigma']))

    with tf.Session() as sess:

        if args['random_seed'] is not None:
            np.random.seed(int(args['random_seed']))
            tf.set_random_seed(int(args['random_seed']))
            train_env.seed(int(args['random_seed']))
            test_env.seed(int(args['random_seed']))

        actor = ActorNetwork(sess,
                             train_env.state_dim,
                             train_env.action_dim,
                             float(args['tau']),
                             float(args['actor_lr']),
                             args['activation'])

        critic = HuberLossCriticNetwork(sess,
                                        train_env.state_dim,
                                        train_env.action_dim,
                                        float(args['delta']),
                                        float(args['gamma']),
                                        float(args['tau']),
                                        float(args['critic_lr']))

        agent = DDPG_agent(sess,
                           actor,
                           actor_noise,
                           critic,
                           train_env,
                           test_env,
                           memory,
                           args['sampler'],
                           logger_step,
                           logger_episode,
                           int(args['minibatch_size']),
                           int(args['nb_test_steps']),
                           int(args['max_steps']),
                           log_dir,
                           int(args['save_freq']),
                           int(args['eval_freq']),
                           args['target_clip']=='True',
                           args['invert_grads']=='True',
                           float(args['alpha']),
                           args['render_test'],
                           int(args['train_freq']),
                           int(args['nb_train_iter']),
                           args['resume_step'],
                           args['resume_timestamp'])
        agent.run()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='provide arguments for DDPG agent')

    # agent parameters
    parser.add_argument('--actor-lr', help='actor network learning rate', default=0.0001)
    parser.add_argument('--critic-lr', help='critic network learning rate', default=0.001)
    parser.add_argument('--gamma', help='discount factor for critic updates', default=0.99)
    parser.add_argument('--tau', help='soft target update parameter', default=0.001)
    parser.add_argument('--buffer-size', help='max size of the replay buffer', default=1000000)
    parser.add_argument('--minibatch-size', help='size of minibatch for minibatch-SGD', default=64)

    parser.add_argument('--memory', help='type of memory to use', default='sarst')
    parser.add_argument('--strategy', help='hindsight strategy: final, episode or future', default='final')
    parser.add_argument('--sampler', help='type of goal_wrappers sampling', default='no')
    parser.add_argument('--alpha', help="how much priorization in goal_wrappers sampling", default=0.5)
    parser.add_argument('--sigma', help="amount of exploration", default=0.3)
    parser.add_argument('--delta', help='delta in huber loss', default='inf')
    parser.add_argument('--activation', help='actor final layer activation', default='tanh')
    parser.add_argument('--invert-grads', help='Gradient inverting for bounded action spaces', default=False)
    parser.add_argument('--target-clip', help='Reproduce target clipping from her paper', default=False)


    # run parameters
    parser.add_argument('--env', help='choose the gym env', default='MountainCarContinuous-v0')
    parser.add_argument('--random-seed', help='random seed for repeatability', default=None)
    parser.add_argument('--max-steps', help='max num of episodes to do while training', default=200000)
    parser.add_argument('--log-dir', help='directory for storing run info',
                        default='/home/pierre/PycharmProjects/deep-rl/log/local/')
    parser.add_argument('--resume-timestamp', help='directory to retrieve weights of actor and critic',
                        default=None)
    parser.add_argument('--resume-step', help='resume_step',
                        default=None)
    parser.add_argument('--train-freq', help='training frequency', default=100)
    parser.add_argument('--nb-train-iter', help='training iteration number', default=50)
    parser.add_argument('--nb-test-steps', help='number of steps in the environment during evaluation', default=1000)
    boolean_flag(parser, 'render-test', default=False)
    parser.add_argument('--save-freq', help='saving models weights frequency', default=10000)
    parser.add_argument('--eval-freq', help='evaluating every n training steps', default=200)

    args = vars(parser.parse_args())
    
    pp.pprint(args)

    main(args)
