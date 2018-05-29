import numpy as np
import tensorflow as tf

from RL_brain import PolicyGradient
from routing_env.py import Net

def run_net():
    step=0
    for episode in range(3000):
        observation=env.reset()

        while True:
            action = RL.choose_action(observation)

            observation_, reward, done=env.step(action)

            RL.store_transition(observation,action,reward)

            if(step>200) and (step%5==0):
                RL.learn()

            observation=observation_

            if done:
                break
            step +=1

if __name__="__main__":
    env=Net()
    RL=...#
    


