import sys
import pandas as pd
import numpy as np
import scipy as sp
from scipy import stats
from numpy.random import seed
from numpy.random import randn
from statsmodels.graphics.gofplots import qqplot
from matplotlib import pyplot as plt


data = pd.read_excel('C:/Users/OBELAB_JH_DESKTOP/Downloads/WJ_project/fnirs/fnirs_feature.xlsx')


for index in data:
    idx = str(index)
    qqplot(data['%s' % (index)], line='s')
plt.show
