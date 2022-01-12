# -*- coding: utf-8 -*-
"""
Created on Sun Nov 28 01:59:19 2021

@author: eng-Moshira
"""

import numpy as np
from systemparameters import parameter
import math

numofUsers=15
numOfUAV = 3  # UAV no.
class UAV():
    
    def __init__(self):
       
        self.height = np.random.randint(75,100) #uav height
        self.Pu = 0.05 * np.random.randint(1, 10, size=numOfUAV)       # Transmission power of each UAV
        self.loc_ue_list = np.random.randint(0, 301, size=[numofUsers, 2])  # Location information: x is random at 0-100
        #sum_task_size = 100 * 1048576  # Total computing task 60 MBits --> 60 80 100 120 140
        #loc_uav = [50, 50]
        self.uav_loc=np.random.randint(50,100,size=[numOfUAV,2])
        #uav_velocity=np.random.randint(5,15,size=numOfUAV)
       # bandwidth_nums = 1
        self.UBW = 30 * 10 ** 6  # Bandwidth 10MHz
        self.p_noisy_los = 10 ** (-13)  # Noise power -100dBm
        self.p_noisy_nlos = 10 ** (-11)  # Noise power -80dBm
        self.flight_speed = 50.  # Flight speed 50m/s
        # f_ue = 6e8 # UE calculation frequency 0.6GHz
        #f_ue = 2e8  # UE calculation frequency 0.6GHz
        #f_uav = 1.2e9  # UAV calculation frequency 1.2GHz
        self.f_uav=np.random.randint(2800, 3200)*10**6
        #self.f_uav=np.random.randint(1, 5)*10**9   # CPU frequency of each UAV
        #r = 10 ** (-27)  # The impact factor of chip structure on cpu processing
        #s = 1000  # The number of cpu cycles required for unit bit processing is 1000
        self.p_uplink = 0.1  # Uplink transmission power 0.1W
        self.alpha0 = 1e-5  # Reference channel gain when the distance is 1m -30dB = 0.001, -50dB = 1e-5
        self.uplink_rate=self.UBW * math.log2(1 + (parameter["user_tr_power"] * self.alpha0) / self.p_noisy_los)
        self.r = 10 ** (-27) # The impact factor of chip structure on cpu processing
        self.v_ue = 1  # ue moving speed 1m/s
       
        self.delta_t =1 + 7 # 1s flight, the last 7s are used for hover calculation
        self.m_uav = 9.65*10**3  # uav mass/kg
        self.maxv=15 # uav max velocity m/s
        self.movedist=np.random.randint(10,20) #moving distance
        self.flypower=100 #flight power/W
        self.staypower=50 #stay power/w
        self.e_battery_uav = 500000  # uav battery power: 500kJ. ref: Mobile Edge Computing via a UAV-Mounted Cloudlet: Optimization of Bit Allocation and Path Planning

    
      # Calculate the communication delay taking on consideration uav height and ue location 
    def uav_com_delay(self,v_id, loc_ue,dis_fly, theta, task_size,task_cycles):
        #dis_fly= dist* self.flight_speed * 1 
        dx_uav = dis_fly * math.cos(theta)
        dy_uav = dis_fly * math.sin(theta)
        loc_uav_after_fly = [self.uav_loc[v_id][0] + dx_uav, self.uav_loc[v_id][1] + dy_uav]
     
        dx = loc_uav_after_fly[0]-loc_ue[0]
        dy = loc_uav_after_fly[1]-loc_ue[1]
        dh = self.height
        dist_uav_ue = np.sqrt(dx * dx + dy * dy + dh * dh)
        p_noise = self.p_noisy_los
       
        g_uav_ue = abs(self.alpha0 / dist_uav_ue ** 2) # channel gain
        trans_rate = self.UBW * math.log2(1 + parameter["user_tr_power"] * g_uav_ue / p_noise) # Uplink transmission rate bps
        t_trans = task_size / trans_rate # upload delay, 1B=8bit
        t_comp = task_cycles / (self.f_uav ) # Calculate the delay on the UAV edge server
        #t_local_com = (1-offloading_ratio) * task_size / (self.f_ue / self.s) # Local calculation delay
        if t_trans <0 or t_comp <0 :
            raise Exception(print("+++++++++++++++++!! error !!++++++++++++++++++++++ +"))
        return t_trans , t_comp 

    def cal_transmit_time(self, data):
         
         uav_tr_time = data / self.uplink_rate
         return uav_tr_time
    
    def cal_transmit_energy(self, v_id, loc_ue, dis_fly, theta, task_size, task_cycles):
         #tr_time = self.cal_transmit_time(data)
         [tr_time, comp_t]=self.uav_com_delay(v_id,loc_ue, dis_fly, theta, task_size, task_cycles)
         tr_energy = parameter["user_tr_power"] * tr_time  #+ parameter["tail_energy"]
         # tr_energy = self.tr_power * self.cal_transmit_time(data)
         return tr_energy
    
    def cal_processing_time(self, cpu_cycle):
         proc_time = (cpu_cycle / self.f_uav)   #+parameter["LAN_latency"]*10**-3
         # proc_time = proc_time  # in s
         return proc_time
    
    def cal_processing_energy(self, cpu_cycle,dis_fly):
        #fly_energy=self.flypower*(self.movedist/self.flight_speed) 
        #stay_energy = (self.cal_processing_time(cpu_cycle))*self.staypower
        #uav_proc_energy=fly_energy+stay_energy
        
        e_uavfly = (dis_fly / (self.delta_t * 0.5)) ** 2 * self.m_uav * (
                self.delta_t * 0.5) * 0.5  # ref: Mobile Edge Computing via a UAV-Mounted Cloudlet: Optimization of Bit Allocation and Path Planning
        e_uavcomp=self.r * cpu_cycle*self.f_uav ** 2  # Calculate energy consumption on UAV edge server
        uav_proc_energy=e_uavfly+e_uavcomp
        user_proc_energy= (self.cal_processing_time(cpu_cycle))*parameter["user_idle_power"]
        return uav_proc_energy,user_proc_energy