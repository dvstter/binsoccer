# BinSoccer

## Intro

Based on Littman 's paper 'Markov games as a framework for multi-agent reinforcement learning'.

Simple binary game.

## Usage

1. Download this folder
2. User command `pip install -e gym-binsoccer` to install
3. Try `env = gym.make('gym_soccer:binsoccer-v0')`

## Notice

1. After make the environment, you should use `env.init(height, width)` to initial the environment
2. Then you can use `env.reset()` get the initial state which is one tuple including `(p1_h, p1_w, p2_h, p2_w, ball)`
3. `ball == 0` means player1 holds the ball
4. Use `env.step([0,1])` to pass action for player1 and player2
5. Actions included `0,1,2,3,4` represent $north$ $south$ $west$ $south$ and $stop$