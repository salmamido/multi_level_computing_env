# -*- coding: utf-8 -*-
"""
Created on Sat Nov 27 02:41:18 2021

@author: eng-Moshira
"""

import numpy as np
from systemparameters import parameter

class MEC():
    def __init__(self):
        self.MECno=3;
        self.mec_tr_power = 0.5 * np.random.randint(10, 20)       # Transmission power of each MEC
        #self.Fmax =  np.random.randint(5, 10)*10**9   # CPU frequency of each MEC
        self.Fmax=np.random.randint(2800, 3200)*10**6
        #self.Fm = self.Fm * 1e9
        self.M_cap=np.random.randint(1, 4)          # Mission capacity of each MEC
       # self.uplink=7e6
        #self.downlink=10e6
        #self.utilization=np.random.randint(.2,.8)
        #self.execution_cap = self.Fmax * (1 - self.utilization)
        self.channelgain=1e-3 # Reference channel gain when the distance is 1m -30dB = 0.001, -50dB = 1e-5(li2020)
        self.noiseloss=10** (-13)  # Noise power -100dBm=.1pW(chen2021)
        self.MBWu=75e6 # Mec uplink bandwidth(chen2021)
        self.uplink_rate=self.MBWu * np.log2(1 + (parameter["user_tr_power"] * self.channelgain) / self.noiseloss)
        
        
    
    def cal_transmit_time(self, data):
        
        mec_tr_time = data / self.uplink_rate
        return mec_tr_time

    def cal_transmit_energy(self, data):
        tr_time = self.cal_transmit_time(data)
        tr_energy = parameter["user_tr_power"] * tr_time    #+ parameter["tail_energy"]
        # tr_energy = self.tr_power * self.cal_transmit_time(data)
        return tr_energy

    def cal_processing_time(self, cpu_cycle):
        proc_time = (cpu_cycle / self.Fmax)+parameter["LAN_latency"]*10**-3
        # proc_time = proc_time  # in s
        return proc_time

    def cal_processing_energy(self, cpu_cycle):
        proc_energy = (self.cal_processing_time(cpu_cycle))*parameter["user_idle_power"]
        # proc_time = proc_time  # in s
        return proc_energy
    
    #def cal_price(self, proc_time):
     #   expense = proc_time * parameter['edge_cps'] + parameter['edge_request']
      #  return expense

    # def cal_total_cost(self, data, cpu_cycle):
    #     """
    #     if utilization is less than 50%, process here, otherwise offload to cloud by 2.5x.
    #     if utilization = 0.6, 0.6-0.5 = 0.1*2.5 = 25% chance to offload in cloud
    #     for 10.67% = 0.51, 20.87 = 0.4, 29.78=0.33, 40.26 = 0.26, 50 = 0.19
    #     """
    #     edge_tr_time = self.cal_transmit_time(data)
    #     energy = self.cal_transmit_energy(data)

    #     process_here = self.server_utilization - 0.4
    #     # process_here = 1

    #     if random.uniform(0, 1) >= 2.5 * process_here:
    #         proc_time = self.cal_processing_time(cpu_cycle)
    #         money = self.cal_price(proc_time)
    #         time = edge_tr_time + proc_time
    #         total = self.w1 * time + self.w2 * energy + self.w3 * money
    #         # return total, time, energy, money, 0
    #         return total, edge_tr_time, proc_time, energy, money, 0
    #     else:
    #         cloud = Cloud(self.uplink_rate)
    #         cloud_tr_time = cloud.cal_transmit_from_edge(data)
    #         proc_time = cloud.cal_processing_time(cpu_cycle)
    #         money = cloud.cal_price(proc_time)
    #         time = edge_tr_time + cloud_tr_time + proc_time
    #         total = self.w1 * time + self.w2 * energy + money * self.w3
    #         # self.off_from_edge += 1
    #         # return total, time, energy, money, 1
    #         return total, edge_tr_time + cloud_tr_time, proc_time, energy, money, 1

    # def cal_total_cost_naive(self, data, cpu_cycle):
    #     edge_tr_time = self.cal_transmit_time(data)
    #     energy = self.cal_transmit_energy(data)
    #     proc_time = self.cal_processing_time(cpu_cycle)
    #     money = self.cal_price(proc_time)
    #     time = edge_tr_time + proc_time
    #     total = self.w1 * time + self.w2 * energy + money * self.w3
    #     # total = time + money + energy
    #     return total, time, energy, money