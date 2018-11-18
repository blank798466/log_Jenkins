# coding=utf-8
import requests
import time
# from pprint import pprint
import MySQLdb
from DBUtils.PooledDB import PooledDB
import sys
import HTMLParser


reload(sys)
sys.setdefaultencoding('utf-8')

job = 'service'
# job = sys.argv[1]


def getjson(url):
    try:
        # 通过解析url获取其中的json数据
        req = requests.get(url)
        res = req.json()
        return res
    except Exception:
        return None

# 获取需要的三种url: jobUrl,stagesUrl,nodesUrl
# 以及获取的对应的解析的json数据: jobCon,stagesCon,nodesCon


url = "http://192.168.11.248:8083/job/" + job + "/wfapi/runs"
jobId = getjson(url)[0]['id']  # 解析url获取当前id
# jobId = 114
jobUrl = 'http://192.168.11.248:8083/job/%s/%s/wfapi/describe' % (job, jobId)
# print jobUrl
stagesUrl, nodesUrl, stagesCon, nodesCon = [[], [], [], []]


# 解析jobUrl并获取stagesUrl
jobCon = getjson(jobUrl)
Pid = jobCon['id']
jobname = job
if 'FAILED' in [i['status'] for i in jobCon['stages']]:
    status = 'FAILED'
else:
    status = 'SUCCESS'
startTimeMillis = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(jobCon['startTimeMillis']/1000+28800))
endTimeMillis = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(jobCon['startTimeMillis']/1000+28800))
durationMillis = str(jobCon['durationMillis']/1000.0) + 's'
queueDurationMillis = str(jobCon['queueDurationMillis'])
pauseDurationMillis = str(jobCon['pauseDurationMillis'])
stages_count = len(jobCon['stages'])
for i in jobCon['stages']:
    stagesUrl.append('http://192.168.11.248:8083'+i['_links']['self']['href'])
# print(stagesUrl)


def getstage(stageUrl):
    # 获取stage阶段的各个属性值
    stage_Con = getjson(stageUrl)
    Sid = Pid + stage_Con['id']
    Sname = stage_Con['name']
    SexecNode = stage_Con['execNode']
    Sstatus = stage_Con['status']
    if Sstatus == 'FAILED':
        SerrorMessage = stage_Con['error']['message']
        SerrorType = stage_Con['error']['type']
    else:
        SerrorMessage = ''
        SerrorType = ''
    SstartTimeMillis = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(stage_Con['startTimeMillis']/1000+28800))
    SdurationMillis = str(stage_Con['durationMillis']/1000.0) + 's'
    SpauseDurationMillis = str(stage_Con['pauseDurationMillis'])
    Cnodes_count = len(stage_Con['stageFlowNodes'])
    # 获取nodesUrl
    for node in stage_Con['stageFlowNodes']:
        url1 = 'http://192.168.11.248:8083' + node['_links']['self']['href']
        url2 = 'http://192.168.11.248:8083' + node['_links']['log']['href']
        nodesUrl.append((url1, url2))
    return [Sid, Sname, SexecNode, Sstatus, SerrorMessage, SerrorType,
            SstartTimeMillis,SdurationMillis, SpauseDurationMillis, Cnodes_count]

# 解析stagesUrl
# 如果当前stage阶段错误，则不执行后续stage阶段


i = 0
last_status = 'SUCCESS'
while i < len(stagesUrl):
    if last_status == 'SUCCESS':
        con = getstage(stagesUrl[i])
        con.insert(1, Pid)
        con.insert(10, stagesUrl[i])
        stagesCon.append(con)
        # print con
        last_status = con[4]
    else:
        break
    i += 1
# pprint(stagesCon)
# pprint(nodesUrl)


def getnode(url1, url2):
    # 获取node的describe信息和log信息
    node_Con = getjson(url1)
    log_Con = getjson(url2)
    Nid = Pid+node_Con['id']
    Sid = Pid+node_Con['parentNodes'][0]
    Nname = node_Con['name']
    NexecNode = node_Con['execNode']
    Nstatus = node_Con['status']
    NerrorMessage = ''
    NerrorType = ''
    NerrorParameterDescription = ''
    if Nstatus == 'FAILED':
        NerrorMessage = node_Con['error']['message']
        NerrorType = node_Con['error']['type']
    if 'parameterDescription' in node_Con.keys():
        NerrorParameterDescription = node_Con['parameterDescription']
    NstartTimeMillis = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(node_Con['startTimeMillis'] / 1000 + 28800))
    NdurationMillis = str(node_Con['durationMillis'] / 1000.0) + 's'
    NpauseDurationMillis = str(node_Con['pauseDurationMillis'])
    hasMore = str(log_Con['hasMore'])
    Ntextlength = str(log_Con['length'])
    NtextContent = ''
    if 'text' in log_Con.keys():
        # html反转义
        NtextContent = HTMLParser.HTMLParser().unescape(log_Con['text'])
        NtextContent = NtextContent.replace('\'', '').replace('\n', '')
    return [Nid, Sid, Nname, NexecNode, Nstatus,
            NerrorMessage, NerrorType, NerrorParameterDescription,
            NstartTimeMillis, NdurationMillis, NpauseDurationMillis,
            hasMore, Ntextlength, NtextContent]

# 解析nodesUrl并获取nodesCon
# 如果当前node阶段错误，则不执行后续node阶段


j = 0
last_status = 'SUCCESS'
while j < len(nodesUrl):
    if last_status == 'SUCCESS':
        con = getnode(nodesUrl[j][0], nodesUrl[j][1])
        con.insert(11, nodesUrl[j][0])
        con.insert(12, nodesUrl[j][1])
        nodesCon.append(con)
        # print con
        last_status = con[4]
    else:
        break
    j += 1
# pprint(nodesCon)
print len(nodesCon[0])


# 连接数据库mysql进行存储相关日志数据
pool = PooledDB(MySQLdb, 5,
                host='192.168.11.248',
                port=10086,
                user='root',
                passwd='whu12345',
                db='logs')
conn = pool.connection()
cursor = conn.cursor()


# jobCon
job_Con = '\',\''.join([Pid, jobname, status, startTimeMillis,
                   endTimeMillis, durationMillis, queueDurationMillis,
                   pauseDurationMillis, jobUrl])

sql_1 = 'INSERT INTO logs.logs_pipeline VALUES(\'%s\',%d);' % (job_Con, stages_count)
# print sql_1


# stagesCon
sql_stages = []
for i in stagesCon:
    # print i
    stage_Con = '\',\''.join(i[:-1])
    sql_2 = 'INSERT INTO logs.logs_stages VALUES(\'%s\',%d);' \
            % (stage_Con, i[-1])
    # print sql_2
    sql_stages.append(sql_2)


# nodesCon
sql_nodes = []
for i in nodesCon:
    # print i
    node_Con = '\',\''.join(i)
    # print node_Con
    sql_3 = 'INSERT INTO logs.logs_nodes VALUES(\'%s\');' % node_Con
    print sql_3
    sql_nodes.append(sql_3)


try:

    cursor.execute(sql_1)

    for sql_2 in sql_stages:
        cursor.execute(sql_2)

    for sql_3 in sql_nodes:
        print cursor.execute(sql_3)

    conn.commit()

except Exception as e:
    print e
    conn.rollback()

cursor.close()
conn.close()
