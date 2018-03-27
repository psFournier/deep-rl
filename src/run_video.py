from keras.models import load_model
import os
from gym.envs.registration import make
from gym.monitoring import VideoRecorder
import numpy as np
from ddpg.util import load

log_dir = '../log/cluster/ReacherGoal-v0_sigma_0.3/ReacherGoal-v0_sarst_final_1_10_0.0001_500_0.3_1_1/20180326194845_495483/'
model = load_model(os.path.join(log_dir, 'saves', 'actor_model.h5'))
test_env = make('ReacherGoal-v0')

if test_env.spec._goal_wrapper_entry_point is not None:
    wrapper_cls = load(test_env.spec._goal_wrapper_entry_point)
    test_env = wrapper_cls(test_env)


vid_dir = os.path.join(log_dir, 'videos')
os.makedirs(vid_dir, exist_ok=True)
base_path = os.path.join(vid_dir, 'video_init')
rec = VideoRecorder(test_env, base_path=base_path)
test_env.rec = rec

test_env.set_goal_init()

print(test_env.goal)

state = test_env.reset()
reward_sum = 0
for k in range(1000):
    test_env.render(mode='human')
    action = model.predict(np.reshape(state, (1, test_env.state_dim[0])))
    action = np.clip(action, test_env.action_space.low, test_env.action_space.high)
    state, reward, terminal, info = test_env.step(action[0])
    reward_sum += reward
    print('reward: ', reward_sum)
    terminal = terminal or info['past_limit']
    if terminal:
        break
