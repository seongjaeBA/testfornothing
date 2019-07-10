#data input, output
import os
import sys
#split only ㅋ
import re
# 뭐에 쓰드라...
import math
# data 전처리, 분석용
import pandas as pd
import numpy as np
import scipy as sp
from scipy import stats as st
import statsmodels.stats.api as sms

# 서버 requests
import requests
from requests.auth import HTTPBasicAuth
# age 추출
import datetime
from datetime import date
# figure 작업 용
import matplotlib as mpl
import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
#이미지 작업용
import matplotlib.image as mpimg # np.array로 이미지 로드
from PIL import Image # 오브젝트로 로드  -> np.array로 캐스팅


def figure_out_perf(s_data = {}, gtype = 'bar', level = False):
    """
        작성자: sjyoo
        작성일: 190704
        기능: 행동 데이터 figure 추출
        입력: s_data(score 분리 데이터)
        출력: figure(A to Z).png export
        용례: figure_out_perf(s_data, gtype = ['bar', 'stem', 'image 작성중..', 'dist 따로 만들듯...'], 
                                level = boolen(지금은 레벨 점수 적용 여부))
    """
    #폰트 설정
    sns.set(font_scale=0.5)
    mpl.rcParams['axes.unicode_minus'] = False
    path = 'C:/Windows/Fonts/HYSNRL.ttf'
    font_name = fm.FontProperties(fname=path).get_name()
    plt.rc('font', family=font_name)
    
    for task in s_data:
        if 'REST' in task or 'VFT' in task:
            pass
        else:
            s_list = s_data[task].childName.unique()

            for child in s_list:
                s_child = s_data[task][s_data[task].childName == child]
                s_child = s_child.dropna(how = 'any')
                y = s_child['%s_Cor' % task].astype('int')
                y = y.replace(0, -1)
                
                #레벨 적용
                if level == True:
                    LV = [int(lv[2:]) for lv in s_child['%s_LV' % task]]
                    y = np.multiply(LV, y)
                
                fig = plt.figure()
                ax =plt.subplot(111)
                x_name=  s_child['ctime']
                n_groups = len(x_name)
                index = np.arange(n_groups)
                bar_width = 0.35
                opacity = 1
                
                # bar graph
                if gtype == 'bar':
                   

                    ax.bar(index, y.replace(y[y<0], np.nan), alpha=opacity, color='b')
                    ax.bar(index, y.replace(y[y>0], np.nan), alpha=opacity, color='r')
                    ax.set_xlabel('time')
                    ax.set_ylabel('%s_Cor' % task)
                    ax.set_title('%s Bar Chart' % (task))
#                     ax.set_ylim(-3,3)
                    
                    plt.savefig('%s_%s_%s.png' % (child, task, gtype), format = 'png', dpi = 300)
                    plt.show()

                # stem graph    
                elif gtype == 'stem':

                    ax.stem(index, y.replace(y[y<0], np.nan), markerfmt = 'C3o', basefmt = 'r', linefmt='grey')
                    ax.stem(index, y.replacey(y[y>0], np.nan), markerfmt = 'C0o', basefmt= 'r', linefmt='grey' )
                    ax.set_xlabel('time')
                    ax.set_ylabel('%s_Cor' % task)
                    ax.set_title('%s Stem Chart' % (task))
#                     ax.set_ylim(-3,3)
                    
                    plt.savefig('%s_%s_%s.png' % (child, task, gtype), format = 'png', dpi = 300)
                    plt.show()

                # Distribution figure
                elif gtype == 'image':
                    path = os.getcwd()
                    imf = os.path.join(path, 'graphboard.png')

                    image = mpimg.imread(imf)
                    plt.imshow(image)
#                     height, width, layer = image.shape
#                     f, axes = plt.subplots(2, 2, figsize=(8, 8*height/width))
                    ## original img plotting 
#                     axes[0][0].imshow(image[:, :, :]), axes[0][0].axis('off')
#                     axes[0][0].set_xticks([]), axes[0][0].set_yticks([])# 이걸 하지 않으면 tick이 남아있어서 간격이 생김. 
                    # Red, Green, Blue로 구분하여 표현. colormap 또한, 그 형식에 맞춰서 표현 
                    # 실제 그림을 보면 색깔별로 어느 정도 구분되어 있는 것을 알 수 있음. 
#                     cmaps = [plt.cm.Reds, plt.cm.Greens, plt.cm.Blues]
#                     for i in range(1, 4):
#                         axes[i//2][i%2].imshow(image[:, :, i-1], cmap=cmaps[i-1])
#                         axes[i//2][i%2].set_xticks([]), axes[i//2][i%2].set_yticks([])# 이걸 하지 않으면 tick이 남아있어서 간격이 생김. 
#                         axes[i//2][i%2].axis('off')
#                     plt.subplots_adjust(left = 0, bottom = 0, right = 1, top = 1, hspace = 0, wspace = 0)
                    ## sutplots_adjust는 subplot 간에 간격을 붙이려고 쓴건데, 쓰고보니 어떻게 쓰는건지 모르겠음. 그냥 모르겠음...
                    plt.margins(0, 0, tight=False)
                    # pad_inches를 0으로 두고 저장하면, 공백없이 저장됨. 
#                     plt.savefig("../../assets/images/markdown_img/180628_1935_google_rgb.svg", pad_inches=0)
                    plt.show()
                    
                elif gtype == 'dist':

                    a = List[feature].dropna()
                    low = a[a < np.percentile(a, 30)].count()
                    high = a[a > np.percentile(a, 70)].count()
                    middle = a[(a <= np.percentile(a, 70))&(a >= np.percentile(a, 30))].count()

                    points = sns.distplot(a.dropna() 
            #                               , bins = 1000
                                          , fit=sp.stats.norm
                                          , hist =False, kde = True, kde_kws = {'shade' :True, 'kernel' : 'gau'
            #                                                                  , 'bw' : 0.1
                                                                                , 'clip' :(a.min(),a.max()) 
                                                                            }
                                         ).get_lines()[0].get_data()

                    x = points[0]
                    y = points[1]
            #         th = sms.DescrStatsW(a).tconfint_mean(0.0001)[0]
            #         se = sms.DescrStatsW(a).tconfint_mean(0.0001)[1]
                    plt.fill_between(x,y, where = x > np.percentile(a, 75), color='y', alpha=0.7, label = '높음')
                    plt.fill_between(x,y, where = x <  np.percentile(a, 25), color='y', alpha=0.7, label = '낮음')
                    plt.fill_between(x,y, where = (x <=  np.percentile(a, 75)) & (x >= np.percentile(a, 25)), color='b', alpha=0.7, label = '보통')
                    plt.fill_between(x,y, where = (x > np.percentile(a, 90)) &  (x < np.percentile(a, 10)), color='r', alpha=0.7, label = '높음')

            #         hito = plt.hist(a, alpha = 0.5, align  = 'right' )
            #         plt.text(.50, .5, '낮음 = %s , 중간 = %s , 보통 = %s' % (low, middle, high), horizontalalignment='center',
            #      verticalalignment='center',
            #      textcoords = 'axes fraction')
            #         plt.text(x.min(), hito[0].max(), '낮음 = %s , 보통 = %s, 높음 = %s' % (low, middle, high), style='italic',
            #         bbox={'facecolor':'red', 'alpha':0.5, 'pad':10})
            #         plt.annotate('낮음 = %s' % low, xy = (np.percentile(a, 25),np.percentile(a, 25)), xytext=(0.25, 0.5), textcoords = 'axes fraction', arrowprops = dict(color = 'g', alpha= 0.5))
            #         plt.annotate('중간 = %s' % middle, xy = (np.percentile(a, 50),np.percentile(a, 50)), xytext=(0.5, 0.7), textcoords = 'axes fraction', arrowprops = dict(color = 'g', alpha= 0.5))
            #         plt.annotate('높음 = %s' % high, xy = (np.percentile(a, 75),np.percentile(a, 75)), xytext=(0.75, 0.5), textcoords = 'axes fraction', arrowprops = dict(color = 'g', alpha= 0.5))


                    plt.savefig('%s_%s.png' % (feature, gtype), format = 'png', dpi = 1200)
                    plt.show()
    return

def data_scoring(raw = pd.DataFrame(), export = 'f_data'):
    """
        작성자: sjyoo
        작성일: 190704
        기능: 각 행동 데이터 response, index, ctime, taskUUID를 분리하여 코딩
        입력: raw = pd.DataFrame(raw data)
        출력: f_data.xlsx export & figure 용 data
        용례: s_data = data_scoring(list_raw, data, str(export excel file name))
    """
    tasks = {1:'REST',2:'CBTTF',3:'CBTTB',4:'GNG',5:'TWOBACK',6:'STRC',7:'STRI',8:'VFT',9:'REPEAT',10:'MIND',11:'FOLD'}
    GNG_LV = {'LV1':2500, 'LV2': 2250, 'LV3': 2000, 'LV4': 1750, 'LV5': 1500, 'LV6': 1250, 'LV7': 1000, 'LV8': 750, 'LV9': 750, 'LV10': 750, 'LV11': 750, 'LV12': 750} 
    print('scoring data listing 시작')
    s_data = {}
    with pd.ExcelWriter('C:/Users/OBELAB_JH_DESKTOP/Documents/GitHub/testfornothing/OBE/data/'+ export + '.xlsx') as writer:
        for k, v in tasks.items():
            print('key : '+ str(k) + ', value : ' + v)
            s_data[v] = raw[raw['taskType'] == str(k)]
            s_data[v] = s_data[v].replace(['TASKMARKER','OUTTOUCH', 'TASKMARKER\r','OUTTOUCH\r'],[np.nan, np.nan, np.nan, np.nan]).dropna(axis = 1, how = 'all')
            s_data[v].fillna('')
            if 'GNG' in v or 'STRC' in v or 'STRI' in v or 'TWOBACK' in v or 'CBTTF' in v or 'CBTTB' in v or 'MIND' in v or 'REPEAT' in v or 'FOLD' in v:
                LV = []
                Cor = []
                Act = []
                RT =[]
                for ra in s_data[v]['ra']:
                    if pd.isnull(ra) == False:
                        marker = ra.split('/')
                        LV.append(marker[0])
                        Cor.append(marker[1])
                        Act.append(marker[2])
                        RT.append(marker[3])
                    else:
                        marker = ['LV', 'Cor', 'Act', 'RT']
                        LV.append(marker[0])
                        Cor.append(marker[1])
                        Act.append(marker[2])
                        RT.append(marker[3])
                s_data[v]['%s_LV' % v] = LV
                s_data[v]['%s_Cor' % v] = Cor
                s_data[v]['%s_Act' % v] = Act
                s_data[v]['%s_RT' % v] = RT
                print('%s 과제 완료' % v)
            else:
                pass

#             s_data[v] = s_data[v].merge(pack)
            s_data[v].to_excel(writer, sheet_name=v, index = None)
    print('caculate 완료')
    return s_data



def data_merge(List = pd.DataFrame(), raw_data = {}, export = 'merge'):
    """
        작성자: sjyoo
        작성일: 190612
        기능: list와 raw 파일 COR, ACC, RT 등을 merge
        입력: list = pd.DataFrame(), raw_data = dict{}
        출력: merge.xlsx export
        용례: data_merge(list_raw, raw_data, str(export excel file name))
    """
    tasks = {1:'REST',2:'CBTTF',3:'CBTTB',4:'GNG',5:'TWOBACK',6:'STRC',7:'STRI',8:'VFT',9:'REPEAT',10:'MIND',11:'FOLD'}
    GNG_LV = {'LV1':2500, 'LV2': 2250, 'LV3': 2000, 'LV4': 1750, 'LV5': 1500, 'LV6': 1250, 'LV7': 1000, 'LV8': 750, 'LV9': 750, 'LV10': 750, 'LV11': 750, 'LV12': 750} 
    print('merge 시작')
    m_data = {}
    print(m_data)
    m_data = raw_data
    for k, v in tasks.items():
        print('key : '+ str(k) + ', value : ' + v)
        m_data[v] = m_data[v].replace(['TASKMARKER','OUTTOUCH', 'TASKMARKER\r','OUTTOUCH\r'],[np.nan, np.nan, np.nan, np.nan]).T.dropna(axis = 1, how = 'all')
        m_data[v].fillna('')
        pack = pd.DataFrame()
        pack['taskUUID'] = m_data[v].index
        idx = m_data[v].index
        col = m_data[v].columns
        Cor_list = []
        RT = []
        Acc =[]
        Max = []
        
        if 'GNG' in v:
            for i in idx:
                Cor = 0
                LV = 0
                RT_list = []
                LV_list = []
                for j in col:
                    if pd.isnull(m_data[v][j][i]) == False:
                        marker = m_data[v][j][i].split('/')
                        if 'LV' in marker[0]:
                            Cor += int(marker[1])
                            LV += 1
#                             print(marker[0][2:])
                            LV_list.append(marker[0][2:])
                            if '1-1' in marker[2]:
                                if 'LV' in marker[3]:
                                    pass
                                else:
                                    if [int(marker[3]) < t for l, t in GNG_LV.items() if marker[0] == l]:
                                        RTint = int(marker[3])
                                        RT_list.append(RTint)
                        else:
                            pass
                    else:
                        pass
                print(LV_list)
                Max.append(max(LV_list))
                Cor_list.append(Cor)
                if len(RT_list) is not 0:
                    RT.append(sum(RT_list) / len(RT_list))
                else:
                    RT.append(0)
                
                if LV == 0:
                    Acc.append(0)
                else:
                    Acc.append(Cor/LV)
                
            pack['%s_Cor' % v] = Cor_list
            pack['%s_RT' % v] = RT
            pack['%s_ACC' % v] = Acc
            pack['%s_max' % v] = Max
            print('정답률, 반응시간')
            print('과제 완료')
        
        elif 'STRC' in v or 'STRI' in v:
            for i in idx:
                Cor = 0
                LV = 0
                RT_list = []
                for j in col:
                    if pd.isnull(m_data[v][j][i]) == False:
                        marker = m_data[v][j][i].split('/')
                        if 'LV' in marker[0]:
                            Cor += int(marker[1])
                            LV += 1
                            if marker[1] == '1':
                                if 'LV' in marker[3]:
                                    pass
                                else:
                                    if int(marker[3]) < 2000 :
                                        RTint = int(marker[3])
                                        RT_list.append(RTint)
                        else:
                            pass
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
                
            pack['%s_Cor' % v] = Cor_list
            pack['%s_RT' % v] = RT
            pack['%s_ACC' % v] = Acc
            print('정답률, 반응시간')
            print('과제 완료')
            
        elif 'TWOBACK' in v:
            for i in idx:
                Cor = 0
                LV = 0
                RT_list = []
                for j in col:
                    if pd.isnull(m_data[v][j][i]) == False:
                        marker = m_data[v][j][i].split('/')
                        if 'LV' in marker[0]:
                            Cor += int(marker[1])
                            LV += 1
                            if '1-1' in marker[2]:
                                if 'LV' in marker[3]:
                                    pass
                                else:
#                                 if int(marker[3]) < 2000 :
                                    RTint = int(marker[3])
                                    RT_list.append(RTint)
                        else:
                            pass
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
                
            pack['%s_Cor' % v] = Cor_list
            pack['%s_RT' % v] = RT
            pack['%s_ACC' % v] = Acc
            print('정답률, 반응시간')
            print('과제 완료')
            
            
        elif 'CBTTF' in v or 'CBTTB' in v or 'MIND' in v or 'REPEAT' in v or 'FOLD' in v:
            for i in idx:
                Cor = 0
                LV = 0
                LV_list = []
                for j in col:
                    if pd.isnull(m_data[v][j][i]) == False:
                        marker = m_data[v][j][i].split('/')
                        if 'LV' in marker[0]:
                            Cor += int(marker[1])
                            LV += 1
#                             print(marker[0])
                            LV_list.append(marker[0][2:])
                        else:
                            pass
                    else:
                        pass
                print(LV_list)
                if not LV_list:
                    Max.append(1)
                else:
                    Max.append(max(LV_list))
                Cor_list.append(Cor)
                if LV == 0:
                    Acc.append(0)
                else:
                    Acc.append(Cor/LV)
#             print(pack)
#             print(Cor_list)
            pack['%s_Cor' % v] = Cor_list
            pack['%s_ACC' % v] = Acc
            pack['%s_max' % v] = Max
            print('정답률')
            print('과제 완료')
            
        else:
            print('pass')
            pass
        
#         print(List)
        List = List.merge(pack, on='taskUUID', how = 'outer')
    List['GNG_z'] = List['GNG_ACC'] / List['GNG_RT']*1000
    List['STRC_z'] =  List['STRI_ACC'] / List['STRI_RT']*1000
    List['STRI_z'] =  List['STRC_ACC'] / List['STRC_RT']*1000
    List['STRE'] =  List['STRC_RT'] - List['STRI_RT']*1000
    List['STRE_z'] =  List['STRI_z'] - List['STRC_z']
    List.to_excel(export + '.xlsx', sheet_name = 'data')
    print('caculate 완료')
    return List
    
def raw_to_data(raw):
    """
        작성자: sjyoo
        작성일: 190611
        기능: table을 분석용 dict로 내보내기
        입력: raw table(dataframe)
        출력: raw_data = dict{pd.DataFrame{task pivot)}
        용례: raw_data = raw_to_data(pandas DataFrame(raw))
        메모: 데이터에 따라 pivot/pivot_table 조절
    """
    tasks = {1:'REST',2:'CBTTF',3:'CBTTB',4:'GNG',5:'TWOBACK',6:'STRC',7:'STRI',8:'VFT',9:'REPEAT',10:'MIND',11:'FOLD'}
    task_num = raw['taskType'].unique()
    raw_data = {}
    for task in tasks.values():
        raw_data[task]= pd.DataFrame()
#     print(raw)
    for k in task_num:
        task_ind = raw.query('taskType == "' + k +'"')
#         print(task_ind)
        # data = task_ind.pivot(columns = 'childName', values = 'raw')
        # data = pd.pivot_table(task_ind, index = 'index', columns = 'childName', values = 'raw', aggfunc=np.sum, margins = True)
        raw_data[tasks[int(k)]] = pd.pivot_table(task_ind, index = 'index', columns = 'taskUUID', values = 'ra', aggfunc=np.sum)
        print('%s  실행' % k)
    return raw_data

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
#     list_raw = pd.DataFrame()
    print('table 요청 시작')
    for child in uuid:
        print(child + '_로딩 중....')
        url_uuid = url + '?taskUUID=' + child
        r = requests.get(url=url_uuid, auth=HTTPBasicAuth(my_id, my_pw))
        r = r.content.decode("utf-8")
        r = re.split('\n|\r', r)
        t_head = r.pop(0).split(',')
        t_head[-1] = t_head[-1][0:-1]
        t_body = [t.split(',') for t in r if t != '']
        full = pd.DataFrame(t_body, columns=t_head)
        full = full[full.taskUUID != '']
        tasks = full['taskType'].unique()
        for task in tasks:
            task_raw = full.query('taskType == "' + str(task) +'"')
            mx = task_raw.taskSubID.max()
            if mx != '':
                t_mx_raw = task_raw.query('taskSubID == "'+str(mx)+'"')
                raw = pd.concat([raw, t_mx_raw], axis=0)
        print('%s 완료' % child)
#     list_raw['name'] = raw['childName']
#     list_raw['uuid'] = raw['taskUUID']
#     list_raw = list_raw.drop_duplicates(keep = 'last')
    print("raw export 완료")
#     return raw, list_raw
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
    print('table access 시작')
    if table == 'uuid':
        return request_to_table(api_uuid, uuid, connect_info[0], connect_info[1])
    elif table == 'raw':
        return request_to_table(api_raw, uuid, connect_info[0], connect_info[1])
    elif table == 'perf':
        return request_to_table(api_perf, uuid, connect_info[0], connect_info[1])
    print("raw 완료")


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
    r = re.split('\n|\r', r)
    t_head = r.pop(0).split(',')
    t_head[-1] = t_head[-1][0:-1]
    t_body = [t.split(',') for t in r]
    data = pd.DataFrame(t_body, columns=t_head)
    data = data.query('taskCreated >= "' + date1 + '" and taskCreated <= "' + date2 +'"')
    pack = []
    for b, c in zip(data.childBirth, data.taskCreated):
        birth = datetime.datetime.strptime(b, '%Y/%m/%d')
        testdate = datetime.datetime.strptime(c, '%Y-%m-%d %H:%M:%S.%f+00:00')
        ag = testdate.year - birth.year
        pack.append(ag)
    data['age'] = pack
    data.pop('sn')
    data = data.drop_duplicates(keep = 'last')
    return data


def server_connect_info():
    my_id = 'admin'
    my_pw = 'obe1234'

    return my_id, my_pw

if __name__ =="__main__":
    connect_info = server_connect_info()
    list_raw = get_UUID(connect_info, '2019-06-28', '2019-07-01')
    # print(list_raw)
    target_child = list_raw.taskUUID
    # target_child = ['HgwQ9iNB', 'vnTJNL39']
    # print(target_child)
    raw = access_to_table(connect_info = connect_info, uuid=target_child, table = 'perf') #한예준
    # raw_data = raw_to_data(raw)
    # List = data_merge(list_raw, raw_data, 'Result_07_5')
    s_data = data_scoring(raw, 'scoring')
    figure_out_perf(s_data)