
import datetime as dt
import csv
import matplotlib.pyplot as plt
import json


# https://data.nasa.gov/resource/eva.json (with modifications)
input_file = open('./eva-data.json', 'r', encoding='ascii')

output_file = open('./eva-data.csv','w', encoding='utf-8')
graph_file = './cumulative_eva_graph.png'



data=[]


for _ in range(375):
    line=input_file.readline()
    print(line)
    data.append(json.loads(line[1:-1]))
#data.pop(0)
## Comment out this bit if you don't want the spreadsheet


csv_writer=csv.writer(output_file)


time = []
date =[]

j=0
for _ in data:
    print(data[j])
    # and this bit
    csv_writer.writerow(data[j].values())
    if 'duration' in data[j].keys():
        duration_str=data[j]['duration']
        if duration_str == '':
            pass
        else:
            duration_dt=dt.datetime.strptime(duration_str,'%H:%M')
            duration_hours = dt.timedelta(hours=duration_dt.hour, minutes=duration_dt.minute, seconds=duration_dt.second).total_seconds()/(60*60)
            print(duration_dt,duration_hours)
            time.append(duration_hours)
            if 'date' in data[j].keys():
                date.append(dt.datetime.strptime(data[j]['date'][0:10], '%Y-%m-%d'))
                #date.append(data[j]['date'][0:10])

            else:
                time.pop(0)
    j+=1

duration_dt=[0]
for i in time:
    duration_dt.append(duration_dt[-1]+i)

date,time = zip(*sorted(zip(date, time)))



plt.plot(date,duration_dt[1:], 'ko-')
plt.xlabel('Year')
plt.ylabel('Total time spent in space to date (hours)')
plt.tight_layout()
plt.savefig(graph_file)
plt.show()
