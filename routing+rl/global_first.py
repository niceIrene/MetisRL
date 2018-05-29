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
time_interval=3
K=10




def SDN_DM():
    a=np.loadtxt(open("TM.csv"),delimiter=",")
    return a
def SDN_USE():
    a=np.loadtxt(open("USE.csv"),delimiter=",")
    return a.T
def SDN_APPLY(a):
    np.savetxt('OUT.csv',a,delimiter=',')
def step():
    perform=[]
    for j in range(5000):
        link_load=[0 for i in range(16)]
        DM=SDN_DM()
        
        
        a=[[0 for i in range(16)]for i in range(16)]
        for i in range(16):
            for j in range(16):
                if int(i/4)==int(j/4):
                    a[i][j]=0
                else:
                    src=int(i/4)
                    dst=int(j/4)
                    for k in range(4):
                        link1=k*4+src
                        link2=k*4+dst
                        choose=-1
                        if link_load[link1]<=200 and link_load[link2]<200:
                            choose=k
                            link_load[link1]+=DM[i][j]
                            link_load[link2]+=DM[i][j]
                            break
                        if choose==-1:
                            choose=random.randint(0,3)
                            link_load[choose*4+src]+=DM[i][j]
                            link_load[choose*4+dst]+=DM[i][j]
        SDN_APPLY(a)
        time.sleep(time_interval)
        USE=SDN_USE()
        ratio=0
        for i in range(LINK_N):
            
            if USE[i]>ratio:
                ratio=USE[i]
        ratio=ratio/200
        print ("DM",sum(sum(DM)),ratio)
        perform.append(ratio)
step()

























