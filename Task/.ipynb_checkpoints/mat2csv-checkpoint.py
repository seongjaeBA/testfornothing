import scipy.io
import numpy as np



mat = scipy.io.loadmat('C:/Users/OBELAB_JH_DESKTOP/Documents/GitHub/Data_AnalysisTool/ActivationMap/brainmodel.mat')

for i in mat:
    if '__' not in i and 'readme' not in i:
          np.savetxt(("file.csv"),mat[i],delimiter=',')
          