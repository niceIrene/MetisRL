import time
import random
import thread
import numpy

TM = [[0.0 for col in range(16)] for row in range(16)]

count = 0
flowSize = 0.6
burst_rate = 0.8

def pickbool(probabilities):
	x = random.uniform(0,1)
	if (x > probabilities):
		return 0
	else:
		return 1

def generateFlow( src, dst):
	size_arr = numpy.random.normal(0.2,1,1000)
	size = numpy.mean(size_arr)
	TM [src][dst] += size;

def generateFlowSkew(src, dst, pod):
	if pod == 0:
		size_arr = numpy.random.normal(0,1,1000)
		size = numpy.mean(size_arr)
		if size < 0:
			size = 0
		TM [src][dst] += size;
	if pod == 1:
		size_arr = numpy.random.normal(0.05,1,1000)
		size = numpy.mean(size_arr)
		TM [src][dst] += size;
	if pod == 2:
		size_arr = numpy.random.normal(0.1,1,1000)
		size = numpy.mean(size_arr)
		TM [src][dst] += size;
	if pod == 3:
		size_arr = numpy.random.normal(0.2,1,1000)
		size = numpy.mean(size_arr)
		TM [src][dst] += size;


def killFlow(TM1, TM2):
	tmp = [[0.0 for col in range(16)] for row in range(16)]
	for i in range (16):
		for j in range(16):
			tmp[i][j] = TM1[i][j] - TM2[i][j]

def flowSimulationProb():
	TMPlus1 = [[0.0 for col in range(16)] for row in range(16)]#the increase 2s ago
	TMPlus2 = [[0.0 for col in range(16)] for row in range(16)]#the increase 2s ago
	burst_rate = pickbool(0.1)
	P_edg = 0.5
	P_pod = 0.3
	while(1):
		for i in range(16):
			edgBool = pickbool(P_edg)
			Pod1 = pickbool(P_pod)
			Pod2 = pickbool(P_pod)
			Pod3 = pickbool(P_pod)
			#generate flow to edg
			if i%2 == 1:
				plus = -1
			else:
				plus = 1
			if edgBool ==1 and burst_rate == 1:
				generateFlowSkew(i, i + plus, i/4)
				TMPlus1[i][i+plus] +=flowSize
			#generate flow to pod
			if i % 4 ==3:
				Podd1 = i-3
				Podd2 = i-2
				Podd3 = i-1
			elif i% 4 == 2:
				Podd1 = i+1
				Podd2 = i-2
				Podd3 = i-1 
			elif i % 4 == 1:
				Podd1 = i+2
				Podd2 = i+1
				Podd3 = i-1
			elif i % 4 ==0:
				Podd1 = i+3
				Podd2 = i+2
				Podd3 = i+1
			if Pod1 == 1 and burst_rate ==1:
				generateFlowSkew(i, Podd1, i/4)
				TMPlus1[i][Podd1] += flowSize
			if Pod2 ==1 and burst_rate ==1:
				generateFlowSkew(i, Podd2, i/4)
				TMPlus1[i][Podd2] += flowSize
			if Pod3 == 1 and burst_rate ==1:
				generateFlowSkew(i, Podd3, i/4)
				TMPlus1[i][Podd3] += flowSize
			#generate flow to the other
			for k in range(16):
				if k/4 == i/4:
					continue
				flag = pickbool(1-P_pod-P_edg)
				if flag ==1 and burst_rate ==1:
					#generateFlowSkewSkew(i, k, i/4)
					generateFlowSkew(i, k, i/4)
					TMPlus1[i][k] += flowSize
		reward(TM)
		time.sleep(1)
		killFlow(TM,TMPlus2)
		TMPlus2 = [[0.0 for col in range(16)] for row in range(16)]
		for i in range(16):
			edgBool = pickbool(P_edg)
			Pod1 = pickbool(P_pod)
			Pod2 = pickbool(P_pod)
			Pod3 = pickbool(P_pod)
			#generate flow to edg
			if i%2 == 1:
				plus = -1
			else:
				plus = 1
			if edgBool ==1 and burst_rate ==1:
				generateFlowSkew(i, i + plus, i/4)
				TMPlus2[i][i+plus] +=flowSize
			#generate flow to pod
			if i % 4 ==3:
				Podd1 = i-3
				Podd2 = i-2
				Podd3 = i-1
			elif i% 4 == 2:
				Podd1 = i+1
				Podd2 = i-2
				Podd3 = i-1 
			elif i % 4 == 1:
				Podd1 = i+2
				Podd2 = i+1
				Podd3 = i-1
			elif i % 4 ==0:
				Podd1 = i+3
				Podd2 = i+2
				Podd3 = i+1
			if Pod1 == 1 and burst_rate ==1:
				generateFlowSkew(i, Podd1, i/4)
				TMPlus2[i][Podd1] += flowSize
			if Pod2 ==1 and burst_rate ==1:
				generateFlowSkew(i, Podd2, i/4)
				TMPlus2[i][Podd2] += flowSize
			if Pod3 == 1 and burst_rate ==1:
				generateFlowSkew(i, Podd3, i/4)
				TMPlus2[i][Podd3] += flowSize
			#generate flow to the other
			for k in range(16):
				if k/4 == i/4:
					continue
				flag = pickbool(1-P_pod)
				if flag ==1 and burst_rate ==1:
					generateFlowSkew(i, k, i/4)
					TMPlus2[i][k] += flowSize
		time.sleep(1)
		killFlow(TM, TMPlus1)
		TMPlus1 = [[0.0 for col in range(16)] for row in range(16)]
		TM_arr = numpy.array(TM)
		numpy.savetxt('TM.csv', TM_arr, delimiter = ',')
		reward(TM)
		burst_rate = pickbool(0.2)
		#print "aaaaaaaaaaaaaaaaaaaaaaaaaaa"

def flowSimulationRandom():
	TMPlus1 = [[0.0 for col in range(16)] for row in range(16)]#the increase 2s ago
	TMPlus2 = [[0.0 for col in range(16)] for row in range(16)]#the increase 2s ago
	burst_rate = pickbool(0.1)
	P_edg = 0.333
	P_pod = 0.333
	while(1):
		for i in range(16):
			edgBool = pickbool(P_edg)
			Pod1 = pickbool(P_pod)
			Pod2 = pickbool(P_pod)
			Pod3 = pickbool(P_pod)
			#generate flow to edg
			if i%2 == 1:
				plus = -1
			else:
				plus = 1
			if edgBool ==1 and burst_rate == 1:
				generateFlowSkew(i, i + plus, i/4)
				TMPlus1[i][i+plus] +=flowSize
			#generate flow to pod
			if i % 4 ==3:
				Podd1 = i-3
				Podd2 = i-2
				Podd3 = i-1
			elif i% 4 == 2:
				Podd1 = i+1
				Podd2 = i-2
				Podd3 = i-1 
			elif i % 4 == 1:
				Podd1 = i+2
				Podd2 = i+1
				Podd3 = i-1
			elif i % 4 ==0:
				Podd1 = i+3
				Podd2 = i+2
				Podd3 = i+1
			if Pod1 == 1 and burst_rate ==1:
				generateFlowSkew(i, Podd1, i/4)
				TMPlus1[i][Podd1] += flowSize
			if Pod2 ==1 and burst_rate ==1:
				generateFlowSkew(i, Podd2, i/4)
				TMPlus1[i][Podd2] += flowSize
			if Pod3 == 1 and burst_rate ==1:
				generateFlowSkew(i, Podd3, i/4)
				TMPlus1[i][Podd3] += flowSize
			#generate flow to the other
			for k in range(16):
				if k/4 == i/4:
					continue
				flag = pickbool(1-P_pod)
				if flag ==1 and burst_rate ==1:
					#generateFlowSkewSkew(i, k, i/4)
					generateFlowSkew(i, k, i/4)
					TMPlus1[i][k] += flowSize
		reward(TM)
		time.sleep(1)
		killFlow(TM,TMPlus2)
		TMPlus2 = [[0.0 for col in range(16)] for row in range(16)]
		for i in range(16):
			edgBool = pickbool(P_edg)
			Pod1 = pickbool(P_pod)
			Pod2 = pickbool(P_pod)
			Pod3 = pickbool(P_pod)
			#generate flow to edg
			if i%2 == 1:
				plus = -1
			else:
				plus = 1
			if edgBool ==1 and burst_rate ==1:
				generateFlowSkew(i, i + plus, i/4)
				TMPlus2[i][i+plus] +=flowSize
			#generate flow to pod
			if i % 4 ==3:
				Podd1 = i-3
				Podd2 = i-2
				Podd3 = i-1
			elif i% 4 == 2:
				Podd1 = i+1
				Podd2 = i-2
				Podd3 = i-1 
			elif i % 4 == 1:
				Podd1 = i+2
				Podd2 = i+1
				Podd3 = i-1
			elif i % 4 ==0:
				Podd1 = i+3
				Podd2 = i+2
				Podd3 = i+1
			if Pod1 == 1 and burst_rate ==1:
				generateFlowSkew(i, Podd1,i/4)
				TMPlus2[i][Podd1] += flowSize
			if Pod2 ==1 and burst_rate ==1:
				generateFlowSkew(i, Podd2,i/4)
				TMPlus2[i][Podd2] += flowSize
			if Pod3 == 1 and burst_rate ==1:
				generateFlowSkew(i, Podd3,i/4)
				TMPlus2[i][Podd3] += flowSize
			#generate flow to the other
			for k in range(16):
				if k/4 == i/4:
					continue
				flag = pickbool(1-P_pod)
				if flag ==1 and burst_rate ==1:
					generateFlowSkew(i, k,i/4)
					TMPlus2[i][k] += flowSize
		time.sleep(1)
		killFlow(TM, TMPlus1)
		TMPlus1 = [[0.0 for col in range(16)] for row in range(16)]
		TM_arr = numpy.array(TM)
		
		reward(TM)
		burst_rate = pickbool(0.8)
		#print "aaaaaaaaaaaaaaaaaaaaaaaaaaa"

def flowSimulationStride(stride):
	TMPlus1 = [[0.0 for col in range(16)] for row in range(16)]#the increase 2s ago
	TMPlus2 = [[0.0 for col in range(16)] for row in range(16)]#the increase 2s ago
	burst_rate = pickbool(0.8)
	while(1):
		for i in range(16):
			if burst_rate == 1:
				generateFlowSkew(i, (i+stride)%16,i/4)
				TMPlus1[i][(i+stride)%16]
		reward(TM)
		time.sleep(1)
		killFlow(TM,TMPlus2)
		for i in range(16):
			if burst_rate == 1:
				generateFlowSkew(i, (i+stride)%16,i/4)
				TMPlus2[i][(i+stride)%16]
		reward(TM)
		time.sleep(1)
		killFlow(TM,TMPlus1)	
		burst_rate = pickbool(0.8)	



def getlinkTraffic(TM, out, pod, num):
	summ = 0
#	if pod ==0 and num ==0:
#		print TM
	for i in range(pod*4, pod*4+3):
		for j in range(16):
			if int(j/4) == int(i/4):
				continue
			if out[j][i] == pod:
				flag1 = 1
			else:
				flag1 = 0
			if out[i][j] == pod:
				flag2 = 1
			else:
				flag2 = 0
			summ += TM[j][i]*flag1
			summ += TM[i][j]*flag2
	return summ

def reward(TM):
	if not open("OUT.csv",'r'):
		out_arr =numpy.loadtxt(open("OUT.csv"), delimiter = ",")
		out = out_arr.tolist()
	else:
		out=[[0,0,0,0,1,1,1,1,2,2,2,2,3,3,3,3]for i in range(16)]
	
	link00 = getlinkTraffic(TM, out, 0, 0)
	link01 = getlinkTraffic(TM, out, 0, 1)
	link02 = getlinkTraffic(TM, out, 0, 2)
	link03 = getlinkTraffic(TM, out, 0, 3)
	link10 = getlinkTraffic(TM, out, 1, 0)
	link11 = getlinkTraffic(TM, out, 1, 1)
	link12 = getlinkTraffic(TM, out, 1, 2)
	link13 = getlinkTraffic(TM, out, 1, 3)
	link20 = getlinkTraffic(TM, out, 2, 0)
	link21 = getlinkTraffic(TM, out, 2, 1)
	link22 = getlinkTraffic(TM, out, 2, 2)
	link23 = getlinkTraffic(TM, out, 2, 3)
	link30 = getlinkTraffic(TM, out, 3, 0)
	link31 = getlinkTraffic(TM, out, 3, 1)
	link32 = getlinkTraffic(TM, out, 3, 2)
	link33 = getlinkTraffic(TM, out, 3, 3)
	used = [link00,link01,link02,link03,link10,link11,link12,link13,link20,link21,link22,link23,link30,link31,link32,link33]
	print used
	TM_arr = numpy.array(TM)
	
	numpy.savetxt('TM.csv', TM_arr, delimiter = ',')
	used_arr = numpy.array(used)
	numpy.savetxt('USE.csv', used_arr, delimiter = ',')


while(1):

#	flowSimulationStride(8)
#  the parameter for stride range from 1,2,4,8
#	flowSimulationRandom()

	flowSimulationProb()
#go to line 55,56 set P_edg and P_pod as (1,0)(0.5,0.3)(0.2,0.3)