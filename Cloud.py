# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 11:49:51 2021

@author: eng-Moshira
"""

from systemparameters import parameter
import numpy as np


np.random.seed(1)


class Cloud:
    def __init__(self):
       # self.tr_power = parameter['tr_power']
        self.Pc=30
        self.tail_latency_energy = parameter['tail_energy']
        self.tail_duration = parameter["tail_duration"]
        #self.uplink_rate = uplink_rate
        self.execution_cap = parameter['cloud_com_cap'] * parameter["cloud_cap"]
        # self.w1 = parameter['w1']
        # self.w2 = parameter['w2']
        # self.w3 = parameter['w3']
      
        self.Fmax = 10*10**9   # CPU frequency of each MEC
         #self.Fm = self.Fm * 1e9
        #self.C_cap=np.random.randint(5, 10)          # Mission capacity of each MEC
        # self.uplink=7e6
         #self.downlink=10e6
         #self.utilization=np.random.randint(.2,.8)
         #self.execution_cap = self.Fmax * (1 - self.utilization)
        self.channelgain=1e-5 # Reference channel gain when the distance is 1m -30dB = 0.001, -50dB = 1e-5(li2020)
        self.noiseloss=10** (-13)  # Noise power -100dBm=.1pW(chen2021)
        self.CBWu=150e6 # Mec uplink bandwidth(chen2021)
        self.uplink_rate=self.CBWu * np.log2(1 + (parameter["user_tr_power"] * self.channelgain) / self.noiseloss)
         
    def cal_propagation_delay(self):
        # delay = self.distance / self.propagation_speed
        # delay = 0.25 # amazon us-east-1 average latency for a day. 250ms,
        # using normal distribution, mean = 250ms, std=448ms
        while True:
            # delay = np.random.randint(300, 500)
            delay = np.random.normal(250, 250)
            if delay < 100:
                continue
            else:
                delay = delay / 1000.0
                break
        return delay

    def cal_transmit_time(self, data):
        tr_time = data / self.uplink_rate
        # tr_time += tr_time  # from mobile to edge and then edge to cloud. so, transmit time is twice.
        tr_time += self.cal_propagation_delay()
        tr_time += 0.1  # 100ms added for miscellanious time
        return tr_time

    # def cal_transmit_from_edge(self, data):
    #     tr_time = data / self.uplink_rate
    #     tr_time += self.cal_propagation_delay()
    #     tr_time += 0.2  # 100ms added for miscellanious time
    #     return tr_time

    def cal_transmit_energy(self, data):
        tr_time = self.cal_transmit_time(data)
        tr_energy = parameter["user_tr_power"] * tr_time + self.tail_latency_energy * 1.75
        
        return tr_energy

    def cal_processing_time(self, cpu_cycle):
        proc_time = (cpu_cycle / self.Fmax)+parameter["WAN_latency"]*10**-3
        return proc_time
    
    def cal_processing_energy(self, cpu_cycle):
        proc_energy = self.cal_processing_time(cpu_cycle)*parameter["user_idle_power"]
        # proc_time = proc_time  # in s
        return proc_energy

    # def cal_price(self, proc_time):
    #     expense = proc_time * parameter['cloud_cps'] + parameter['cloud_request']
    #     return expense

    # def cal_total_cost(self, data, cpu_cycle):
    #     tr_time = self.cal_transmit_time(data)
    #     proc_time = self.cal_processing_time(cpu_cycle)
    #     energy = self.cal_transmit_energy(data)
    #     money = self.cal_price(proc_time)
    #     time = tr_time + proc_time
    #     total = self.w1 * time + self.w2 * energy + self.w3 * money
    #     #return total, time, energy, money
    #     return total, tr_time, proc_time, energy, money

    # def cal_total_cost_naive(self, data, cpu_cycle):
    #     tr_time = self.cal_transmit_time(data)
    #     proc_time = self.cal_processing_time(cpu_cycle)
    #     energy = self.cal_transmit_energy(data)
    #     money = self.cal_price(proc_time)
    #     time = tr_time + proc_time
    #     total = self.w1 * time + self.w2 * energy + money * self.w3
    #     return total, time, energy, money

