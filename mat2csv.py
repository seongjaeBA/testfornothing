# import scipy.io
from scipy.io import loadmat
# import numpy as np
import pandas as pd
import xlsxwriter



# mat = scipy.io.loadmat('C:/Users/OBELAB_JH_DESKTOP/Documents/GitHub/Data_AnalysisTool/ActivationMap/brainmodel.mat')
mat = loadmat('C:/Users/OBELAB_JH_DESKTOP/Documents/GitHub/Data_AnalysisTool/ActivationMap/brainmodel.mat')

# for i in mat:
#     if '__' not in i and 'readme' not in i:
#           np.savetxt(("file.csv"),mat[i],delimiter=',')


# mat.pop('__header__')
# mat.pop('__version__')
# mat.pop('__globals__')


workbook =  xlsxwriter.Workbook('brainmodel.xlsx')
worksheet = workbook.add_worksheet()

row = 0
col = 0

for k in mat.keys():
    row += 1
    worksheet.write(row, col, k)
    for v in mat[k]:
        print(v)
        if isinstance(v, (list, tuple)):
                r = ''.join(v)
                worksheet.write_string(row, col + 1, r)
                row += 1
        else:
                worksheet.write(row, col + 1, v)
                row += 1
        
workbook.close()