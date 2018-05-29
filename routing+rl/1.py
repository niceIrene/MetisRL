import numpy as np
import tensorflow as tf

b=[[0,0,0,0,1,1,1,1,2,2,2,2,3,3,3,3] for i in range(16)]

np.savetxt('OUT.csv',b,delimiter=',',dtype='int32')

