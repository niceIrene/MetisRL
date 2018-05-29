import numpy as np
import pandas as pd
import time
import sys
import queue
import copy
import random


HOS_N=16 #有多少个host
LINK_N=16 #有多少个link
alpha=1
beta=0.5 #这两个参数都是用来控制reward的，目前reward就是最大利用率减去超过了的利用率
time_interval=2
K=10





def SDN_APPLY():#action矩阵通过sdn应用到实际网络中
    b=np.ones((16,16))
    for i in range(16):
        for j in range(16):
            b[i][j]=random.randint(0,3)
    np.savetxt('OUT.csv',b,delimiter=',')

        
def SDN_USE():
    a=np.loadtxt(open("USE.csv"),delimiter=",")

    return a.T

        #拿到现在的链路利用
def SDN_BAND():
    a=[200 for i in range(LINK_N)]
    return a
        #拿到每个链路capacity

def SDN_DM():
    a=np.loadtxt(open("TM.csv"),delimiter=",")
    return a
    





def step():
    
    perform=[]
    for j in range(1000):
        DM=SDN_DM()
        
        SDN_APPLY()#接口2，sdn把拿到的action应用到网络中
        time.sleep(time_interval)#过一个episode
        USE=SDN_USE()#接口3，sdn拿到链路利用的bandwidth
        Bandwidth=SDN_BAND()#接口4，sdn拿到每个链路的capacity
        
        ratio=0
        punish=0
        minn=0
        

        avg=sum(USE)/16
        for i in range(LINK_N):
            
            if USE[i]>ratio:
                ratio=USE[i]
                
        
        ratio=ratio/200
        print ("DM",sum(sum(DM)),ratio)
        
        
        perform.append(ratio)
    


        
step()
        
    




        


