import gym
from gym import spaces
import numpy as np
import random as rn

ACTIONS_INDEX = ['n', 's', 'w', 'e', 'stop']
ACTIONS_UNICODE = ['\u2191', '\u2193', '\u2190', '\u2192', '\u25B2']
ACTIONS = {'n': (-1, 0), 's': (1, 0), 'w': (0, -1), 'e': (0, 1), 'stop': (0, 0)}


class BinSoccerEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super(BinSoccerEnv, self).__init__()
        self.inited = False

    def init(self, h, w):
        self.shape = (h, w)
        self.action_space = spaces.Box(low=np.array([0, 0]), high=np.array([4, 4]), shape=(2,), dtype=np.int)
        self.observation_space = spaces.Box(low=np.array([0, 0, 0, 0, 0]),
                                            high=np.array([h - 1, w - 1, h - 1, w - 1, 1]), shape=(5,), dtype=np.int)
        self.reward_range = (-1, 1)
        self.start_points = [(int(h / 2), 0), (int(h / 2), w - 1)]

    def reset(self):
        self.ground = np.zeros(self.shape)
        self.players = [x for x in self.start_points]
        for idx, p in enumerate(self.players, 1):
            self.ground[p] = idx
        self.ball = 0 if rn.random() < 0.5 else 1
        self.inited = True
        return self.__get_observation()

    '''
        @params: list actions, like [0, 1]
    '''

    def step(self, actions):
        if not self.inited:
            raise RuntimeError('This game should be inited or has finished!')
        coord1, coord2 = self.players  # current coordinates or two players
        act1, act2 = [ACTIONS_INDEX[a] for a in actions]  # change action number into action name
        new_coord1 = self.__new_coord(coord1, act1)
        new_coord2 = self.__new_coord(coord2, act2)

        # randomly choose who act first
        if rn.random() < 0.5:
            # player1 act firstly
            self.__move(0, new_coord1)
            self.__move(1, new_coord2)

        else:
            # player2 act firstly
            self.__move(1, new_coord2)
            self.__move(0, new_coord1)

        coord1, coord2 = self.players  # get updated players' positions
        obs = self.__get_observation()
        reward, done = self.__get_game_state(coord1, coord2)

        return obs, reward, done, {}

    def render(self, mode='human', close=False):
        temp = [[str(int(x)) for x in line] for line in self.ground.copy().tolist()]
        if self.ball == 0:
            temp[self.players[0][0]][self.players[0][1]] = '\u2460'
        else:
            temp[self.players[1][0]][self.players[1][1]] = '\u2461'

        print('-' * (self.shape[1] * 2 + 1))
        for i in range(self.shape[0]):
            print('|' + '|'.join(temp[i]) + '|')
            print('-' * (self.shape[1] * 2 + 1))

    def close(self):
        self.inited = False

    # test coordinates overpass, if not return the new coordinates
    def __new_coord(self, coord, action):
        next_coord = np.array(coord) + np.array(ACTIONS[action])
        if next_coord[0] not in range(self.shape[0]) or next_coord[1] not in range(self.shape[1]):
            return coord
        else:
            return tuple(next_coord)

    def __move(self, player, new_coord):
        coord = self.players.pop(player)
        another_coord = self.players[0]

        if player == self.ball:
            # current player own the ball
            if new_coord == another_coord:
                self.ball = 0 if player == 1 else 1
                new_coord = coord
            else:
                self.ground[coord] = 0
                self.ground[new_coord] = player + 1
        else:
            if new_coord != another_coord:
                self.ground[coord] = 0
                self.ground[new_coord] = player + 1

        self.players = [another_coord, another_coord]
        self.players[player] = new_coord

    def __get_observation(self):
        return tuple(list(self.players[0]) + list(self.players[1]) + [self.ball])

    def __get_game_state(self, coord1, coord2):
        if coord1 == (2, 0) and self.ball == 0:
            done = True
            reward = 1  # we want to train player1, so the player1's goal will be rewarded
            self.inited = False
        elif coord2 == (1, 4) and self.ball == 1:
            done = True
            reward = -1
            self.inited = False
        else:
            done = False
            reward = 0

        return reward, done