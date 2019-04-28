import os
from sklearn import linear_model as lm
import pandas as pd



path = os.path.dirname(os.path.abspath(__file__))

f = os.path.join(path, 'filename')
data = pd.read_csv(f)



lasso = lm.Lasso()
 
parameters = {'alpha' : [1e-15, 1e-10, 1e-8, 1e-4, 1e-3, 1e-2, 1, 5, 10, 20]}



