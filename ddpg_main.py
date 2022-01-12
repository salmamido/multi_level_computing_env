# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 17:52:26 2021

@author: eng-Moshira
"""
test_interval = 400
from ddpg_torch import Agent
#from network import Agent
import gym
import numpy as np
import torch as T
from utils import plotLearning
from multi_tier_env import multi_tier_env
import matplotlib.pyplot as plt
# import sys
# import trace

def plot_rate(rate_his, title, rolling_intv=400):
    
    import pandas as pd
    import matplotlib as mpl

    rate_array = np.asarray(rate_his)
    df = pd.DataFrame(rate_his)

    mpl.style.use('seaborn')
    #    rolling_intv = 20
    if title == 'train':
        plt.figure(dpi=150)
        plt.plot(np.arange(len(rate_array)) + 1, df.rolling(rolling_intv, min_periods=1).mean(), 'b')
        plt.fill_between(np.arange(len(rate_array)) + 1, df.rolling(rolling_intv, min_periods=1).min()[0],
                         df.rolling(rolling_intv, min_periods=1).max()[0], color='c', alpha=0.2)
        plt.title('Performance after training', loc='center', fontsize=15)
        plt.ylabel('Normalized Computation Rate')
        plt.xlabel('Time Frames')
        plt.show()
        plt.savefig('Normalized computation rate(training).jpeg')
    if title == 'test':
        plt.figure(dpi=150)
        plt.plot((np.arange(len(rate_array)) + 1) * test_interval, df.rolling(rolling_intv, min_periods=1).mean(), 'xkcd:orange')
        plt.fill_between((np.arange(len(rate_array)) + 1) * test_interval, df.rolling(rolling_intv, min_periods=1).min()[0],
                         df.rolling(rolling_intv, min_periods=1).max()[0], color='xkcd:peach', alpha=0.2)
        #plt.xticks(np.arange(1, n + 1, step=test_interval))
        plt.title('Performance at different time frame', loc='center', fontsize=15)
        plt.ylabel('Normalized Computation Rate')
        plt.xlabel('Time Frames')
        plt.show()
        plt.savefig('Normalized computation rate(testing).jpeg')





# create a Trace object, telling it what to ignore, and whether to
# do tracing or line-counting or both.
# tracer = trace.Trace(
#     ignoredirs=[sys.prefix, sys.exec_prefix],
#     trace=0,
#     count=1)

# run the new command using the given tracer
numofepsoides=1000
numoftasks=50
env = multi_tier_env()
#env = gym.make('LunarLanderContinuous-v2')
s_dim=env.state_dim
a_dim=env.action_dim

#agent = Agent(alpha=0.000025, beta=0.00025, input_dims=[8], tau=0.001, env=env,
           #   batch_size=64,  layer1_size=400, layer2_size=300, n_actions=2)
#agent=Agent(alpha=0.0004, beta=0.004, input_dims=s_dim,
                           # tau=0.01, env=env, batch_size=64, layer1_size=500,
                           # layer2_size=300, n_actions=a_dim)
agent = Agent(alpha=0.0004, beta=0.004, input_dims=[s_dim], tau=0.01, env=env,
             n_actions=a_dim,gamma=0.99)
#agent.load_models()
np.random.seed(0)
score_record = []
score_record_step = []
count_record = []
count_record_step = []
time_record = []
time_record_step = []
energy_record = []
energy_record_step = []
uavtasks=[]
mectasks=[]
cloudtasks=[]
uavtasks_step=[]
mectasks_step=[]
cloudtasks_step=[]
x=[]

for i in range(numofepsoides):
    obs = env.reset()
    #print(obs.dtype) # This should not be 'object'
    # b = T.from_numpy(obs)
    # print(b)
    done = False
    score = 0
    while not done:
        act = agent.choose_action(obs)
        #tracer.run('env.step(act)')
        # make a report, placing output in the current directory
       # r = tracer.results()
       # r.write_results(show_missing=True, coverdir=".")
        new_state, reward, done, info = env.step(act)
        agent.remember(obs, act, reward, new_state, int(done))
        agent.learn()
        score += reward
        obs = new_state
        #env.render()
    score_record.append(score)
    #print('episode ', i, 'score %.2f' % score,
        #  'trailing 100 games avg %.3f' % np.mean(score_history[-100:]))
    right_record=1 - env.count_wrong / numoftasks
    print('episode ', i, 'score %.2f' % score, 'right_record %.2f' % right_record, "    wrong: ", env.count_wrong)
    count_record.append(right_record)
    time_record.append(env.exe_delay)
    energy_record.append(env.proc_energy)
    uavtasks.append(info[2])
    mectasks.append(info[3])
    cloudtasks.append(info[4])
    if i % 50 == 0 and i != 0:
        agent.save_models()
        score_record_step.append(np.mean(score_record))
        count_record_step.append(np.mean(count_record))
        time_record_step.append(np.mean(time_record))
        energy_record_step.append(np.mean(energy_record))
        uavtasks_step.append(np.mean(info[2]))
        mectasks_step.append(np.mean(info[3]))
        cloudtasks_step.append(np.mean(info[4]))
        x.append(i)

# filename = 'LunarLander-alpha000025-beta00025-400-300.png'
# plotLearning(score_record, filename, window=100)
# reward
plt.figure()
x_data = np.arange(len(score_record))
plt.plot(x_data, score_record)

plt.figure()
x_data = np.arange(len(score_record_step))
plt.plot(x_data, score_record_step)

# 卸载成功率
plt.figure()
x_data = np.arange(len(count_record))
plt.plot(x_data, count_record)

plt.figure()
x_data = np.arange(len(count_record_step))
plt.plot(x_data, count_record_step)

# 每回合时延
plt.figure()
x_data = np.arange(len(time_record))
plt.plot(x_data, time_record)

plt.figure()
x_data = np.arange(len(time_record_step))
plt.plot(x_data, time_record_step)
plt.show()

# 每回合时延
plt.figure()
x_data = np.arange(len(energy_record))
plt.plot(x_data, energy_record)

plt.figure()
x_data = np.arange(len(energy_record_step))
plt.plot(x_data, energy_record_step)
plt.show()

X1 = np.arange(len(uavtasks_step))
ax = plt.subplot(111)
w = 0.3
ax.bar(X1-w, uavtasks_step, width=w, color='b', align='center')
ax.bar(X1, mectasks_step, width=w, color='g', align='center')
ax.bar(X1+w, cloudtasks_step, width=w, color='r', align='center')

ax.autoscale(tight=True)

plt.show()

plot_rate(score_record_step, 'train')
plot_rate(count_record_step, 'train')
plot_rate(time_record_step, 'train')
plot_rate(energy_record_step, 'train')