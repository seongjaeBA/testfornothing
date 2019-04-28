"""
작성자: cmlee
작성일: 190320
기능: 작성된 함수의 전체 Test 코드 작성
    개별 함수에 대한 코드는 하단 __name__ = __main__ 형태로 두었음.
구조:

용례:

"""

import dataIO
import dataPreProcess as dpp
import dataPostProcess as dpp2
from runtime import runtime

import dataVisualization as dv
import matplotlib.pyplot as plt
import numpy as np
import os


# Load data

myData = dataIO.DataRaw()
print(dir(myData))
DIR = os.path.abspath( "examples" )
print(DIR)

file_name = os.path.join(DIR, '180530 1452_cmlee_test_000035_stroop_Raw.csv')
print(file_name)
myData.set_value(file_name, 'csv')

# myData shape print
print(myData.raw.d780.shape)
print(myData.raw.d850.shape)
print(myData.battery.shape)
print(myData.accel.shape)
print(myData.gyro.shape)

# set spec
raw780 = myData.raw.d780.values
raw850 = myData.raw.d850.values
spec = dataIO.DataSpec()

# set basic values
spec.set_ndata(len(myData.timestamp))
myData.set_task_block(spec)

# bpf
bpf780 = dpp.bpf(raw780, spec)
bpf850 = dpp.bpf(raw850, spec)

# calculate snr
snr780 = dpp.snr(bpf780, spec)
snr850 = dpp.snr(bpf850, spec)
myData.snr_map.d780 = snr780
myData.snr_map.d850 = snr850

# calculate dOD
dod780 = dpp.find_dod(bpf780, spec)
dod850 = dpp.find_dod(bpf850, spec)

# calculate mbll
hbo, hbr, hbt = dpp.find_mbll(dod780, dod850, spec)
ch_rej = dpp.find_ch_rej(raw780, raw850, snr780, snr850, hbo, hbr, spec)
myData.mbll.HbO = hbo
myData.mbll.HbR = hbr
myData.mbll.HbT = hbt

# calculate IMU
[filt_ang_x, filt_ang_y, filt_ang_z, ths_motion_xyz, _, _] = dpp.degree_imu(myData.accel, myData.gyro, spec)
myData.motion.ang_x = filt_ang_x
myData.motion.ang_y = filt_ang_y
myData.motion.ang_z = filt_ang_z
myData.motion.motion_thd = ths_motion_xyz

# calculate mdOD
mdod780 = dpp.find_mdod(dod780, filt_ang_x, filt_ang_y, filt_ang_z, ths_motion_xyz, spec, ch_rej)
mdod850 = dpp.find_mdod(dod850, filt_ang_x, filt_ang_y, filt_ang_z, ths_motion_xyz, spec, ch_rej)

# spike removal
sdod780 = dpp.spike_removal(mdod780, spec)
sdod850 = dpp.spike_removal(mdod850, spec)

# bpf and apply new baseline
bdod780 = dpp.new_baseline(dpp.bpf(sdod780, spec), spec)
bdod850 = dpp.new_baseline(dpp.bpf(sdod850, spec), spec)

# calculate mbll (corrected)
hbo_new, hbr_new, hbt_new = dpp.find_mbll(bdod780, bdod850, spec)
ch_rej_new = dpp.find_ch_rej(raw780, raw850, snr780, snr850, hbo_new, hbr_new, spec)

# apply channel rejection + center padding (교환만)
hbo_new_padded, ch_rej_new = dpp.padding_ch3(dpp.apply_ch_rej(hbo_new, ch_rej_new), ch_rej_new, spec)
hbr_new_padded, _ = dpp.padding_ch3(dpp.apply_ch_rej(hbr_new, ch_rej_new), ch_rej_new, spec)
myData.mod_mbll.HbO = hbo_new_padded
myData.mod_mbll.HbR = hbr_new_padded
myData.mod_mbll.HbT = hbo_new_padded + hbr_new_padded
myData.ch_rej = ch_rej_new

# region clustering
hbo_new_clustered, block_rej = dpp.clustering_ch(hbo_new_padded, ch_rej_new, spec)
hbr_new_clustered, _ = dpp.clustering_ch(hbr_new_padded, ch_rej_new, spec)
myData.mod_clustered_mbll.HbO = hbo_new_clustered
myData.mod_clustered_mbll.HbR = hbr_new_clustered
myData.mod_clustered_mbll.HbT = hbo_new_clustered + hbr_new_clustered
myData.block_rej = block_rej

# extract blocks
block_mbll = dpp2.blocknize_data(myData.mod_mbll.HbO, myData, spec)
myData.mod_block_mbll = block_mbll


# close existing figures
plt.close("all")

# plot raw
ts_graph1 = dv.TimeSeriesPlot()
timestamp = myData.timestamp
ts_graph1.set_x_values(timestamp)
ts_graph1.set_y_values(raw780)
ts_graph1.set_label('test_x_label', 'test_y_label', 'test title')
ts_graph1.draw_now(1, '--')

# ts_graph2 = dv.TimeSeriesPlot()
# timestamp = myData.timestamp
# ts_graph2.set_x_values(timestamp)
# ts_graph2.set_y_values(raw850)
# ts_graph2.set_label('test_x_label', 'test_y_label', 'test title')
# ts_graph2.draw_now(2, '-')

# # draw snr map
ts_graph1 = dv.TimeSeriesPlot()
timestamp = myData.timestamp
ts_graph1.set_x_values(timestamp)
ts_graph1.set_y_values(snr780[0:48, :])
ts_graph1.set_label('time', 'snr', 'snr780')
ts_graph1.draw_now(3, '-')

# ts_graph2 = dv.TimeSeriesPlot()
# ts_graph2.set_x_values(timestamp)
# ts_graph2.set_y_values(snr850[0:48, :])
# ts_graph2.set_label('time', 'snr', 'snr850')
# ts_graph2.draw_now(4, '-')

# draw dOD
ts_graph1 = dv.TimeSeriesPlot()
timestamp = myData.timestamp
ts_graph1.set_x_values(timestamp)
ts_graph1.set_y_values(dod780[0:48, :])
ts_graph1.set_label('test_x_label', 'dod780', 'test title')
ts_graph1.draw_now(5, '-')

# ts_graph2 = dv.TimeSeriesPlot()
# timestamp = myData.timestamp
# ts_graph2.set_x_values(timestamp)
# ts_graph2.set_y_values(dod850[0:68, :])
# ts_graph2.set_label('test_x_label', 'dod850', 'test title')
# ts_graph2.draw_now(6, '-')

# draw MBLL
ts_graph1 = dv.TimeSeriesPlot()
timestamp = myData.timestamp
ts_graph1.set_x_values(timestamp)
ts_graph1.set_y_values(hbo[0:48, :])
ts_graph1.set_label('frames', 'HbO2', 'MBLL output')
ts_graph1.draw_now(7, '-')


# # make test signal and test with spike & step removal
# random_number1 = np.random.randint(0, 200, 10)
# random_number2 = np.random.randint(0, 20, 200)
# random_number = np.concatenate((random_number1, random_number2))
# np.random.shuffle(random_number)
# random_number[int(len(random_number)/2):] += 100
# random_number[:int(len(random_number)/2)] += 30
# plt.plot(random_number)
#
# input_signal = np.array(random_number)
# output = dpp.spike_removal(input_signal)
# t = np.arange(0, len(input_signal), 1)
# plt.plot(t, input_signal, t, output)