### site: https://medium.com/coinmonks/visualizing-brain-imaging-data-fmri-with-python-3e1899d1e212
### https://github.com/akcarsten/fMRI_data_analysis/blob/master/Intro_to_fMRI_Data_Part_I_Data_Structure.ipynb
## Generalize가 아닌 General 이기 때문에 위 사이트에서 참조.

import numpy as np
import numpy.linalg as npl
from numpy import matrix
# import scipy.linalg as spl 
##당연한 얘기지만 이게 더 빠르다 여기서는 npl을 사용하고 나중에 개선하자.

def do_GLM(X, y):
    if X.shape[1] > X.shape[0]:
        # Returns a view of the array with axes transposed.
        X = X.transpose()# X.T면 충분할 것같은데.. np 버전이나 np.transepose때문에 이렇게 쓰는걸까.
    tmp = npl.inv(X.transepose().dot(X))
    tmp = tmp.dot(X.transepose())

    #pre-allacate variables : 값이 0인 배열 생성 zeros
    beta = np.zeros((y.shape[0], X.shape[1]))
    e = np.zeros(y.shape)
    model = np.zeros(y.shape)
    r = np.zeros(y.shape)

# Find the beta values, the error and the correlation coefficients 
# between the model and the data for each voxel in the data.
    for i in range(y.shape[0]):
        beta[i]  = tmp.dot(y[i,:].transpose())
        model[i] = X.dot(beta[i])
        e[i]     = (y[i,:] - model[i])
        r[i]     = np.sqrt(model[i].var()/y[i,:].var())
    
    return beta, model, e, r

# Run the GLM
beta, model, e, r = do_GLM(design_matrix, data)


## design_matrix는 최상단 링크에서 확인할것