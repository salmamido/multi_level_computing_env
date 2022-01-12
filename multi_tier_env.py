# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 17:52:26 2021

@author: eng-Moshira
"""
import offtask
import math
import numpy as np
#import csv
from collections import deque
from Cloud import Cloud
from MEC import MEC
#from generate_states import read_state_from_file, get_initial_state, get_next_state
from UAV import UAV
from systemparameters import parameter
sconst=np.random.randint(1,5)*10**-3
## Variables
numOfUAV = 3    # Number of drones
numofMEC=3      # Number of MECs
numofUsers=10   # Number of users
numoftasks=50    # Number of Tasks
omega=.5
# mu = 5
# sigma = 0.15 * mu
#B = sigma * np.random.randn(numOfUAV) + mu              # Available bandwidth of each drone
                                         
#T_max = np.random.randint(2, 10, size=numOfTask)        # The maximum execution time allowed for each task
no_epsoides=15000 # epsoides no(uav-assisted) ,we may try 140000
s = 1000  # The number of cpu cycles required for unit bit processing is 1000
uv=UAV()      

class multi_tier_env():
    #U = 3  # UAV no.
    def __init__(self):
        self.ground_length = ground_width = 300  # The length and width of the site are both 300m,      
        self.UAV_hieght=100       # self.battery = Energy()
        self.exe_delay = 0
        self.trans_delay = 0
        self.proc_energy = 0
        self.trans_energy = 0
        self.tot_off_cost = 0
        self.total_cost = 0
        self.count_wrong=0
        self.waiting=deque()
        self.new_queue = 0
        self.info=[self.exe_delay , self.proc_energy]
        self.done=False
        self.is_off=[0]*(numoftasks)
        self.progress=[0]*(numoftasks)
        self.T=400                                # total Period 400s
        self.slot_num = int(self.T / 8)  # 40 intervals
        self.alloc_resource = [0] * (numoftasks)  # 分配的资源
        self.numofresources=numOfUAV+numofMEC+1
        self.rest_resource = [0] * self.numofresources
        #self.offtasks=self.gen_Task_List()
        self.offtasks=self.get_task_info()
        self.high=[1,1,1,1,1]
        self.low=[-1,-1,-1,-1,-1]
        self.uavs_locs=uv.uav_loc
        #################### UEs ####################
        # self.block_flag_list = np.random.randint(0, 2,numofUsers)  # 4 ue, ue occlusion situation
        self.loc_ue_list = np.random.randint(0, 301, size=[numofUsers, 2])  # Location information: x is random at 0-100
        # #self.task_list = np.random.randint(1572864, 2097153, M) # Random calculation task 1.5~2Mbits -> Corresponding total task size 60
        # #self.task_list = np.random.randint(2097153, 2621440, M)  # Random calculation task 2~2.5Mbits -> 80
        # self.Task_list=self.get_task_info(numoftasks) #generate rondom task list

        self.action_bound = [-1, 1]  # corresponds to tahn activation function
        self.action_dim=5 # 1st digit represent ue id of the task;the next two digit represent the offloading layer selected;the last two digits represent the selected server id
        #action_dim = 4  # The first digit represents the ue id of the service; the middle two digits represent the flight angle and distance; the last digit represents the current unloading rate serving the UE
        #self.state_dim = 7 + numoftasks * numofUsers  # uav battery remain, uav loc, remaining sum task size, all ue loc, all ue task data, all ue block_flag,uav remaining capacity,mec remaining capacity
        self.state_dim = numoftasks*2+self.numofresources  #+2*numofUsers+2*numOfUAV
        #################### MECs,UAVs,Cloud ####################
        self.mecs_info = [MEC() for i in range(numofMEC)]
        self.uavs_info = [UAV() for i in range(numOfUAV)]
        self.cloud_info = Cloud()
        self.user_inf=[User() for i in range(numofUsers)]
        
        
                     # uav loc, all mec data, all ue loc, all ue task size, all ue block_flag
        #self.task_data=self.get_tasks_data(numoftasks, numofUsers)
        #print(task_data)
        

    def get_tasks_data(self,numoftasks,numofUsers):
        tasks_data=np.zeros((numofUsers,numoftasks))
        #tasks_data=np.arange(numofUsers*numoftasks).reshape(numofUsers,numoftasks)
        for i in range(numofUsers):
            
            for k in range(numoftasks):
             tasks_data[i][k]=self.offtasks[i][k][3]
             
        return tasks_data
    
    def get_task_info(self):
        task = {}
        #total_tasks=numoftasks*numofUsers
        #task_info_len=3 #cpucycles,datasize,delaytolerance
        #tasklist=np.zeros((numofUsers,numoftasks,task_info_len))
        dz= 10*1e6 * np.ones(numoftasks) + np.random.uniform(-1, 1, size=numoftasks) * 1e6
        cn = 8*1e9 * np.ones(numoftasks) + np.random.uniform(-1,1, size=numoftasks) * 1e9
        dl=np.random.randint(10,100,size=numoftasks)*1e-3      #tasklist=np.arange(total_tasks*task_info_len).reshape(numofUsers,numoftasks,task_info_len)
        for i in range(numoftasks):
            us_id=np.random.choice(range(0,numofUsers-1))
            # choice = np.random.choice(len(offtask.applications))
            # services = offtask.applications[choice]
            # data_size = services[2]*8
            # cpu_cycle = data_size * services[1]
            # d_const=services[3]
            
            # choice = np.random.choice(len(offtask.services))
            # services = offtask.services[choice]
            # data_size = services[2]*8
            # cpu_cycle = data_size * services[1]
            # d_const=services[3]
           # ue=User()
            # user_tlist=ue.Task_list
            #for k in range(numoftasks):
        # i = 0
        # while i < num:
            #task[i] = Task( i,np.random.uniform(0.3, 0.5), np.random.randint(900, 1100),1.2 )
            task[i] = Task( us_id,dz[i], cn[i],dl[i])
            #task[i] = Task( i,data_size, cpu_cycles,d_const)
            #i += 1
        return task
    
    def gen_Task_List(self):
        total_tasks=numoftasks*numofUsers
        task_info_len=3 #cpucycles,datasize,delaytolerance
        tasklist=np.zeros((numofUsers,numoftasks,task_info_len))
        #tasklist=np.arange(total_tasks*task_info_len).reshape(numofUsers,numoftasks,task_info_len)
        for i in range(numofUsers):
            ue=User()
            user_tlist=ue.Task_list
            for k in range(numoftasks):
             tasklist[i][k][0]=user_tlist[k].cpucycles
             tasklist[i][k][1]=user_tlist[k].datasize
             tasklist[i][k][2]=user_tlist[k].dalaytolerance
       
        return tasklist
           
    def reset_env(self):
        # self.sum_task_size = 100 * 1048576  # 总计算任务60 Mbits -> 60 80 100 120 140
        # self.e_battery_uav = 500000  # uav电池电量: 500kJ
        # self.loc_uav = np.random.randint(50,100,size=[numOfUAV,2])
        
        self.mecs_info = [MEC() for i in range(numofMEC)]
        self.uavs_info = [UAV() for i in range(numOfUAV)]
        self.cloud_info = Cloud() 
        self.loc_ue_list = np.random.randint(0, 301, size=[numofUsers, 2])   # 位置信息:x在0-100随机
        self.user_inf=[User() for i in range(numofUsers)]
        #UE=User()
        #self.Task_list=UE.Task_list # 随机计算任务1.5~2Mbits -> 1.5~2 2~2.5 2.5~3 3~3.5 3.5~4
        
        # self.task_list = np.random.randint(3145728, 3670017, self.M)  # 随机计算任务1.5~2Mbits -> 1.5~2 2~2.5 2.5~3 3~3.5 3.5~4
        # self.task_list = np.random.randint(3670016, 4194305, self.M)  # 随机计算任务1.5~2Mbits -> 1.5~2 2~2.5 2.5~3 3~3.5 3.5~4
        #self.block_flag_list = np.random.randint(0, 2, numoftasks) 


    def reset(self):
        self.reset_env()
        # uav battery remain, uav loc, remaining sum task size, all ue loc, all ue task size, all ue block_flag
        # self.state = np.append(self.e_battery_uav, self.loc_uav)
        # self.state = np.append(self.state, self.sum_task_size)
        # self.state = np.append(self.state, np.ravel(self.loc_ue_list))
        # self.state = np.append(self.state, self.task_list)
        # self.state = np.append(self.state, self.block_flag_list)
        return self._get_obs()

    def _get_obs(self):
        self.count_wrong = 0
        self.exe_delay = 0
        self.proc_energy=0
        #self.is_off = [0] * self.num_task # offload decision
        self.alloc_resource = [0] * numoftasks # allocated resource
        # Remaining resources
        for i in range(self.numofresources):
            if i< numOfUAV:
                for u in range(numOfUAV):
                    self.rest_resource[i] = self.uavs_info[u].f_uav
            elif i<numOfUAV+numofMEC:
                 for m in range(numofMEC):
                     self.rest_resource[i] = self.mecs_info[m].Fmax
            else:
                self.rest_resource[i] = self.cloud_info.Fmax
                
        self.progress = [0] * numoftasks # progress
        self.new_task()
        uv=UAV()
        # np.array(self.is_off).astype(int)
        # np.array(self.alloc_resource).astype(int)
        # np.array(self.rest_resource).astype(int)
        # np.array(self.progress).astype(int)
        # state = np.concatenate((self.is_off, self.alloc_resource, self.rest_resource, self.progress)).reshape((4, 10))
        state = np.concatenate(( self.progress, self.alloc_resource, self.rest_resource))
        # state = np.append(state, np.ravel(self.loc_ue_list))
        # state=np.append(state,np.ravel(self.uavs_locs))
        
        #state=np.append(self.rest_resource,self.task_data)
        #self.state=np.append(self.state,self.loc_ue_list) 
        
        #state=np.array(state)
       
        return state
    
    def new_task(self):
        self.waiting.clear()
        # Number of pending tasks
        rest = numoftasks - sum(self.progress)
        length = np.random.randint(1, self.numofresources) if rest >= self.numofresources else rest
        # What task should start
        task_id = sum(self.progress)
        self.waiting.extend(range(task_id, task_id + length))
        self.new_queue = 1

    def step(self, action):  # 0: Select the ue number of the service; 1: direction theta; 2: distance d; 3: offloading ratio
        
        reward=0
       
        #step_redo = False
        # is_terminal = False
        # offloading_ratio_change = False
        # reset_dist = False
        action=np.array(action)
        #print('action value:', action)
        #ue_id = int(action[0])
        #task_id = int(action[1])
        action = (action + 1) / 2  # Set the action in the range of -1~1 -> the action in 0~1. Avoid training the actor network tanh function to always take the boundary 0 when the original action_bound is [0,1]
        #print('action 0-1 value:', action)
        #################Find the best service object UE#####################
         # Improve ddpg, add a layer to the output layer to output discrete actions (implementation results are incorrect)
         # Using the closest distance algorithm, there is an error. If the closest distance UAV keeps on the head (wrong)
         # Random polling: first generate a random number queue, remove the UE after the service is completed, and generate randomly again when the queue is empty (the logic is wrong)
         # The control variable is mapped to the value range of each variable
        # if action[0] >= 1:
        #     ue_id = numofUsers - 1
        # else:
        #     ue_id = int(numofUsers * action[0])

        # if action[1] >= 1:
        #     task_id = numoftasks - 1
        # else:
        #     task_id = int(numoftasks * action[1])
        #             #theta = action[1] * np.pi * 2  # angle
        #     #layer_idx=[1,2]
        if action[0]>=1:
            off_layer=2
        else:
            off_layer=int(3*action[0])
            
        if off_layer==2:
            sel_server=0
        else:
        
            if action[1]>=1:
                 sel_server=2
            else:
                 sel_server=int(3*action[1])    
        req_comp_cap = int((action[2] + 1) * 2000 / 2) + 1000    
        
        
        
        task_id = self.waiting[0]
        ue_id = self.offtasks[task_id].ue
        dtol = self.offtasks[task_id].dalaytolerance
        task_size = self.offtasks[task_id].dalaytolerance
        task_cycles = self.offtasks[task_id].dalaytolerance
        ue_loc=self.loc_ue_list[ue_id]
        uavcount=0
        meccount=0
        cloudcount=0
        

        if self.new_queue == 1:
           for i in range(self.numofresources):
               if i< numOfUAV:
                   for u in range(numOfUAV):
                       self.rest_resource[i] = self.uavs_info[u].f_uav
               elif i<numOfUAV+numofMEC:
                    for m in range(numofMEC):
                        self.rest_resource[i] = self.mecs_info[m].Fmax
               else:
                   self.rest_resource[i] = self.cloud_info.Fmax  
            
        layer=''
          
        #print('user id=',ue_id,' task id= ',task_id,'offloading layer: ',off_layer,' selected server=',sel_server)
           
        #dtol=UE.Task_list[task_id].dalaytolerance
            
        # if off_layer == 0: #Local computing
        #         layer='Local Computing'
        #         f=UE.cpu_freq
        #         t=task_cycles/f
        #         e=(parameter["User_energy_ceof"]*f**3)*t
                
                
        #         if t <= dtol:
        #             self.progress[task_id] = 1
        #             self.alloc_resource[task_id] = f
        #             self.done = True if sum(self.progress) == numofUsers*numoftasks else False
        #             reward = dtol - t 
        #             self.exe_delay += t
        #             self.proc_energy+=e
        #         else:
        #             self.progress[task_id] = 1
        #             self.count_wrong += 1
        #             self.done = True if sum(self.progress) == numofUsers*numoftasks else False
        #             reward = -dtol 
        #             self.exe_delay += t
        #             self.proc_energy+=e
                    
        if off_layer== 0:  #UAV Offloading
                layer='UAV Computing'
               # UE=self.user_inf[ue_id]
                uavlist=self.uavs_info
                uavid=int(sel_server)
                off_uav=uavlist[uavid]
                uavcount+=1
                #f=off_uav.f_uav
                #tran_t=off_uav.cal_transmit_time(task_size)
                theta = action[3] * np.pi * 2 # angle
                dis_fly = action[4] * off_uav.flight_speed * 1 # 1s flying distance
                [tran_t,uav_exec_t]=off_uav.uav_com_delay(uavid,ue_loc, dis_fly, theta, task_size, task_cycles)
                #exec_t=off_uav.cal_processing_time(task_cycles)
                #trans_e=off_uav.cal_transmit_energy(task_size)
                ue_trans_e=off_uav.cal_transmit_energy(uavid,ue_loc, dis_fly, theta, task_size, task_cycles)
                [uav_exec_e,user_exec_e]=off_uav.cal_processing_energy(task_cycles,dis_fly)
                total_t=tran_t+uav_exec_t
                totaluser_e=ue_trans_e+user_exec_e
                #print("%s = %s\n" %(" selected server frequency: ", self.rest_resource[uavid]) )
                #print("\n selected server frequency: "+ '{:d}'.format(self.rest_resource[uavid]))
                #print("%s = %s\n" %("\ndelay:" , total_t)+ "%s = %s\n" %(", cost energy: ", totaluser_e)+"%s = %s\n" %( ", layer: ", layer) )
                if total_t <= dtol and uav_exec_e < off_uav.e_battery_uav and req_comp_cap<=self.rest_resource[uavid]:
                    self.progress[task_id] = 1
                    self.offtasks[task_id].notexpire=True
                    self.alloc_resource[task_id] = req_comp_cap
                    self.rest_resource[uavid] -=req_comp_cap
                    self.done = True if sum(self.progress) == numoftasks else False
                    #reward =(1-omega)*self.offtasks[task_id].notexpire-total_t-omega*totaluser_e+sconst
                    reward = dtol - total_t
                    self.waiting.popleft()
                    off_uav.e_battery_uav -=uav_exec_e
                    self.exe_delay += total_t
                    self.proc_energy += totaluser_e
                else:
                    self.progress[task_id] = 1
                    self.offtasks[task_id].notexpire=False
                    self.count_wrong += 1
                    self.done = True if sum(self.progress) == numoftasks else False
                    reward = -dtol
                    #reward =(1-omega)*self.offtasks[task_id].notexpire-total_t-omega*totaluser_e+sconst
                    self.waiting.popleft()
                    self.exe_delay += total_t
                    self.proc_energy += totaluser_e
                #print("%s = %s\n" %("delay:" , total_t)+  "%s = %s" %(", timeconstraints: ", dtol) + "%s = %s" %(", cost energy: ", totaluser_e) + "%s = %s" %(", uav cost energy: ", uav_exec_e) +"%s = %s" %( ", layer: ", layer)+"%s = %s" %( ", reward: ", reward))
                    
        elif off_layer== 1:  #MEC Offloading
                layer='Edge Computing'
                meclist=self.mecs_info
                mecid=int(sel_server)
                off_mec=meclist[mecid]
                meccount+=1
                #f=off_mec.Fmax
                tran_t=off_mec.cal_transmit_time(task_size)
                exec_t=off_mec.cal_processing_time(task_cycles)
                trans_e=off_mec.cal_transmit_energy(task_size)
                exec_e=off_mec.cal_processing_energy(task_cycles)
                total_t=tran_t+exec_t
                total_e=trans_e+exec_e
               # print("%s = %s\n" %(" selected server frequency: ", self.rest_resource[mecid+numOfUAV]) )
                #print("%s = %s\n" %("\ndelay:" , total_t)+ "%s = %s\n" %(", cost energy: ", total_e) +"%s = %s\n" %( ", layer: ", layer))
                if total_t <= dtol and req_comp_cap<=self.rest_resource[mecid+numOfUAV]:
                    self.progress[task_id] = 1
                    self.alloc_resource[task_id] = req_comp_cap
                    self.rest_resource[mecid+numOfUAV] -=req_comp_cap
                    self.done = True if sum(self.progress) == numoftasks else False
                    self.offtasks[task_id].notexpire=True
                    reward = dtol - total_t
                    #reward=(1-omega)*self.offtasks[task_id].notexpire- total_t-omega*total_e+sconst
                    self.waiting.popleft()
                    self.exe_delay += total_t
                    self.proc_energy += total_e
                else:
                    self.progress[task_id] = 1
                    self.count_wrong += 1
                    self.done = True if sum(self.progress) == numoftasks else False
                    self.offtasks[task_id].notexpire=False
                    reward = -dtol
                    #reward=(1-omega)*self.offtasks[task_id].notexpire- total_t-omega*total_e+sconst
                    self.waiting.popleft()
                    self.exe_delay += total_t
                    self.proc_energy += total_e    
                #print("%s = %s\n" %("delay:" , total_t)+  "%s = %s" %(", timeconstraints: ", dtol) + "%s = %s" %(", cost energy: ", total_e) +"%s = %s" %( ", layer: ", layer)+"%s = %s" %( ", reward: ", reward))
        elif off_layer== 2:  #Cloud Offloading
                layer='Cloud Computing'
                off_cloud=self.cloud_info
                cloudcount+=1
                #f=off_cloud.Fmax
                tran_t=off_cloud.cal_transmit_time(task_size)
                exec_t=off_cloud.cal_processing_time(task_cycles)
                trans_e=off_cloud.cal_transmit_energy(task_size)
                exec_e=off_cloud.cal_processing_energy(task_cycles)
                total_t=tran_t+exec_t
                total_e=trans_e+exec_e
                #print("%s = %s\n" %(" selected server frequency: ", self.rest_resource[numofMEC+numOfUAV]) ) 
                
                if total_t <= dtol and req_comp_cap<=self.rest_resource[numofMEC+numOfUAV]:
                      self.progress[task_id] = 1
                      self.alloc_resource[task_id] = req_comp_cap
                      self.rest_resource[numofMEC+numOfUAV] -=req_comp_cap
                      self.done = True if sum(self.progress) == numoftasks else False
                      self.offtasks[task_id].notexpire=True
                      reward = (dtol - total_t) 
                      #reward=(1-omega)*self.offtasks[task_id].notexpire- total_t-omega*total_e+sconst
                      self.waiting.popleft()
                      self.exe_delay += total_t
                      self.proc_energy += total_e
                else:
                      self.progress[task_id] = 1
                      self.count_wrong += 1
                      self.done = True if sum(self.progress) == numoftasks else False
                      self.offtasks[task_id].notexpire=False
                      #reward=(1-omega)*self.offtasks[task_id].notexpire- total_t-omega*total_e+sconst
                      reward = -dtol
                      self.waiting.popleft()
                      self.exe_delay += total_t
                      self.proc_energy += total_e      
                #print("%s = %s\n" %("delay:" , total_t)+  "%s = %s" %(", timeconstraints: ", dtol) +"%s = %s" %(", cost energy: ", total_e) +"%s = %s" %( ", layer: ", layer)+"%s = %s" %( ", reward: ", reward))
        # Update the status at the next moment file_name = 'output.txt'
         # file_name = 'output_ddpg_' + str(self.bandwidth_nums) + 'MHz.txt'
        
        if self.waiting:
            self.new_queue = 0
        else:
            self.new_task()
            self.new_queue = 1
        
        
        self.info=[self.exe_delay, self.proc_energy,uavcount,meccount,cloudcount]
        # print("\nUE-" + '{:d}'.format(ue_id) + ", task size: " + '{:d}'.format(int(task_size)) + ", Task_id:" + '{:.2f}'.format(task_id)+", progress:" + '{:d}'.format(sum(self.progress)))
        # #file_obj.write("\n:Offloading Layer" + '{:.s}'.format(layer) + ", selected server: " + '{:.s}'.format(sel_server)) 
        # print("%s = %s\n" %("Offloading Layer", off_layer)+", %s = %s\n" %("selected server: ", sel_server) )
        # print("\ndelay:" + '{:.2f}'.format(self.exe_delay)+ ", cost energy: "+ '{:.2f}'.format(self.proc_energy)+ ", Done: "+ '{:d}'.format(int(self.done))+", Reward: "+ '{:.2f}'.format(reward) )
        
        # ue moves randomly
        for i in range(numofUsers): 
                tmp = np.random.rand()
                if 0.6 <tmp <= 0.7:
                    self.loc_ue_list[i] += [0, 1]
                elif 0.7 <tmp <= 0.8:
                    self.loc_ue_list[i] += [1, 0]
                elif 0.8 <tmp <= 0.9:
                    self.loc_ue_list[i] += [0, -1]
                else:
                    self.loc_ue_list[i] += [-1, 0]
                np.clip(self.loc_ue_list[i], 0, 300)
                
        state = np.concatenate((self.progress, self.alloc_resource, self.rest_resource))
        # state = np.append(state, np.ravel(self.loc_ue_list))
        # state=np.append(state,np.ravel(self.uavs_locs))
        
        file_name = 'output.txt'
        with open(file_name, 'a') as file_obj:
          file_obj.write("\nUE-" + '{:d}'.format(ue_id) + ", task size: " +  ", Task_id:" + '{:.2f}'.format(task_id)+", progress:" + '{:.2f}'.format(sum(self.progress)))
          #file_obj.write("\n:Offloading Layer" + '{:.s}'.format(layer) + ", selected server: " + '{:.s}'.format(sel_server)) 
          file_obj.write("%s = %s\n" %("Offloading Layer", layer)+", %s = %s\n" %("selected server: ", sel_server) )
          file_obj.write("\ndelay:" + '{:.2f}'.format(self.exe_delay)+ ", cost energy: "+ '{:.2f}'.format(self.proc_energy)+ ", Done: "+ '{:d}'.format(int(self.done))+", %s = %s\n" %(" Reward: ", reward) )
           

           # self.reset2(self.exe_delay, self.proc_energy, task_size,ue_id)   # Reset ue task size, remaining total task size, ue position, and record to file

        return state, reward, self.done,self.info

    # # Reset ue task size, remaining total task size, ue position, and record to file
    # def reset2(self, delay, x, y, offloading_ratio, task_size, ue_id):
    #     self.sum_task_size -= self.task_list[ue_id]  # remaining task amount
        
    #     for i in range(self.M): # ue position after random movement
    #          tmp = np.random.rand(2)
    #          theta_ue = tmp[0] * np.pi * 2 # ue random movement angle
    #          dis_ue = tmp[1] * self.delta_t * self.v_ue # ue random movement distance
    #          User.loc_ue_list[i][0] = User.loc_ue_list[i][0] + math.cos(theta_ue) * dis_ue
    #          User.loc_ue_list[i][1] = User.loc_ue_list[i][1] + math.sin(theta_ue) * dis_ue
    #          User.loc_ue_list[i] = np.clip(User.loc_ue_list[i], 0, self.ground_width)
    #     self.reset_step() # ue random calculation task 1~2Mbits # 4 ue, ue occlusion situation
    #      # Record UE cost
    #     file_name = 'output.txt'
    #     # file_name = 'output_ddpg_' + str(self.bandwidth_nums) + 'MHz.txt'
    #     with open(file_name, 'a') as file_obj:
    #         file_obj.write("\nUE-" + '{:d}'.format(ue_id) + ", task size: " + '{:d}'.format(int(task_size)) + ", offloading ratio:" + '{:.2f}'.format(offloading_ratio))
    #         file_obj.write("\ndelay:" + '{:.2f}'.format(delay))
    #         file_obj.write("\nUAV hover loc:" + "[" + '{:.2f}'.format(x) + ', ' + '{:.2f}'.format(y) + ']')  # 输出保留两位结果

    # Calculate the cost
    # def com_delay(self, loc_ue, loc_uav, offloading_ratio, task_size, block_flag):
    #     dx = loc_uav[0] - loc_ue[0]
    #     dy = loc_uav[1] - loc_ue[1]
    #     dh = self.height
    #     dist_uav_ue = np.sqrt(dx * dx + dy * dy + dh * dh)
    #     p_noise = self.p_noisy_los
    #     if block_flag == 1:
    #         p_noise = self.p_noisy_nlos
    #     g_uav_ue = abs(self.alpha0 / dist_uav_ue ** 2)  # Channel gain
    #     trans_rate = self.B * math.log2(1 + self.p_uplink * g_uav_ue / p_noise)  # Uplink transmission rate bps
    #     t_tr = offloading_ratio * task_size / trans_rate  # upload delay, 1B=8bit
    #     t_edge_com = offloading_ratio * task_size / (self.f_uav / self.s)  # Calculate the delay on the UAV edge server
    #     t_local_com = (1 - offloading_ratio) * task_size / (self.f_ue / self.s)  # local calculation delay
    #     if t_tr < 0 or t_edge_com < 0 or t_local_com < 0:
    #         raise Exception(print("+++++++++++++++++++!! error !!++++++++++++++++++++++++ +"))
    #     return max([t_tr + t_edge_com, t_local_com])  # Flight time impact factor

class User():
    def __init__(self):
     self.block_flag_list = np.random.randint(0, 2,numofUsers)  # 4 ue, ue occlusion situation
     self.loc_ue_list = np.random.randint(0, 501, size=[numofUsers, 2])  # Location information: x is random at 0-100
     #self.task_list = np.random.randint(1572864, 2097153, M) # Random calculation task 1.5~2Mbits -> Corresponding total task size 60
    #self.task_list = np.random.randint(2097153, 2621440, M)  # Random calculation task 2~2.5Mbits -> 80
     #self.Task_list=[offtask.get_random_task() for i in range(numoftasks)]#generate rondom task list
     self.Task_list=multi_tier_env.get_task_info(numoftasks) #generate rondom task list
     self.trans_power=parameter["user_tr_power"] 
     #self.trans_power=23 #user transmision power in MHZ
     self.proc_power=5
     self.idle_power=.3
     #self.cpu_freq=.5e9
     self.cpu_freq=np.random.randint(800, 900)*10**6
     self.energy_ceof=1e-25
     
    # def get_task_info(self,num):
    #     task_list=[offtask.get_random_task() for i in range(num)]
    #     # for i in range(num):
    #     #         task_list[i]=offtask.get_random_task()
    #     return task_list

class Task():
    def __init__(self,ue, dz,cyc,dt):
        self.ue=ue
        self.datasize=dz
        self.cpucycles=cyc
        self.dalaytolerance=dt
        self.notexpire=False
        
        