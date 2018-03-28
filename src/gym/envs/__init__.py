from gym.envs.registration import registry, register, make, spec

# Algorithmic
# ----------------------------------------

register(
    id='Copy-v0',
    entry_point='gym.envs.algorithmic:CopyEnv',
    max_episode_steps=200,
    reward_threshold=25.0,
)

register(
    id='RepeatCopy-v0',
    entry_point='gym.envs.algorithmic:RepeatCopyEnv',
    max_episode_steps=200,
    reward_threshold=75.0,
)

register(
    id='ReversedAddition-v0',
    entry_point='gym.envs.algorithmic:ReversedAdditionEnv',
    kwargs={'rows' : 2},
    max_episode_steps=200,
    reward_threshold=25.0,
)

register(
    id='ReversedAddition3-v0',
    entry_point='gym.envs.algorithmic:ReversedAdditionEnv',
    kwargs={'rows' : 3},
    max_episode_steps=200,
    reward_threshold=25.0,
)

register(
    id='DuplicatedInput-v0',
    entry_point='gym.envs.algorithmic:DuplicatedInputEnv',
    max_episode_steps=200,
    reward_threshold=9.0,
)

register(
    id='Reverse-v0',
    entry_point='gym.envs.algorithmic:ReverseEnv',
    max_episode_steps=200,
    reward_threshold=25.0,
)

# Classic
# ----------------------------------------

register(
    id='CartPole-v0',
    entry_point='gym.envs.classic_control:CartPoleEnv',
    max_episode_steps=200,
    reward_threshold=195.0,
)

register(
    id='CartPole-v1',
    entry_point='gym.envs.classic_control:CartPoleEnv',
    max_episode_steps=500,
    reward_threshold=475.0,
)

register(
    id='MountainCar-v0',
    entry_point='gym.envs.classic_control:MountainCarEnv',
    max_episode_steps=200,
    reward_threshold=-110.0,
)

register(
    id='CMC-v0',
    entry_point='gym.envs.classic_control:Continuous_MountainCarEnv',
    goal_wrapper_entry_point='ddpg.goal_wrappers.cmc:CmcNoGoal',
    max_episode_steps=999,
)

register(
    id='CMCPos-v0',
    entry_point='gym.envs.classic_control:Continuous_MountainCarEnv',
    goal_wrapper_entry_point='ddpg.goal_wrappers.cmc:CmcPos',
    max_episode_steps=999,
)

register(
    id='CMCFull-v0',
    entry_point='gym.envs.classic_control:Continuous_MountainCarEnv',
    goal_wrapper_entry_point='ddpg.goal_wrappers.cmc:CmcFull',
    max_episode_steps=999,
)

register(
    id='Pendulum-v0',
    entry_point='gym.envs.classic_control:PendulumEnv',
    max_episode_steps=200,
)

register(
    id='Acrobot-v1',
    entry_point='gym.envs.classic_control:AcrobotEnv',
    max_episode_steps=500,
)

# Gridworlds
# ----------------------------------------
register(
    id='Gridworld-v0',
    entry_point='gym.envs.gridworlds:gridEnv',
    goal_wrapper_entry_point='ddpg.goal_wrappers.wrapper:no_goal',
    max_episode_steps=50,
)

# Robotics
# ----------------------------------------

def _merge(a, b):
    a.update(b)
    return a

for reward_type in ['sparse', 'dense']:
    suffix = 'Dense' if reward_type == 'dense' else ''
    kwargs = {
        'reward_type': reward_type,
    }

    # Fetch
    register(
        id='FetchSlide{}-v0'.format(suffix),
        entry_point='gym.envs.robotics:FetchSlideEnv',
        kwargs=kwargs,
        max_episode_steps=50,
    )

    register(
        id='FetchPickAndPlace{}-v0'.format(suffix),
        entry_point='gym.envs.robotics:FetchPickAndPlaceEnv',
        kwargs=kwargs,
        max_episode_steps=50,
    )

    register(
        id='FetchReach{}-v0'.format(suffix),
        entry_point='gym.envs.robotics:FetchReachEnv',
        kwargs=kwargs,
        max_episode_steps=50,
    )

    register(
        id='FetchPush{}-v0'.format(suffix),
        entry_point='gym.envs.robotics:FetchPushEnv',
        kwargs=kwargs,
        max_episode_steps=50,
    )

    # Hand
    register(
        id='HandReach{}-v0'.format(suffix),
        entry_point='gym.envs.robotics:HandReachEnv',
        kwargs=kwargs,
        max_episode_steps=50,
    )

    register(
        id='HandManipulateBlockRotateZ{}-v0'.format(suffix),
        entry_point='gym.envs.robotics:HandBlockEnv',
        kwargs=_merge({'target_position': 'ignore', 'target_rotation': 'z'}, kwargs),
        max_episode_steps=100,
    )

    register(
        id='HandManipulateBlockRotateParallel{}-v0'.format(suffix),
        entry_point='gym.envs.robotics:HandBlockEnv',
        kwargs=_merge({'target_position': 'ignore', 'target_rotation': 'parallel'}, kwargs),
        max_episode_steps=100,
    )

    register(
        id='HandManipulateBlockRotateXYZ{}-v0'.format(suffix),
        entry_point='gym.envs.robotics:HandBlockEnv',
        kwargs=_merge({'target_position': 'ignore', 'target_rotation': 'xyz'}, kwargs),
        max_episode_steps=100,
    )

    register(
        id='HandManipulateBlockFull{}-v0'.format(suffix),
        entry_point='gym.envs.robotics:HandBlockEnv',
        kwargs=_merge({'target_position': 'random', 'target_rotation': 'xyz'}, kwargs),
        max_episode_steps=100,
    )

    # Alias for "Full"
    register(
        id='HandManipulateBlock{}-v0'.format(suffix),
        entry_point='gym.envs.robotics:HandBlockEnv',
        kwargs=_merge({'target_position': 'random', 'target_rotation': 'xyz'}, kwargs),
        max_episode_steps=100,
    )

    register(
        id='HandManipulateEggRotate{}-v0'.format(suffix),
        entry_point='gym.envs.robotics:HandEggEnv',
        kwargs=_merge({'target_position': 'ignore', 'target_rotation': 'xyz'}, kwargs),
        max_episode_steps=100,
    )

    register(
        id='HandManipulateEggFull{}-v0'.format(suffix),
        entry_point='gym.envs.robotics:HandEggEnv',
        kwargs=_merge({'target_position': 'random', 'target_rotation': 'xyz'}, kwargs),
        max_episode_steps=100,
    )

    # Alias for "Full"
    register(
        id='HandManipulateEgg{}-v0'.format(suffix),
        entry_point='gym.envs.robotics:HandEggEnv',
        kwargs=_merge({'target_position': 'random', 'target_rotation': 'xyz'}, kwargs),
        max_episode_steps=100,
    )

    register(
        id='HandManipulatePenRotate{}-v0'.format(suffix),
        entry_point='gym.envs.robotics:HandPenEnv',
        kwargs=_merge({'target_position': 'ignore', 'target_rotation': 'xyz'}, kwargs),
        max_episode_steps=100,
    )

    register(
        id='HandManipulatePenFull{}-v0'.format(suffix),
        entry_point='gym.envs.robotics:HandPenEnv',
        kwargs=_merge({'target_position': 'random', 'target_rotation': 'xyz'}, kwargs),
        max_episode_steps=100,
    )

    # Alias for "Full"
    register(
        id='HandManipulatePen{}-v0'.format(suffix),
        entry_point='gym.envs.robotics:HandPenEnv',
        kwargs=_merge({'target_position': 'random', 'target_rotation': 'xyz'}, kwargs),
        max_episode_steps=100,
    )


# Box2d
# ----------------------------------------

register(
    id='LunarLander-v2',
    entry_point='gym.envs.box2d:LunarLander',
    max_episode_steps=1000,
    reward_threshold=200,
)

register(
    id='LunarLanderContinuous-v2',
    entry_point='gym.envs.box2d:LunarLanderContinuous',
    max_episode_steps=1000,
    reward_threshold=200,
)

register(
    id='BipedalWalker-v2',
    entry_point='gym.envs.box2d:BipedalWalker',
    max_episode_steps=1600,
    reward_threshold=300,
)

register(
    id='BipedalWalkerHardcore-v2',
    entry_point='gym.envs.box2d:BipedalWalkerHardcore',
    max_episode_steps=2000,
    reward_threshold=300,
)

register(
    id='CarRacing-v0',
    entry_point='gym.envs.box2d:CarRacing',
    max_episode_steps=1000,
    reward_threshold=900,
)

# Toy Text
# ----------------------------------------

register(
    id='Blackjack-v0',
    entry_point='gym.envs.toy_text:BlackjackEnv',
)

register(
    id='KellyCoinflip-v0',
    entry_point='gym.envs.toy_text:KellyCoinflipEnv',
    reward_threshold=246.61,
)
register(
    id='KellyCoinflipGeneralized-v0',
    entry_point='gym.envs.toy_text:KellyCoinflipGeneralizedEnv',
)

register(
    id='FrozenLake-v0',
    entry_point='gym.envs.toy_text:FrozenLakeEnv',
    kwargs={'map_name' : '4x4'},
    max_episode_steps=100,
    reward_threshold=0.78, # optimum = .8196
)

register(
    id='FrozenLake8x8-v0',
    entry_point='gym.envs.toy_text:FrozenLakeEnv',
    kwargs={'map_name' : '8x8'},
    max_episode_steps=200,
    reward_threshold=0.99, # optimum = 1
)

register(
    id='CliffWalking-v0',
    entry_point='gym.envs.toy_text:CliffWalkingEnv',
)

register(
    id='NChain-v0',
    entry_point='gym.envs.toy_text:NChainEnv',
    max_episode_steps=1000,
)

register(
    id='Roulette-v0',
    entry_point='gym.envs.toy_text:RouletteEnv',
    max_episode_steps=100,
)

register(
    id='Taxi-v2',
    entry_point='gym.envs.toy_text.taxi:TaxiEnv',
    reward_threshold=8, # optimum = 8.46
    max_episode_steps=200,
)

register(
    id='GuessingGame-v0',
    entry_point='gym.envs.toy_text.guessing_game:GuessingGame',
    max_episode_steps=200,
)

register(
    id='HotterColder-v0',
    entry_point='gym.envs.toy_text.hotter_colder:HotterColder',
    max_episode_steps=200,
)

# Mujoco
# ----------------------------------------

# 2D

register(
    id='Reacher-v0',
    entry_point='gym.envs.mujoco:ReacherEnv',
    goal_wrapper_entry_point='ddpg.goal_wrappers.reacher:ReacherNoGoal',
    max_episode_steps=1000,
)

register(
    id='ReacherGoal-v0',
    entry_point='gym.envs.mujoco:ReacherEnv',
    goal_wrapper_entry_point='ddpg.goal_wrappers.reacher:Reacher',
    max_episode_steps=1000,
)

register(
    id='Pusher-v0',
    entry_point='gym.envs.mujoco:PusherEnv',
    max_episode_steps=100,
    reward_threshold=0.0,
)

register(
    id='Thrower-v0',
    entry_point='gym.envs.mujoco:ThrowerEnv',
    max_episode_steps=100,
    reward_threshold=0.0,
)

register(
    id='Striker-v0',
    entry_point='gym.envs.mujoco:StrikerEnv',
    max_episode_steps=100,
    reward_threshold=0.0,
)

register(
    id='InvertedPendulum-v1',
    entry_point='gym.envs.mujoco:InvertedPendulumEnv',
    max_episode_steps=1000,
    reward_threshold=950.0,
)

register(
    id='InvertedDoublePendulum-v1',
    entry_point='gym.envs.mujoco:InvertedDoublePendulumEnv',
    max_episode_steps=1000,
    reward_threshold=9100.0,
)

register(
    id='HalfCheetah-v0',
    entry_point='gym.envs.mujoco:HalfCheetahEnv',
    goal_wrapper_entry_point='ddpg.goal_wrappers.hc:HalfCheetahNoGoal',
    max_episode_steps=1000,
)

register(
    id='HalfCheetahGoal-v0',
    entry_point='gym.envs.mujoco:HalfCheetahEnv',
    goal_wrapper_entry_point='ddpg.goal_wrappers.hc:HalfCheetahX',
    max_episode_steps=1000,
)

register(
    id='Hopper-v1',
    entry_point='gym.envs.mujoco:HopperEnv',
    max_episode_steps=1000,
    reward_threshold=3800.0,
)

register(
    id='Swimmer-v1',
    entry_point='gym.envs.mujoco:SwimmerEnv',
    max_episode_steps=1000,
    reward_threshold=360.0,
)

register(
    id='Walker2d-v1',
    max_episode_steps=1000,
    entry_point='gym.envs.mujoco:Walker2dEnv',
)

register(
    id='Ant-v1',
    entry_point='gym.envs.mujoco:AntEnv',
    max_episode_steps=1000,
    reward_threshold=6000.0,
)

register(
    id='Humanoid-v1',
    entry_point='gym.envs.mujoco:HumanoidEnv',
    max_episode_steps=1000,
)

register(
    id='HumanoidStandup-v1',
    entry_point='gym.envs.mujoco:HumanoidStandupEnv',
    max_episode_steps=1000,
)

register(
    id='Manipulator-v0',
    entry_point='gym.envs.mujoco:ManipulatorEnv',
    goal_wrapper_entry_point='ddpg.goal_wrappers.manipulator:BaseNoGoal',
    max_episode_steps=1000,
)

register(
    id='ManipulatorGoal-v0',
    entry_point='gym.envs.mujoco:ManipulatorEnv',
    goal_wrapper_entry_point='ddpg.goal_wrappers.manipulator:Base',
    max_episode_steps=1000,
)

register(
    id='ManipulatorBall-v0',
    entry_point='gym.envs.mujoco:ManipulatorBallEnv',
    goal_wrapper_entry_point='ddpg.goal_wrappers.manipulator:BallNoGoal',
    max_episode_steps=1000,
)

register(
    id='ManipulatorBallGoal-v0',
    entry_point='gym.envs.mujoco:ManipulatorBallEnv',
    goal_wrapper_entry_point='ddpg.goal_wrappers.manipulator:Ball',
    max_episode_steps=1000,
)

register(
    id='ManipulatorBallCup-v0',
    entry_point='gym.envs.mujoco:ManipulatorBallCupEnv',
    goal_wrapper_entry_point='ddpg.goal_wrappers.manipulator:BallCupNoGoal',
    max_episode_steps=1000,
)

register(
    id='ManipulatorBallCupGoal-v0',
    entry_point='gym.envs.mujoco:ManipulatorBallCupEnv',
    goal_wrapper_entry_point='ddpg.goal_wrappers.manipulator:BallCup',
    max_episode_steps=1000,
)

register(
    id='ManipulatorPeg-v0',
    entry_point='gym.envs.mujoco:ManipulatorPegEnv',
    goal_wrapper_entry_point='ddpg.goal_wrappers.manipulator:PegNoGoal',
    max_episode_steps=1000,
)

register(
    id='ManipulatorPegGoal-v0',
    entry_point='gym.envs.mujoco:ManipulatorPegEnv',
    goal_wrapper_entry_point='ddpg.goal_wrappers.manipulator:Peg',
    max_episode_steps=1000,
)

register(
    id='ManipulatorPegSlot-v0',
    entry_point='gym.envs.mujoco:ManipulatorPegSlotEnv',
    goal_wrapper_entry_point='ddpg.goal_wrappers.manipulator:PegSlotNoGoal',
    max_episode_steps=1000,
)

register(
    id='ManipulatorPegSlotGoal-v0',
    entry_point='gym.envs.mujoco:ManipulatorPegSlotEnv',
    goal_wrapper_entry_point='ddpg.goal_wrappers.manipulator:PegSlot',
    max_episode_steps=1000,
)

register(
    id='ManipulatorBoxes-v0',
    entry_point='gym.envs.mujoco:ManipulatorBoxesEnv',
    goal_wrapper_entry_point='ddpg.goal_wrappers.manipulator:BoxesNoGoal',
    max_episode_steps=1000,
)

register(
    id='ManipulatorBoxesGoal-v0',
    entry_point='gym.envs.mujoco:ManipulatorBoxesEnv',
    goal_wrapper_entry_point='ddpg.goal_wrappers.manipulator:Boxes',
    max_episode_steps=1000,
)

register(
    id='Playroom-v0',
    entry_point='gym.envs.mujoco:PlayroomEnv',
    goal_wrapper_entry_point='ddpg.goal_wrappers.manipulator:PlayroomNoGoal',
    max_episode_steps=1000,
)

register(
    id='PlayroomGoal-v0',
    entry_point='gym.envs.mujoco:PlayroomEnv',
    goal_wrapper_entry_point='ddpg.goal_wrappers.manipulator:Playroom',
    max_episode_steps=1000,
)


# Atari
# ----------------------------------------

# # print ', '.join(["'{}'".format(name.split('.')[0]) for name in atari_py.list_games()])
for game in ['air_raid', 'alien', 'amidar', 'assault', 'asterix', 'asteroids', 'atlantis',
    'bank_heist', 'battle_zone', 'beam_rider', 'berzerk', 'bowling', 'boxing', 'breakout', 'carnival',
    'centipede', 'chopper_command', 'crazy_climber', 'demon_attack', 'double_dunk',
    'elevator_action', 'enduro', 'fishing_derby', 'freeway', 'frostbite', 'gopher', 'gravitar',
    'hero', 'ice_hockey', 'jamesbond', 'journey_escape', 'kangaroo', 'krull', 'kung_fu_master',
    'montezuma_revenge', 'ms_pacman', 'name_this_game', 'phoenix', 'pitfall', 'pong', 'pooyan',
    'private_eye', 'qbert', 'riverraid', 'road_runner', 'robotank', 'seaquest', 'skiing',
    'solaris', 'space_invaders', 'star_gunner', 'tennis', 'time_pilot', 'tutankham', 'up_n_down',
    'venture', 'video_pinball', 'wizard_of_wor', 'yars_revenge', 'zaxxon']:
    for obs_type in ['image', 'ram']:
        # space_invaders should yield SpaceInvaders-v0 and SpaceInvaders-ram-v0
        name = ''.join([g.capitalize() for g in game.split('_')])
        if obs_type == 'ram':
            name = '{}-ram'.format(name)

        nondeterministic = False
        if game == 'elevator_action' and obs_type == 'ram':
            # ElevatorAction-ram-v0 seems to yield slightly
            # non-deterministic observations about 10% of the time. We
            # should track this down eventually, but for now we just
            # mark it as nondeterministic.
            nondeterministic = True

        register(
            id='{}-v0'.format(name),
            entry_point='gym.envs.atari:AtariEnv',
            kwargs={'game': game, 'obs_type': obs_type, 'repeat_action_probability': 0.25},
            max_episode_steps=10000,
            nondeterministic=nondeterministic,
        )

        register(
            id='{}-v4'.format(name),
            entry_point='gym.envs.atari:AtariEnv',
            kwargs={'game': game, 'obs_type': obs_type},
            max_episode_steps=100000,
            nondeterministic=nondeterministic,
        )

        # Standard Deterministic (as in the original DeepMind paper)
        if game == 'space_invaders':
            frameskip = 3
        else:
            frameskip = 4

        # Use a deterministic frame skip.
        register(
            id='{}Deterministic-v0'.format(name),
            entry_point='gym.envs.atari:AtariEnv',
            kwargs={'game': game, 'obs_type': obs_type, 'frameskip': frameskip, 'repeat_action_probability': 0.25},
            max_episode_steps=100000,
            nondeterministic=nondeterministic,
        )

        register(
            id='{}Deterministic-v4'.format(name),
            entry_point='gym.envs.atari:AtariEnv',
            kwargs={'game': game, 'obs_type': obs_type, 'frameskip': frameskip},
            max_episode_steps=100000,
            nondeterministic=nondeterministic,
        )

        register(
            id='{}NoFrameskip-v0'.format(name),
            entry_point='gym.envs.atari:AtariEnv',
            kwargs={'game': game, 'obs_type': obs_type, 'frameskip': 1, 'repeat_action_probability': 0.25}, # A frameskip of 1 means we get every frame
            max_episode_steps=frameskip * 100000,
            nondeterministic=nondeterministic,
        )

        # No frameskip. (Atari has no entropy source, so these are
        # deterministic environments.)
        register(
            id='{}NoFrameskip-v4'.format(name),
            entry_point='gym.envs.atari:AtariEnv',
            kwargs={'game': game, 'obs_type': obs_type, 'frameskip': 1}, # A frameskip of 1 means we get every frame
            max_episode_steps=frameskip * 100000,
            nondeterministic=nondeterministic,
        )

# Board games
# ----------------------------------------

register(
    id='Go9x9-v0',
    entry_point='gym.envs.board_game:GoEnv',
    kwargs={
        'player_color': 'black',
        'opponent': 'pachi:uct:_2400',
        'observation_type': 'image3c',
        'illegal_move_mode': 'lose',
        'board_size': 9,
    },
    # The pachi player seems not to be determistic given a fixed seed.
    # (Reproduce by running 'import gym; h = gym.make('Go9x9-v0'); h.seed(1); h.reset(); h.step(15); h.step(16); h.step(17)' a few times.)
    #
    # This is probably due to a computation time limit.
    nondeterministic=True,
)

register(
    id='Go19x19-v0',
    entry_point='gym.envs.board_game:GoEnv',
    kwargs={
        'player_color': 'black',
        'opponent': 'pachi:uct:_2400',
        'observation_type': 'image3c',
        'illegal_move_mode': 'lose',
        'board_size': 19,
    },
    nondeterministic=True,
)

register(
    id='Hex9x9-v0',
    entry_point='gym.envs.board_game:HexEnv',
    kwargs={
        'player_color': 'black',
        'opponent': 'random',
        'observation_type': 'numpy3c',
        'illegal_move_mode': 'lose',
        'board_size': 9,
    },
)

# Debugging
# ----------------------------------------

register(
    id='OneRoundDeterministicReward-v0',
    entry_point='gym.envs.debugging:OneRoundDeterministicRewardEnv',
    local_only=True
)

register(
    id='TwoRoundDeterministicReward-v0',
    entry_point='gym.envs.debugging:TwoRoundDeterministicRewardEnv',
    local_only=True
)

register(
    id='OneRoundNondeterministicReward-v0',
    entry_point='gym.envs.debugging:OneRoundNondeterministicRewardEnv',
    local_only=True
)

register(
    id='TwoRoundNondeterministicReward-v0',
    entry_point='gym.envs.debugging:TwoRoundNondeterministicRewardEnv',
    local_only=True,
)

# Parameter tuning
# ----------------------------------------
register(
    id='ConvergenceControl-v0',
    entry_point='gym.envs.parameter_tuning:ConvergenceControl',
)

register(
    id='CNNClassifierTraining-v0',
    entry_point='gym.envs.parameter_tuning:CNNClassifierTraining',
)

# Safety
# ----------------------------------------

# interpretability envs
register(
    id='PredictActionsCartpole-v0',
    entry_point='gym.envs.safety:PredictActionsCartpoleEnv',
    max_episode_steps=200,
)

register(
    id='PredictObsCartpole-v0',
    entry_point='gym.envs.safety:PredictObsCartpoleEnv',
    max_episode_steps=200,
)

# semi_supervised envs
    # probably the easiest:
register(
    id='SemisuperPendulumNoise-v0',
    entry_point='gym.envs.safety:SemisuperPendulumNoiseEnv',
    max_episode_steps=200,
)
    # somewhat harder because of higher variance:
register(
    id='SemisuperPendulumRandom-v0',
    entry_point='gym.envs.safety:SemisuperPendulumRandomEnv',
    max_episode_steps=200,
)
    # probably the hardest because you only get a constant number of rewards in total:
register(
    id='SemisuperPendulumDecay-v0',
    entry_point='gym.envs.safety:SemisuperPendulumDecayEnv',
    max_episode_steps=200,
)

# off_switch envs
register(
    id='OffSwitchCartpole-v0',
    entry_point='gym.envs.safety:OffSwitchCartpoleEnv',
    max_episode_steps=200,
)

register(
    id='OffSwitchCartpoleProb-v0',
    entry_point='gym.envs.safety:OffSwitchCartpoleProbEnv',
    max_episode_steps=200,
)
