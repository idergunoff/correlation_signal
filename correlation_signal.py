from scipy import stats
import numpy as np
import os
import matplotlib.pyplot as plt

meas = list()
all_meas_comp = list()
files = os.listdir('Data_Corr')
for file in files:
    with open('Data_Corr/'+file) as f:
        file_izm = [list(row.split('\t')) for row in f.readlines()]
        file_izm.pop(0)
        for i in file_izm:
            component = list(map(float, i))
            component.pop(0)
            meas.append(component)
        meas_comp = np.array(meas)
        meas_comp = meas_comp.transpose()
        all_meas_comp.extend(meas_comp)
        meas = list()
print(len(all_meas_comp))


all_result_corr = list()
all_result_plvl = list()
corr_row = list()
plvl_row = list()

result_corr = list()
result_corr_for_hist = list()
result_signals = list()
result_index = list()
result_row = list()
i = 0
while i < len(all_meas_comp):
    j = 0
    signal1 = all_meas_comp[i]
    while j < len(all_meas_comp):
        signal2 = all_meas_comp[j]
        corr, plvl = stats.spearmanr(signal1, signal2)
        corr_row.append(corr)
        plvl_row.append(plvl)
        if corr >= 0.5 and corr < 0.999 and plvl <= 0.05:
            result_row.append(str(((i+1)//24)+1)+'-'+str((i+1)%24)+' and '+str(((j+1)//24)+1)+'-'+str((j+1)%24))
            result_row.append(corr)
            result_row.append(plvl)
            result_corr.append(result_row)
            result_row = list()
            if result_index.count(i+1) < 1:
                result_index.append(i+1)
                result_signals.append(signal1)
            if result_index.count(j+1) < 1:
                result_index.append(j+1)
                result_signals.append(signal2)
            if result_corr_for_hist.count(corr) < 1:
                result_corr_for_hist.append(corr)
        j += 1
    all_result_corr.append(corr_row)
    all_result_plvl.append(plvl_row)
    i += 1
    j = 0
    corr_row = list()
    plvl_row = list()

result_index_name = list()
for i in result_index:
    result_index_name.append(str((i//24)+1)+'comp'+str(i%24))
result_index_name.append('super_signal')


print(result_corr)
print(len(result_corr))
print(len(result_signals))

super_signal = [0]*1711
for i in result_signals:
    super_signal += i
result_signals.append(super_signal)

print(result_index)
print(result_index_name)

f_result_signal = open('result_signal.txt', 'w')
for i in result_index_name:
    f_result_signal.write(i+'\t')
f_result_signal.write('\n')
j = 0
while j < len(result_signals[0]):
    for i in result_signals:
        f_result_signal.write(str(i[j])+'\t')
    f_result_signal.write('\n')
    j += 1
f_result_signal.close()

f_result_corr = open('result_corr.txt', 'w')
f_result_corr.write('pair\tcorr\n')
for i in result_corr:
    f_result_corr.write(i[0]+'\t'+str(i[1])+'\n')
f_result_corr.close()
ax = plt.subplots()
plt.plot(super_signal)
#plt.pcolor(all_result_corr, cmap='bwr')
plt.show()

