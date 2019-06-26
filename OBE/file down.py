import os
import datetime
import requests
import math
import pandas as pd
import numpy as np
from requests.auth import HTTPBasicAuth
# from datetime import date
# from datetime import datetime


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

    path = os.getcwd()
    print(path)
    # file = os.path.join(path, "data", 'sj_perforamance.xls')
    f1 = os.path.join(path, "OBE/data", raw_file + '.xlsx')
    f2 = os.path.join(path, "OBE/data", WJ_list + '.xlsx')
    List = pd.read_excel(open(f2, 'rb'), header=0)

    for i in range(len(task_list)):
        Task[task_list[i]] = pd.read_excel(open(f1, 'rb'), sheet_name = '%s' % task_list[i], header=None).T.dropna(how = 'all')
        Task[task_list[i]] = pd.DataFrame.from_dict(Task[task_list[i]])
        Task[task_list[i]] = Task[task_list[i]].replace(['TASKMARKER','OUTTOUCH','TASKMARKER\r','OUTTOUCH\r'],[np.nan, np.nan, np.nan, np.nan]).dropna(axis = 1, how = 'all')
        Task[task_list[i]] = Task[task_list[i]].fillna('damm')
        


    for task in task_list:
        pack = pd.DataFrame(Task[task][0])
        idx = Task[task].index
        # print(idx)
        # print(col)
        col = Task[task].columns
        if 'GNG' in task or 'TWOBACK' in task or 'STRC' in task or 'STRI' in task  or 'FOLD' in task:
            Cor_list = []
            RT = []
            Acc =[]
            for i in idx:
                Cor = 0
                LV = 0
                RT_list = []
                for j in col:
                    if Task[task][j][i] == 'damm':
                        pass
                    else:     
                        marker = Task[task][j][i].split('/')
                    if 'LV' in marker[0]:
                        Cor += int(marker[1])
                        LV += 1
                    else:
                        continue
                
                    if int(marker[3]) < 2000 :
                        if '1-1' in marker[2]:
                            RTint = int(marker[3])
                            RT_list.append(RTint)
                Cor_list.append(Cor)
                if len(RT_list) is not 0:
                    RT.append(sum(RT_list) / len(RT_list))
                else:
                    RT.append(0)
                
                Acc.append(Cor/LV)
                
            pack['%s_Cor' % task] = Cor_list
            pack['%s_RT' % task] = RT
            pack['%s_ACC' % task] = Acc
    
            print(task)
            print('정답률, 반응시간')
            
            
        elif 'CBTTF' in task or 'CBTTB' in task or 'MIND' in task or 'REPEAT' in task:
            Cor_list = []
            for i in idx:
                Cor = 0
                LV = 0
                for j in col:
                    if Task[task][j][i] == 'damm':
                        pass
                    else:
                        marker = Task[task][j][i].split('/')
                    
                    if 'LV' in marker[0]:
                        Cor += int(marker[1])
                        LV += 1
                    else:
                        continue

                Cor_list.append(Cor)

            ACC_list = [x / LV for x in Cor_list]
            pack['%s_Cor' % task] = Cor_list
            pack['%s_ACC' % task] = ACC_list
            
            print(task)
            print('정답률')
            
        else:
            print(task)
            print('pass')
            pass
        List = List.merge(pack, left_on='name', right_on=0 , how = 'outer')

    List.pop('0_x')
    List.pop('0_y')
    List.to_excel(merge + '.xlsx')
    print('완료')
    return
    
def raw_to_LVAn(raw):
    marker = raw[raw].split('/')
    print(marker)
    # level_anlaysis = raw.pivot(columns = 'childName', values = 'raw')
    return

def raw_to_data(raw, output = 'output'):
    """
        작성자: sjyoo
        작성일: 190611
        기능: table을 분석용 파일로 내보내기(data.to_csv(sj_performance))
        입력: raw table(dataframe), output = export data name
        출력: excel file('C:/Users/OBELAB_JH_DESKTOP/Documents/GitHub/testfornothing/OBE/data/xxxx.xlsx)
        용례: data = raw_to_data(pandas DataFrame(raw), str(output))
    """
    task_num = raw['taskType'].unique()
    tasks = {1:'REST',2:'CBTTF',3:'CBTTB',4:'GNG',5:'TWOBACK',6:'STRC',7:'STRI',8:'VFT',9:'REPEAT',10:'MIND',11:'FOLD'}
    
    with pd.ExcelWriter('C:/Users/OBELAB_JH_DESKTOP/Documents/GitHub/testfornothing/OBE/data/'+ output + '.xlsx') as writer:
        for task in task_num:
            task_ind = raw.query('taskType == "' + task +'"')
            # data = task_ind.pivot(columns = 'childName', values = 'raw')
            data = pd.pivot_table(task_ind, index = 'index', columns = 'childName', values = 'raw', aggfunc=np.sum)
            data.to_excel(writer, sheet_name=tasks[int(task)], index = None)
    return 

def request_to_table(url, uuid, my_id, my_pw):
    """
        작성자: cmlee
        수정자: sjyoo
        작성일: 190509
        수정일: 190611 
        기능: 요청 정보를 이용해서 서버에서 데이터 테이블 형태로 반환
        입력: url, id, pw, taskuuid
        출력: pandas DataFrame : header + contents
        용례: raw = request_to_table(str(api_url), str(uuid)/ list(uuid), str(my_id), str(my_pw))
    """
    raw = pd.DataFrame()
    print('table 요청 시작')
    for child in uuid:
        print('%s 시작' % child)
        url_uuid = url + '?taskUUID=' + child
        r = requests.get(url=url_uuid, auth=HTTPBasicAuth(my_id, my_pw))
        r = r.content.decode("utf-8")
        r = r.split('\n')
        t_head = r.pop(0).split(',')
        t_head[-1] = t_head[-1][0:-1]
        t_body = [t.split(',') for t in r for t in r if t != '']
        data = pd.DataFrame(t_body, columns=t_head)
        data = data[data.taskUUID != '']
        raw = pd.concat([data, raw], axis=0)
        print('%s 완료' % child)
    print("raw export 완료")
    return raw

def access_to_table(connect_info, uuid, table = 'uuid'):
    """
        작성자: sjyoo
        작성일: 190611
        기능: table 접속
        입력: connect_info: id, pw; uuid = taskuuid; table = 받고 싶은 데이터 table
        출력: pandas DataFrame : 현재는 performance 
        용례: raw = access_to_table(connect_info, uuid, table = 'uuid'&'raw'&'perf')
    """
    # base_url = 'http://ec2-15-164-48-95.ap-northeast-2.compute.amazonaws.com'
    base_url = 'http://obelab-api.com'
    api_uuid = base_url + '/api/analysis/taskuuid/'
    api_raw = base_url + '/api/analysis/metaraw/'
    api_perf = base_url + '/api/analysis/metamarker/'

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
        입력: 접속 정보, 시작일, 종료일
        출력: uuid 리스트
        용례: get_UUID(접속정보, 시작일, 종료일)
    """
    base_url = 'http://obelab-api.com'
    api_uuid = base_url + '/api/analysis/taskuuid/'

    uuid = pd.DataFrame()
    #지금은 다 불러와서 date로 filtering
    r = requests.get(url=api_uuid, auth=HTTPBasicAuth(connect_info[0], connect_info[1]))
    r = r.content.decode("utf-8")
    r = r.split('\n')
    t_head = r.pop(0).split(',')
    t_head[-1] = t_head[-1][0:-1]
    t_body = [t.split(',') for t in r]
    data = pd.DataFrame(t_body, columns=t_head)
    return data.query('taskCreated >= "' + date1 + '" and taskCreated <= "' + date2 +'"')

def server_connect_info():
    my_id = 'admin'
    my_pw = 'obe1234'

    return my_id, my_pw


if __name__ == "__main__":
    '''
        data_merge 에서 주소 수정하여 사용할 것.
        wj_list를 받을 방법도 생각할 것.
        용례 적어둘 것.
    '''
    connect_info = server_connect_info()
    p_list = get_UUID(connect_info, '2019-05-24', '2019-06-10')
    # print(p_list)
    target_child = p_list.taskUUID
    # print(target_child)
    # target_child = ['ETMt9ghG'] 
    # target_child = ['ETMt9ghG', '4cCiSclJ', 'DTYMwUxL', 'QtKK7sCe', 'mZrzoY7s', 'byNKiAgk', 'zAQDxtWQ', 'i0FQPTiI', 
    # 'eJURms0y', 'rKkMbuyf', '0FAE54zl', 'YFF4zQ1e', 'PEapshgr', '6hD3Z95T', 'FzF7DQcB', 'KO6fD1ut', 'VJBd04EA', '5I783px6', 'AqQKUZpj', 'B48dNhx8',
    # 'W0UGkIyx', 'xZ7fS5mu', 'Y7yIkcbO', 'H7Ei5cjf', 'PqNn2Db6']
    print('명단 완료')
    raw = access_to_table(connect_info = connect_info, uuid=target_child, table = 'perf') #한예준
    # print(raw)
    # SaveData.raw_to_LVAn(raw)
    raw_to_data(raw, 'output')
    
    data_merge('wj_list', 'output', 'Result')
