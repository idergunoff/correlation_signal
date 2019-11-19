from scipy import stats
import os
measure = []
files = os.listdir('Data_Corr')
for file in files:
    with open('Data_Corr/'+file) as f:
        file_izm = [list(row.split('\t')) for row in f.readlines()]
        file_izm.pop(0)
        for i in file_izm:
            component = list(map(float, i))
            component.pop(0)
            measure.append(component)

print(measure)