# -*- coding: utf-8 -*-
"""
Created on Sat Nov  6 20:24:58 2021

@author: eng-Moshira
"""

import numpy as np

# [name, cpu cycle for 1 bit, min data, maximum data]
# applications = [id, cpu cycle, data size, delay tolerance]
#     [0, 10435, 80000, 800000, 5],  # speech recognition
#     [1, 25346, 300, 1400, 0.5],  # natural language processing
#     [2, 45043, 300000, 30000000, 300],  # face recognition
#     [3, 34252, 300, 4000, 0.1],  # language translation
#     [4, 54633, 100000, 3000000, 50],  # 3d game processing
#     [5, 40305, 100000, 3000000, 40],  # virtual reality
#     [6, 34532, 100000, 3000000, 40],  # augmented reality
# ]


services = [
    [0, 10435, 4400000.0, .008],  # speech recognition
    [1, 25346, 85000.0, .0015],  # natural language processing, newly added
    [2, 45043, 151500000, .5],  # face recognition
    [3, 34252, 21500.0, .001],  # language translation
    [4, 54633, 15500000.0, .1],  # 3d game processing
    [5, 40305, 15500000.0, .08],  # virtual reality
    [6, 34532, 15500000.0, .07],  # augmented reality
    # [7, 100, 15500000.0, 20], # fabricated task, newly added
    [8, 4000, 440000000, .01],  # speech recognition
    [9, 6000, 550000000, .05],  # natural language processing, newly added
    [10, 2000, 1200000000, .1],  # face recognition
]

applications = [
    [0, 400, 440.0, .01],  # speech recognition
    [1, 600, 550.0, .05],  # natural language processing, newly added
    [2, 200, 1200, .1],  # face recognition
   
    
]


def get_random_task():
    choice = np.random.choice(len(applications))
    application = applications[choice]
    data_size = application[2]
    cpu_cycle = data_size * application[1]
    task=Task(application[0],data_size,cpu_cycle,application[3])
    # task = {
    #     "data": data_size,
    #     "cpu_cycle": cpu_cycle,
    #     "dt": application[3]
    # }
    return task


def make_task_from_applications(application):
    data_size = application[2]
    cpu_cycle = data_size * application[1]
    task=Task(data_size,cpu_cycle,application[3])
    # task = {
    #     "data": data_size,
    #     "cpu_cycle": cpu_cycle,
    #     "dt": application[3]
    # }
    return task


# def create_task():
#     data_size_range = [300000, 500000]  # min and max amount of data in bit
#     cpu_cycle_1bit = 10435  # cpu cycle required for 1 bit of data
#     delay_tolerance = 3  # s
#     data_size_choice = [300000, 350000, 400000, 450000, 500000]
#
#     data_size = np.random.choice(data_size_choice)
#     # data_size = np.random.randint(data_size_range[0], data_size_range[1])
#
#     task = {
#         "data": data_size,
#         "cpu_cycle": cpu_cycle_1bit * data_size,
#         "delay_tolerance": delay_tolerance
#     }
#     return task


def get_fixed_task():
    task=Task(4096000,3000e6,8)
    # size = 300000
    # task = {
    #     "data": 4096000,
    #     "cpu_cycle": 3000e6,
    #     "dt": 8
    # }
    return task

class Task():
    def __init__(self, sid,dz,cyc,dt):
        self.datasize=dz
        self.cpucycles=cyc
        self.dalaytolerance=dt
        self.serviceid=sid

if __name__ == '__main__':
    # task = create_task()
    # print(task["cpu_cycle"] / 3.6)
    tasklist=[get_random_task() for i in range(10)]
    for i in range(10):
     print(tasklist[i].datasize)
    # for i in range(20):
    #     print(get_random_task().datasize)