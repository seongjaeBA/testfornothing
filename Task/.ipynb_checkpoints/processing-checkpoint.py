import os
import pandas as pd
import numpy as np
import scipy as sp
import matplotlib as  mlt
from matplotlib import pyplot as plt
from statsmodels.graphics.gofplots import qqplot



df = pd.read_csv('c:/')
# f = pd.read_csv(, sheet=0)

print(df.head)
print(df.tail)
print(df.describe)

df2 = df.dropna(how='all')


df2[df2.dtypes[(df2.dtypes=="float64")|(df2.dtypes=="int64")].index.values].hist(figsize=[15,15])
df2.hist(figsize=[18, 18])

qqplot(df.LDSB, line='s')
plt.show()

rows, columns = df2.shape

if i in df2.corr():


