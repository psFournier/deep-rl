import numpy as np
from ddpg.segmentTree import SumSegmentTree, MinSegmentTree
import random as rnd

# added by Olivier Sigaud --------------------------------
# import pickle
# end of added by Olivier Sigaud --------------------------------

#TODO : same buffer for goals and for expe
class RingBuffer(object):
    def __init__(self, maxlen, shape, dtype='float32'):
        self.maxlen = maxlen
        self.start = 0
        self.length = 0
        self.data = np.zeros((maxlen,) + shape).astype(dtype)

    def __len__(self):
        return self.length

    def __getitem__(self, idx):
        if idx < 0 or idx >= self.length:
            raise KeyError()
        return self.data[(self.start + idx) % self.maxlen]

    def get_batch(self, idxs):
        return self.data[(self.start + idxs) % self.maxlen]

    def append(self, v):
        if self.length < self.maxlen:
            # We have space, simply increase the length.
            self.length += 1
        elif self.length == self.maxlen:
            # No space, "remove" the first item.
            self.start = (self.start + 1) % self.maxlen
        else:
            # This should never happen.
            raise RuntimeError()
        self.data[(self.start + self.length - 1) % self.maxlen] = v

    def dump(self):
        """Get all of the data in a single array"""
        return (self.data[:self.length])


def array_min2d(x):
    x = np.array(x)
    if x.ndim >= 2:
        return x
    return x.reshape(-1, 1)


class ReplayBuffer(object):
    def __init__(self, limit, content_shape):
        self.contents = {}
        self.length = 0
        for content, shape in content_shape.items():
            self.contents[content] = RingBuffer(limit, shape=shape)

    def append(self, buffer_item):
        for name, value in self.contents.items():
            self.length += 1
            value.append(buffer_item[name])

    def dump(self):
        """Get all of the data in a single array"""
        return (self.contents[:self.length])

class Memory(ReplayBuffer):
    def __init__(self, contents_shape, limit):
        super(Memory, self).__init__(limit, contents_shape)

    def end_episode(self, goal_reached):
        pass

    def sample(self, batch_size):
        # Draw such that we always have a proceeding element.
        batch_idxs = np.random.random_integers(self.nb_entries - 2, size=batch_size)
        result = {}
        for name, value in self.contents.items():
            result[name] = array_min2d(value.get_batch(batch_idxs))
        return batch_idxs, result

    @property
    def nb_entries(self):
        return len(self.contents['state0'])


class SARSTMemory(Memory):
    def __init__(self, env, limit):
        state_dim = env.observation_space.high.shape[0]+len(env.state_to_goal)
        action_dim = env.action_space.high.shape[0]
        self.contents_shape = {'state0': (state_dim,),
                        'action': (action_dim,),
                        'state1': (state_dim,),
                        'reward': (1,),
                         'terminal': (1,)}

        super(SARSTMemory, self).__init__(self.contents_shape, limit)

    def build_exp(self, state, action, next_state, reward, terminal):
        dict = {'state0': state,
         'action': action,
         'state1': next_state,
         'reward': reward,
         'terminal': terminal}
        return dict

class EpisodicHerSARSTMemory(SARSTMemory):
    def __init__(self, env, limit, strategy):
        """Replay buffer that does Hindsight Experience Replay
        obs_to_goal is a function that converts observations to goals
        goal_slice is a slice of indices of goal in observation
        """
        super(EpisodicHerSARSTMemory, self).__init__(env, limit)

        self.strategy = strategy
        self.data = []
        self.env = env
        self.state_to_goal = env.state_to_goal
        self.state_to_obs = env.state_to_obs
        self.obs_to_goal = env.obs_to_goal

    def append(self, buffer_item):
        super(EpisodicHerSARSTMemory, self).append(buffer_item)
        self.data.append(buffer_item)

    def change_goal(self, buffer_item, new_goal):
        res = buffer_item
        res['state0'][self.state_to_goal] = new_goal
        res['state1'][self.state_to_goal] = new_goal
        res['reward'], res['terminal'] = self.env.eval_exp(res['state0'],
                                                                   res['action'],
                                                                   res['state1'])
        return res

    def end_episode(self, goal_reached):
        if self.strategy == 'final' and (not goal_reached):
            final_state = self.data[-1]['state1']
            new_goal = final_state[self.state_to_obs][self.obs_to_goal]
            for buffer_item in self.data:
                new_buffer_item = self.change_goal(buffer_item, new_goal)
                super(EpisodicHerSARSTMemory, self).append(new_buffer_item)
        elif self.strategy == 'episode':
            indices = range(0, len(self.data))
            random_indices = rnd.sample(indices, np.min([4, len(indices)]))
            final_states = [self.data[i]['state1'] for i in list(random_indices)]
            for final_state in final_states:
                new_goal = final_state[self.state_to_obs][self.obs_to_goal]
                for buffer_item in self.data:
                    new_buffer_item = self.change_goal(buffer_item, new_goal)
                    super(EpisodicHerSARSTMemory, self).append(new_buffer_item)
        elif self.strategy == 'future':
            for idx, buffer_item in enumerate(self.data):
                indices = range(idx, len(self.data))
                future_indices = rnd.sample(indices, np.min([4, len(indices)]))
                final_states = [self.data[i]['state1'] for i in list(future_indices)]
                for final_state in final_states:
                    new_goal = final_state[self.state_to_obs][self.obs_to_goal]
                    new_buffer_item = self.change_goal(buffer_item, new_goal)
                    super(EpisodicHerSARSTMemory, self).append(new_buffer_item)
        else:
            print('error her strategy')
            return
        self.data = []







