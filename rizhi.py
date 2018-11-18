# coding=utf-8
import requests
import time
from pprint import pprint
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

# job = 'service'
job = sys.argv[1]

url = "http://192.168.11.248:8083/job/" + job + "/wfapi/runs"
myjson = requests.get(url)
lb = myjson.json()[0]
pprint(lb)

# new a dict to store logs
logs_lb = {}

lb_id = lb['id']
# lb_status = lb['status']
lb_startTimeMillis = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(lb['startTimeMillis']/1000+28800))
lb_endTimeMillis = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(lb['endTimeMillis']/1000+28800))
lb_durationMillis = lb['durationMillis']/1000.0
lb_stages = []
for i in lb['stages']:
    lb_stages.append((i['name'],
                      i['status'],
                      i['durationMillis']/1000.0))
if 'FAILURE' in [i[1] for i in lb_stages]:
    lb_status = 'FAILURE'
else:
    lb_status = 'SUCCESS'

fileUrl = '/var/jenkins_home/workspace/' + job + '/' + lb_id + '.log'
with open(fileUrl, 'w') as f:
    f.write("Pipeline-%s 第%s次构建,构建状态为%s \n" % (job, lb_id, lb_status))
    f.write("开始构建时间为：%s \n" % lb_startTimeMillis)
    f.write("构建结束时间为：%s \n" % lb_endTimeMillis)
    f.write("构建总耗时：%s s \n" % lb_durationMillis)
    for i in range(len(lb_stages)):
        f.write("Stage %s： %s 构建状态为：%s,构建时长为：%s s. \n" % (i, lb_stages[i][0],lb_stages[i][1],lb_stages[i][2]))
