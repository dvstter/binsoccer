from gym.envs.registration import register

register(
    id='binsoccer-v0',
    entry_point='gym_binsoccer.envs:BinSoccerEnv',
        )

