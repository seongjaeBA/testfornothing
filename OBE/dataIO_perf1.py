##기본 
import os
import sys
import math

##데이터 처리
import pandas as pd
import numpy as np
import scipy as sp
from scipy import stats

## 서버 접속
import requests
from requests.auth import HTTPBasicAuth

## 시각화
import seaborn as sns
import matplotlib as mpl
from matplotlib import pyplot as plt


def make_list(WJ_list = 'wj_list', p_list = pd.DataFrame()):
    """
        작성자: sjyoo
        작성일: 190612
        기능: list와 raw 파일 AVG, RT 등을 merge
        입력: 데이터 table <- 지금은 excel file
        출력: C:/Users/OBELAB_JH_DESKTOP/Documents/GitHub/testfornothing/OBE/data/ ~~ xlsx파일
        용례: data_merge(리스트, 로우 데이타, 멀지 아웃풋)
        배고프네...
    """
    path = os.getcwd()
    f2 = os.path.join(path, "data", WJ_list + '.xlsx')
    List = pd.read_excel(open(f2, 'rb'), header=0)
    List = List.merge(p_list, left_on=['name', 'parent'], right_on=['childName',  'parentName'] , how = 'outer')
    List.to_excel(WJ_list + '.xlsx', sheet_name = 'data')

def data_merge(WJ_list = 'wj_list', raw_file = 'output', merge = 'merge'):
    """
        작성자: sjyoo
        작성일: 190612
        기능: list와 raw 파일 AVG, RT 등을 merge
        입력: 데이터 table <- 지금은 excel file
        출력: C:/Users/OBELAB_JH_DESKTOP/Documents/GitHub/testfornothing/OBE/data/ ~~ xlsx파일
        용례: data_merge(리스트, 로우 데이타, 멀지 아웃풋)
        배고프네...
    """
    Task = {}
    task_list = ['REST', 'CBTTF', 'CBTTB', 'GNG', 'TWOBACK', 'STRC', 'STRI', 'REPEAT', 'MIND', 'FOLD']
    print('merge 시작')
    # file = os.path.join(path, "data", 'sj_perforamance.xls')
    path = os.getcwd()
    f1 = os.path.join(path, "data", raw_file + '.xlsx')
#     f2 = os.path.join(path, "data", WJ_list + '.xlsx')
    f2 = os.path.join(path, WJ_list + '.xlsx')

    List1 = pd.read_excel(open(f2, 'rb'), header=0)
    

    for i in range(len(task_list)):
        Task[task_list[i]] = pd.read_excel(open(f1, 'rb'), sheet_name = '%s' % task_list[i], header=None).T.dropna(how = 'all')
        Task[task_list[i]] = pd.DataFrame.from_dict(Task[task_list[i]])
        Task[task_list[i]] = Task[task_list[i]].replace(['TASKMARKER','OUTTOUCH', 'TASKMARKER\r','OUTTOUCH\r'],['', '', '', '']).dropna(axis = 1, how = 'all')
        Task[task_list[i]] = Task[task_list[i]].fillna('damm')
        


    for task in task_list:
#         print(Task[task])
        print(task)
        pack = pd.DataFrame(Task[task][0])
        idx = Task[task].index
        # print(idx)
        # print(col)
        col = Task[task].columns
        
        if 'GNG' in task or 'TWOBACK' in task or 'STRC' in task or 'STRI' in task:
            Cor_list = []
            RT = []
            Acc =[]
#             print(Task[task])
            for i in idx:
                Cor = 0
                LV = 0
                RT_list = []
                for j in col:
                    if Task[task][j][i][:2] == 'LV':
                        marker = Task[task][j][i].split('/')
                        if 'LV' in marker[0]:
                            Cor += int(marker[1])
                            LV += 1
                            if '1-1' in marker[2]:
                                if int(marker[3]) < 2000 :
                                    RTint = int(marker[3])
                                    RT_list.append(RTint)
                        else:
                            continue
                    else:
                        pass
                 
                Cor_list.append(Cor)
                if len(RT_list) is not 0:
                    RT.append(sum(RT_list) / len(RT_list))
                else:
                    RT.append(0)
                
                if LV == 0:
                    Acc.append(0)
                else:
                    Acc.append(Cor/LV)
                
            pack['%s_Cor' % task] = Cor_list
            pack['%s_RT' % task] = RT
            pack['%s_ACC' % task] = Acc
            print('정답률, 반응시간')
            print('과제 완료')
            
            
        elif 'CBTTF' in task or 'CBTTB' in task or 'MIND' in task or 'REPEAT' in task or 'FOLD' in task:
            Cor_list = []
            Acc =[]
            for i in idx:
                Cor = 0
                LV = 0
                for j in col:
                    if Task[task][j][i][:2] == 'LV':
                        marker = Task[task][j][i].split('/')
                        if 'LV' in marker[0]:
                            Cor += int(marker[1])
                            LV += 1
                        else:
                            continue
                    else:
                        pass

                Cor_list.append(Cor)
                if LV == 0:
                    Acc.append(0)
                else:
                    Acc.append(Cor/LV)
            
            pack['%s_Cor' % task] = Cor_list
            pack['%s_ACC' % task] = Acc
            print('정답률')
            print('과제 완료')
            
        else:
            print('과제 pass')
            pass
        List1 = List1.merge(pack, left_on='taskUUID', right_on=0 , how = 'outer')

    List1.pop('0_x')
    List1.pop('0_y')
    List1.to_excel(merge + '.xlsx', sheet_name = 'data')
    print('완료')
    return
    
def raw_to_data(raw):
    """
        작성자: sjyoo
        작성일: 190611
        기능: table을 분석용 dict로 내보내기
        입력: raw table(dataframe)
        출력: data = dict{pd.DataFrame{task pivot)}
        용례: data = raw_to_data(pandas DataFrame(raw))
        메모: 데이터에 따라 pivot/pivot_table 조절
    """
    tasks = {1:'REST',2:'CBTTF',3:'CBTTB',4:'GNG',5:'TWOBACK',6:'STRC',7:'STRI',8:'VFT',9:'REPEAT',10:'MIND',11:'FOLD'}
    data = {}
    for task in tasks.values():
        data[task]= pd.DataFrame()
    
    task_num = raw['taskType'].unique()
    for k in task_num:
        task_ind = raw.query('taskType == "' + k +'"')
        # data = task_ind.pivot(columns = 'childName', values = 'raw')
        # data = pd.pivot_table(task_ind, index = 'index', columns = 'childName', values = 'raw', aggfunc=np.sum, margins = True)
        data[tasks[int(k)]] = pd.pivot_table(task_ind, index = 'index', columns = 'taskUUID', values = 'raw', aggfunc=np.sum)
    print('%s  실행' % task)
    return data


def request_to_table(url, uuid, my_id, my_pw):
    """
        작성자: cmlee
        수정자: sjyoo
        작성일: 190509
        수정일: 190611 
        기능: 요청 정보를 이용해서 서버에서 데이터 테이블 형태로 반환
        입력: url, id, pw, taskuuid
        출력: pandas DataFrame : header + contents
        용례: raw, list_raw = request_to_table(str(api_url), str(uuid)/ list(uuid), str(my_id), str(my_pw))
    """
    raw = pd.DataFrame()
    list_raw = pd.DataFrame()
    print('table 요청 시작')
    for child in uuid:
        print(child + '_로딩 중....')
        url_uuid = url + '?taskUUID=' + child
        r = requests.get(url=url_uuid, auth=HTTPBasicAuth(my_id, my_pw))
        r = r.content.decode("utf-8")
        r = r.split('\n')
        t_head = r.pop(0).split(',')
        t_head[-1] = t_head[-1][0:-1]
        t_body = [t.split(',') for t in r if t != '']
        full = pd.DataFrame(t_body, columns=t_head)
        full = full[full.taskUUID != '']
        tasks = full['taskType'].unique()
        for task in tasks:
            task_data = full.query('taskType == "' + str(task) +'"')
            mx = task_data.taskSubID.max()
            if mx != '':
                t_mx_data = task_data.query('taskSubID == "'+str(mx)+'"')
                raw = pd.concat([raw, t_mx_data], axis=0)
        print('%s 완료' % child)
    list_raw['name'] = raw['childName'].unique()
    list_raw['uuid'] = raw['taskUUID'].unique()
    print("raw export 완료")
    return raw, list_raw


def access_to_table(connect_info, uuid, table = 'uuid'):
    """
        작성자: sjyoo
        작성일: 190611
        기능: table 접속
        입력: connect_info: id, pw; uuid = taskuuid; table = str(table categoty)
        출력: pandas DataFrame(table) 
        용례: raw = access_to_table(connect_info, uuid, table = 'uuid'&'raw'&'perf')
    """
    # base_url = 'http://ec2-15-164-48-95.ap-northeast-2.compute.amazonaws.com'
    base_url = 'http://obelab-api.com'
    api_uuid = base_url + '/api/analysis/taskuuid/'
    api_raw = base_url + '/api/analysis/metaraw/'
    api_perf = base_url + '/api/analysis/metamarker/'
    print('table access 시작')
    if table == 'uuid':
        return request_to_table(api_uuid, uuid, connect_info[0], connect_info[1])
    elif table == 'raw':
        return request_to_table(api_raw, uuid, connect_info[0], connect_info[1])
    elif table == 'perf':
        return request_to_table(api_perf, uuid, connect_info[0], connect_info[1])


def get_UUID(connect_info, date1 = '2000-01-01', date2 = '2030-01-01'):
    """
        작성자: sjyoo
        작성일: 190612
        기능: date로 아이디 뽑아내기. UUID 뽑을 거임.
        입력: connect_info = list[ID, PASSWORD], 
             시작일, 종료일 = 'yyyy-mm-dd'
        출력: .columns = 'parentUUID', 'taskUUID', 'parentName', 'childName', 'childSex',
                        'childBirth', 'taskCreated', 'taskUpdated', 'snr'
        용례:   base_url = str(SERVER_ADDRESS)
                api_uuid = base_url + str(SERVER_API_ADDRESS)
                get_UUID(접속정보, 시작일-1, 종료일+1)

    """
    base_url = 'http://obelab-api.com'
    api_uuid = base_url + '/api/analysis/taskuuid/'

    uuid = pd.DataFrame()
    r = requests.get(url=api_uuid, auth=HTTPBasicAuth(connect_info[0], connect_info[1]))
    r = r.content.decode("utf-8")
    r = r.split('\n')
    t_head = r.pop(0).split(',')
    t_head[-1] = t_head[-1][0:-1]
    t_body = [t.split(',') for t in r]
    data = pd.DataFrame(t_body, columns=t_head)
    return data.query('taskCreated >= "' + date1 + '" and taskCreated <= "' + date2 +'"')


def server_connect_info():
    """
        작성자: sjyoo
        작성일: 190612
        기능: 접속 정보 ID, Password
        입력: 
        출력: 접속 정보
        용례: my_id = str(ID), my_pw = str(PASSWORD)
        메모: 필요 없는 기능
    """
    my_id = 'admin'
    my_pw = 'obe1234'
    print('접속 정보 받아오기 완료')
    return my_id, my_pw