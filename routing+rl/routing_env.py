import numpy as np
import pandas as pd
import time
import sys
import queue
import copy


HOS_N=16 #有多少个host
LINK_N=16 #有多少个link
alpha=1
beta=0.5 #这两个参数都是用来控制reward的，目前reward就是最大利用率减去超过了的利用率
time_interval=1
K=10




class Net():
    def __init__(self):
        self.DM_K=queue.Queue(K)#(每次保存前k个demand matrix，有新的进入就把旧的丢弃)
        self.observation_space=np.ones((K*HOS_N*HOS_N))#过去k个DM
        self.action_space=np.ones((4*HOS_N*(HOS_N-4)))
        self.Bandwidth=[10 for i in range (LINK_N)] #假设现在带宽都是10
        self.USE=[5 for i in range(LINK_N)] # 使用到的带宽，假设都是5
        self.episode=0
        self.b=[]
        self.l=[]
    def SDN_DM(self):
        a=np.loadtxt(open("TM.csv"),delimiter=",")
        return a
        #sdn拿到现在的demand matrix
    def SDN_APPLY(self,action):#action矩阵通过sdn应用到实际网络中
        a=list(action[0])
        b=np.ones((16,16))
        for i in range(16):
            for j in range(16):
                if (int(i/4)==int(j/4)):
                    b[i][j]=0
                else:
                    if int(j/4)>int(i/4):
                        b[i][j]=a[i*12+j-4*int((i/4))]
                    else:
                        b[i][j]=a[i*12+j]
        np.savetxt('OUT.csv',b,delimiter=',')

        
    def SDN_USE(self):
        a=np.loadtxt(open("USE.csv"),delimiter=",")

        return a.T

        #拿到现在的链路利用
    def SDN_BAND(self):
        a=[200 for i in range(LINK_N)]
        return a
        #拿到每个链路capacity


    def reset(self): #初始化的时候返回环境，问题是最开始的k次如何拿到，建议先等待k次，然后再开始学习
        DM_TEM=queue.Queue(K)
        while self.DM_K.full()==False:
            time.sleep(time_interval)
            a=self.SDN_DM()#接口1，拿到demand matrix
            DM_TEM.put(a)
            self.DM_K.put(a)
        for i in range(K):
            a=DM_TEM.get()
            for j in range(HOS_N):
                for k in range(HOS_N):
                    self.observation_space[i*HOS_N*HOS_N+j*HOS_N+k]=a[j][k]
        return self.observation_space

            






    def step(self,action):
        self.SDN_APPLY(action)#接口2，sdn把拿到的action应用到网络中
        time.sleep(time_interval)#过一个episode
        self.USE=self.SDN_USE()#接口3，sdn拿到链路利用的bandwidth
        self.Bandwidth=self.SDN_BAND()#接口4，sdn拿到每个链路的capacity
        a=self.SDN_DM()#接口1，拿到demand matrix
        
        ratio=0
        punish=0
        self.episode=self.episode+1

        avg=sum(self.USE)/16
        minn=0




        for i in range(LINK_N):
            if i==0:
                minn=self.USE[0]
            if self.USE[i]<minn:
                minn=self.USE[i]


            if self.USE[i]>ratio:
                ratio=self.USE[i]
                
            if self.USE[i]>200:
                punish+=self.USE[i]/self.Bandwidth[i]
        print ("DM",sum(sum(a)),ratio/200)
        ratio=(ratio-minn)/200
        ratio=ratio/avg
        
       
        
        self.l.append(ratio)
        reward=-ratio*alpha-punish*beta
        
        done=False
        
        self.DM_K.get()
        self.DM_K.put(a)
        for i in range(K):
            a=self.DM_K.get()
            for j in range(HOS_N):
                for k in range(HOS_N):
                    self.observation_space[i*HOS_N*HOS_N+j*HOS_N+k]=a[j][k]
            self.DM_K.put(a)

        s_=self.observation_space

        return s_, reward, done
    




        


