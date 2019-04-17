import numpy as np                                                               
from numpy.random import normal                                                  
import matplotlib.pyplot as plt
from scipy.stats import norm                                                  

# gaussian distributed random numbers with mu =4 and sigma=2                     
x = normal(4, 2, 10000)                                                            

mean = np.mean(x)
sigma = np.std(x)

x -= mean 

x_plot = np.linspace(min(x), max(x), 1000)                                                               

fig = plt.figure()                                                               
ax = fig.add_subplot(1,1,1)                                                      

ax.hist(x, bins=50, normed=True, label="data")
ax.plot(x_plot, norm.pdf(x_plot, mean, sigma), 'r-', label="pdf")                                                          

ax.legend(loc='best')

x_ticks = np.arange(-4*sigma, 4.1*sigma, sigma)                                  
x_labels = [r"${} \sigma$".format(i) for i in range(-4,5)]                       

ax.set_xticks(x_ticks)                                                           
ax.set_xticklabels(x_labels)                                                     

plt.show() 

# import os
# import pandas as pd
# import numpy as np
# import scipy as sp
# import matplotlib as  mlt
# from matplotlib import pyplot as plt
# from statsmodels.graphics.gofplots import qqplot



# df = pd.read_csv('c:/')
# # f = pd.read_csv(, sheet=0)

# print(df.head)
# print(df.tail)
# print(df.describe)

# df2 = df.dropna(how='all')


# df2[df2.dtypes[(df2.dtypes=="float64")|(df2.dtypes=="int64")].index.values].hist(figsize=[15,15])
# df2.hist(figsize=[18, 18])

# qqplot(df.LDSB, line='s')
# plt.show()

# rows, columns = df2.shape

# if i in df2.corr():
