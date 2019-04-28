"""
    작성자: cmlee
    작성일: 190320
    기능: 데이터 입출력을 담당하는 구조를 모두 저장
    구조:
        DatabaseInfo :: database 관련정보 모음
        FeatureNIRSIT :: 개별 건당 target 구역의 feature 추출 모음
        DataSpec :: Spec 관련 설정 및 상수 모음
        DataNIRSIT :: 개별 건당 NIRSIT data 처리를 위한 구조체
    용례:
        import dataIO
        ...
        dataIO.DataSpec()
        dataIO.DataNIRSIT()
"""

import pandas as pd
import exceptions as exc
import psycopg2 as pg2
import numpy as np
import pickle
import gzip
import os


# TODO: Analysis 부분 class 작성 요망
class AnalysisNIRSIT:
    def __init__(self):
        pass


# TODO: feature 부분 class 작성 요망
class BlockAverageFeatures:
    def __init__(self):
        self.value = []


class ConnectivityFeatures:
    def __init__(self):
        self.name_list = {}


class FeatureNIRSIT:
    """
    작성자: cmlee
    작성일: 190322 작성중
    기능: 입력 데이터(가공된)를 지정된 feature space 로 변환하여 저장하는 클래스
    입력:
        #ch x #Frame 입력
    출력:
        instance with features
    용례:
        self.spec = FeatureNIRSIT()
        ...

    """
    def __init__(self):
        self.block_feature = BlockAverageFeatures()
        self.conn_feature = ConnectivityFeatures()

    def about(self):
        print("summary info 작성 요망" + str(self.__dict__))


class DataServer:
    """
        작성자: cmlee
        작성일: 190319
        기능: DB 정보를 기록하고 CRUD 를 진행하는 class
        입력:
            없음
        출력:
            DB 관련 정보
        용례:
            self.dbinfo = DatabaseInfo()
            ...
    """
    def __init__(self):
        self.db_name = "test"
        self.db_user = "postgres"
        self.db_password = "obelab1234"
        self.host_address = "0.0.0.0:8080"
        self.host_port = "5432"
        self.conn = None
        self.cur = None

    def set_params(self, name, user, password, address, port):
        # set another term
        self.db_name = name
        self.db_user = user
        self.db_password = password
        self.host_address = address
        self.host_port = port

    def connect_query(self):
        try:
            self.conn = pg2.connect(database=self.db_name,
                                    user=self.db_user,
                                    password=self.db_password,
                                    host=self.host_address,
                                    port=self.host_port)
            # autocommit 없으면, InternalError: CREATE DATABASE cannot run inside a transaction block
            self.conn.autocommit = True
            self.cur = self.conn.cursor()
        except Exception:
            raise exc.DataServerGetException('잘못된 서버 설정입니다')

    def disconnect_query(self):
        self.cur.close()
        self.conn.close()

    def select_query(self, query_str):
        # query_str = "SELECT " + args + " FROM " + table_name
        self.cur.execute(query_str)
        rows = self.cur.fetchall()
        return rows

    def insert_query(self, query_str):
        # query_str = INSERT INTO some_table (an_int, a_date, a_string)
        # ...     VALUES (%s, %s, %s);
        # ...     """,
        # ...     (10, datetime.date(2005, 11, 18), "O'Reilly")
        self.cur.execute(query_str)
        self.conn.commit()


class NestedDictInit(dict):
    """
    nested dict without initialization
    dict 에서 key 값 없이 일단 선언해서 쓸 수 있는 형태
    Blocknize 에서 사용
    """
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value


class DataMotion:
    """
    작성자: cmlee
    작성일: 190319
    기능: MBLL 결과에 대한 HbO, HbR, HbT
    입력:
        instance 생성시, 무조건 init value 로 HbO, HbR, HbT 칸 만들어줌
    출력:
        empty HbO, HbR, HbT elements
    용례:
        self.mbll = dataHbX()
        ...

    """

    def __init__(self):
        self.ang_x = None
        self.ang_y = None
        self.ang_z = None
        self.motion_thd = None


class DataHbX:
    """
    작성자: cmlee 
    작성일: 190319
    기능: MBLL 결과에 대한 HbO, HbR, HbT
    입력:  
        instance 생성시, 무조건 init value 로 HbO, HbR, HbT 칸 만들어줌
    출력:
        empty HbO, HbR, HbT elements
    용례:
        self.mbll = dataHbX()
        ...
        
    """
    def __init__(self):
        self.HbO = None
        self.HbR = None
        self.HbT = None


class DataLambda:
    """
    작성자: cmlee 
    작성일: 190319
    기능: 데이터 중 다파장 정보를 가지는 경우에 대한 처리 
    입력:  
        instance 생성시, 무조건 init value 로 d780,850 칸만 만들어줌
    출력:
        empty d780, d850 elements
    용례:
        self.raw = dataRaw() 
        self.dOD = dataRaw()
        self.MdOD = dataRaw()
        ...
        
    """
    def __init__(self):
        self.d780 = None
        self.d850 = None


class DataRaw:
    """
    작성자: cmlee 
    작성일: 190319
    기능: NIRSIT / NIRSIT2 의 데이터 값을 관리하는 class
    입력:  
        instance 생성시에 기본 설정값을 가지고
        set_data 를 통해 input 을 넣어준다
    출력:
        NIRSIT data instance
    용례: 
        my_data = dataNIRSIT()
        my_data.set_data('id:1350','server') or 'C:/~~''csv'
        my_data.send_data(id:1350','server') or 'C:/~~''csv'
        my_data.set_meta_information(id_num, name, sex, age, inspector, date)
        spec = DataSpec()
        my_data.set_performance(acc, rt, task_name, spec)
        my_data.set_task_block(self, spec)
    """
    num_data = 0

    def __init__(self):
        # 기기 측정 관련 data 모음
        self.timestamp = None
        self.raw = DataLambda()
        self.dOD = DataLambda()
        self.mbll = DataHbX()
        self.snr_map = DataLambda()
        self.mod_mbll = DataHbX()
        self.mod_clustered_mbll = DataHbX()
        self.block_rej = []
        # TODO: 이후에 spike removal, motion artifact removal 추가 작업 때 늘려주자

        # 행동관련 데이터 
        self.accel = []
        self.gyro = []
        self.motion = DataMotion()

        # channel rejection 
        self.ch_rej = []

        # 그 외 정보
        self.battery = []
        
        # raw string input 
        self.snr_calibration = []  # 없을 수도 있음. 구형 모델에서는 없었음

    def set_value(self, timestamp, raw780, raw850, accel, gyro):
        self.timestamp = timestamp
        self.raw.d780 = raw780
        self.raw.d850 = raw850
        self.accel = accel
        self.gyro = gyro


class DataMeta:
    # 기본 meta information

    def __init__(self):
        self.id_num = None
        self.name = None
        self.sex = None
        self.age = None
        self.inspector = None
        self.date = None
        self.task_name = None

    def set_value(self, id_num, name, sex, age, inspector, date, task_name):
        self.id_num = id_num
        self.name = name
        self.sex = sex
        self.age = age
        self.inspector = inspector
        self.date = date
        self.task_name = task_name


class DataPerformance:
    def __init__(self):
        self.perf_accuracy = None
        self.perf_reaction_time = None

    def set_value(self, acc, rt):
        self.perf_accuracy = acc
        self.perf_reaction_time = rt


class DataTask:
    def __init__(self):
        self.marker = None
        self.ndata = 0
        self.task_block = None

    def set_value(self, marker):
        self.marker = marker
        self.ndata = self.marker.shape[0]
        self.task_block = self.set_task_block()

    def set_task_block(self):
        # 신호 길이가 너무 짧으면 잘못된것으로 보고 자름
        # 1 = rest 의 경우 마커가 없으므로, 전체 구간에 대해 잡도록 설정되어 있ㅇ므
        # 2 = 마커가 1개인 경우, 임의의 시작지점에서 마커 위치까지
        # 3 = 마커가 2개 이상일 경우, 90 보다 큰 경우는 start, end 로 생각해서 버림

        # markers 정보로 부터 task_block 을 생성하는 부분
        marker = self.marker

        # size check
        gap_size = round(DataSpec.FS * 15)
        if gap_size > marker.shape[0] - gap_size:
            self.task_block = []
            raise exc.DataIOException('신호 길이가 너무 짧습니다 확인해주세요')

        else:
            non_zero_index = np.where(marker != 0)[0]

            if len(non_zero_index) == 0:
                # rest 와 같이 신호입력은 있는데 마커 정보가 아예 없는 경우
                self.task_block = [(0, gap_size, marker.shape[0] - gap_size)]
            elif len(non_zero_index) == 1:
                # 마커가 한개만 박혀있는 경우.. ???
                markers = marker[non_zero_index]
                self.task_block = [(0, gap_size, markers[0])]
                raise exc.DataIOException('마커가 하나뿐임.. 코드 확인필요')
            else:
                # 마커가 존재하는 경우
                markers = marker[non_zero_index]
                marker_dict = np.c_[markers.values, markers.index]
                task_block = []
                for i in range(marker_dict.shape[0] - 1):
                    if marker_dict[i + 1, 0] < 90:
                        marker_name = marker_dict[i + 1, 0]
                        marker_start = marker_dict[i, 1]
                        marker_end = marker_dict[i + 1, 1]
                        curr_task_block = [marker_name, marker_start, marker_end]
                        if i == 0:
                            task_block = curr_task_block
                        else:
                            task_block = np.vstack((task_block, curr_task_block))

                self.task_block = task_block

    def set_task_block2(self):
        # TODO: task block 정의에 따라 변경 요망.. 대충돌아가게만 해둠
        """
            정의 : 1234 구조의 네자리 마커를 받아 와서 사용하기로함
            X 는 마커의 종류
            YY는 task 번호(두자리까지 지원)  = 00, 01, 02,... 99 등 구분시 필요한 다양한 번호 지원(ex. congruent vs in-congruent 구분 등)
            Z는 상태번호 = 0:시작, 1:끝, 2: event-related marker,  3~9는 이후 필요시 할당
            1000번 계열(signal 구조 관련) =  1000: 00번 task 를 시작함. 1001: 00번 task 가 끝남
            2000번 계열(task 계열)
            3000번 계열(ctrl 계열)
            5000번 계열 (rest 계열)
            9000번 계열(custom marker)
            빈자리는 이후 필요에 의해 채우되, 분석 툴 처리 원칙을 고지하고 이에 맞게 넣을 수 있게 고정
            # 예시. VFT =  1000(시작) - 5000- 5001-3000-3001-2000-2001 - ....반복 .... 1001 (종료)
        """
        marker = np.array(self.marker)

        # marker 정의 check.
        # TODO: 단 Event design 일 경우 확정되면 수정이 필요함
        # gap_size = round(DataSpec.FS * 15)
        gap_size = 0

        length_markers = marker.shape[0]
        if gap_size > length_markers - gap_size:
            raise exc.DataIOException('마커 정의에 어긋납니다.')

        non_zero_index = np.where(marker != 0)[0]
        if len(non_zero_index) <= 1:
            raise exc.DataIOException('마커 정의에 어긋납니다.')
        else:
            markers = marker[non_zero_index]
            values = markers
            indexes = non_zero_index
            list_new_val = []
            list_new_index = []
            if (values[0] != 1000) or (values[-1] != 1001):
                raise exc.DataIOException('마커 정의에 어긋납니다.')
            else:
                on_task = False
                for i in range(0, values.shape[0]):
                    if i == 0:
                        list_new_val.append(values[i])
                        list_new_index.append(indexes[i])
                        on_task = False
                    elif i == length_markers - 1:
                        list_new_val.append(values[i])
                        list_new_index.append(indexes[i])
                        on_task = False
                    else:
                        if (not on_task) and (values[i] % 1000 == 0):
                            on_task = True
                            list_new_val.append(values[i])
                            list_new_index.append(indexes[i])
                        elif (not on_task) and (values[i] % 1000 != 0):
                            raise exc.DataIOException('마커 정의에 어긋납니다.')
                        elif on_task and (values[i] % 1000 == 1):
                            on_task = True
                            list_new_val.append(values[i - 1] + 1)
                            list_new_index.append(indexes[i] - 1)
                            list_new_val.append(values[i])
                            list_new_index.append(indexes[i])

                marker_dict = np.c_[list_new_val, list_new_index]

                task_block = []
                for i in range(1, marker_dict.shape[0] - 1):
                    if marker_dict[i + 1, 0] >= 2000:
                        marker_name = marker_dict[i, 0]
                        marker_start = marker_dict[i, 1]
                        marker_end = marker_dict[i + 1, 1]
                        curr_task_block = [marker_name, marker_start, marker_end]
                        if i == 1:
                            task_block = curr_task_block
                        else:
                            task_block = np.vstack((task_block, curr_task_block))

                self.task_block = task_block


class DataSpec:
    """
    작성자: cmlee
    작성일: 190319
    기능: 데이터 처리에 사용되는 spec 값들
    입력:
        instance 생성시, 실험에 사용되는 모든 상수 및 조건 값들을 저장함
    수정:
        # TODO: diffusion coefficient 설정하는 경우에 대한 부분 설정 필요 makejson.m 869번줄 참조
        ndata 설정을 task_manager 로 넘김
    출력:
        empty spec elements
    용례:
        self.spec = DataSpec()
        ...

    """
    # 확정 변수에 한해서 Class variable 로 등록해버리자
    FS = 8.138
    SMALL_CONST = 1e-6
    BPF = [0.1, 0.005]
    FRAME_UNIT = True  # Frame 단위로 볼 것인지, sec 단위로 볼 것인지

    def __init__(self):
        self.NCH = 68  # 총 수
        self.CH = 48  # 사용하는 채널 수
        self.SNR_THD = 30
        self.ZSCR_THD = 0.1
        self.ZSCR_THD2 = 1

        # about diffusion coefficient
        index_distance = [68, 120, 156, 204]
        r = [3, 1.5, 2.12, 3.35]
        r_mat = []
        for i in range(len(r)):
            r_mat = np.append(r_mat, np.kron(np.ones([index_distance[i], 1]), r[i]))
        self.r = r_mat
        dpf780 = 5.075
        dpf850 = 4.640
        self.dpf780 = np.kron(np.ones([self.NCH, 1]), dpf780)
        self.dpf850 = np.kron(np.ones([self.NCH, 1]), dpf850)
        extinc_coeff = 1 / 0.4343 * np.array([[0.763, 1.066], [1.097, 0.781]])
        inv_extinc_coeff = np.linalg.inv(extinc_coeff)
        self.inv_extinc_coeff = np.kron(np.ones([self.NCH, 1]), inv_extinc_coeff.reshape(4))

        # about Motion dOD
        self.DOD_S = 10
        self.DOD_E = 15
        self.DOD_N = 10
        self.DOD_SPK_WIN = 10
        self.DOD_XCORR_THD = 0.6
        self.DOD_ACCEL_THD = 1.8
        self.DOD_GYRO_THD = 1.8
        self.DOD_ENV_WIN = 100
        self.MOV_N = 8

        # Brodmann padding Index Dict
        RDPC = [1, 2, 3, 5, 6, 11, 17, 18]
        RVPC = [4, 9, 10]
        RFPC = [7, 8, 12, 13, 21, 22, 25, 26]
        ROFC = [14, 15, 16, 29, 30]
        LDPC = [19, 20, 33, 34, 35, 38, 39, 43]
        LVPC = [40, 44, 45]
        LFPC = [23, 24, 27, 28, 36, 37, 41, 42]
        LOFC = [31, 32, 46, 47, 48]
        RALL = RDPC + RVPC + RFPC + ROFC
        LALL = LDPC + LVPC + LFPC + LOFC
        WHOLE = RALL + LALL
        self.BRODMANN_PAD_LIST = dict()
        self.BRODMANN_PAD_LIST['brodmann1'] = RDPC
        self.BRODMANN_PAD_LIST['brodmann3'] = RVPC
        self.BRODMANN_PAD_LIST['brodmann5'] = RFPC
        self.BRODMANN_PAD_LIST['brodmann7'] = ROFC
        self.BRODMANN_PAD_LIST['brodmann2'] = LDPC
        self.BRODMANN_PAD_LIST['brodmann4'] = LVPC
        self.BRODMANN_PAD_LIST['brodmann6'] = LFPC
        self.BRODMANN_PAD_LIST['brodmann8'] = LOFC
        self.BRODMANN_PAD_LIST['right'] = RALL
        self.BRODMANN_PAD_LIST['left'] = LALL
        self.BRODMANN_PAD_LIST['all'] = WHOLE

        # about tasks
        self.BLOCK_NAMES = ['rest1', 'ctrl1', 'task1', 'rest2', 'ctrl2', 'task2', 'rest_avg', 'ctrl_avg', 'task_avg']
        self.TASK_NAMES = ['REST', 'CBTTF', 'CBTTB', 'GNG', 'TWOBACK', 'STROOP', 'VFT']
        self.BLOCK_DURATION = {'CBTTF': {'rest1': 30, 'task1': 60, 'rest2': 60, 'task2': 60},
                               'CBTTB': {'rest1': 30, 'task1': 60, 'rest2': 60, 'task2': 60},
                               'GNG': {'rest1': 30, 'task1': 30, 'rest2': 30, 'task2': 30},
                               'TWOBACK': {'rest1': 30, 'task1': 30, 'rest2': 30, 'task2': 30},
                               'STROOP': {'rest1': 30, 'task1': 30, 'rest2': 30, 'task2': 30},
                               'VFT': {'rest1': 30, 'ctrl1': 30, 'task1': 30, 'rest2': 30, 'ctrl2': 30, 'task2': 30},
                               'REST': {'rest1': 90}
                               }

        # about connectivity
        self.CON_CORR_THD = 0.5
        self.CON_EDGE_MEASURE_OPT = 'Spearman'  # 'Pearson'
        self.CON_CW2CL_OPT = 'log'  # 'inv'


class DataNIRSIT:
    """
        작성자: cmlee
        작성일: 190416
        기능: NIRSIT_v1 신호 가공에 필요한 최상위 클래스 (sub_class 의 조합으로 생성)
        입력:
            DataRaw, meta_info, performance, task_manager, spec, memo
        수정:
            # TODO: NIRSIT2 의 경우는 DataNIRSIT_v2, DataSpec_v2 로 선언하여 사용
            # class 별 입력 제어 하는 부분 추가 필요
        출력:
            empty spec elements
        용례:
            self.spec = DataSpec()
            ...
    """
    def __init__(self,
                 measure=DataRaw(),
                 meta_info=DataMeta(),
                 performance=DataPerformance(),
                 task_manager=DataTask(),
                 spec=DataSpec(),
                 memo=''):
        self.measure = measure
        self.meta_info = meta_info
        self.performance = performance
        self.task_manager = task_manager
        self.spec = spec
        self.memo = memo

        # save / load data
        self.save_default_extension = '.pickle'

    # TODO: 미완. 다른 부분 어떻게 받아올 것인지 지정이 필요함
    def set_components(self, timestamp, raw780, raw850, accel, gyro,
                       id_num, name, sex, age, inspector, date, task_name,
                       acc, rt,
                       marker,
                       memo):
        self.measure.set_value(timestamp, raw780, raw850, accel, gyro)
        self.meta_info.set_value(id_num, name, sex, age, inspector, date, task_name)
        self.performance.set_value(acc, rt)
        self.task_manager.set_value(marker)
        self.memo = memo

    # TODO: getattr future deprecated 문제 있음
    def save_data(self, save_name='save'):
        # data = dict_from_class(self)
        # save
        default_extension = self.save_default_extension
        filename, file_extension = os.path.splitext(save_name)
        # check file name
        if file_extension != default_extension:
            save_name_str = filename + default_extension
        else:
            save_name_str = save_name
        try:
            with gzip.open(save_name_str, 'wb') as f:
                for key in self.__dict__.keys():
                    pickle.dump(getattr(self, key), f, pickle.HIGHEST_PROTOCOL)
                f.close()   # SJ review 반영
        except Exception:
            raise exc.DataIOException('저장이 되지 않았습니다. 확인하세요')

    def load_data(self, load_name):
        # load
        default_extension = self.save_default_extension
        filename, file_extension = os.path.splitext(load_name)
        # check file name
        if file_extension != default_extension:
            load_name_str = filename + default_extension
        else:
            load_name_str = load_name
        try:
            with gzip.open(load_name_str, 'rb') as f:
                for key in self.__dict__.keys():
                    setattr(self, key, pickle.load(f))
        except Exception:
            raise exc.DataIOException('파일을 확인하세요')

    # TODO: sever post / get 작성 및 테스트 요망
    def post_data(self, route_str, flag_str):
        if flag_str is 'server':  # if server output
            # with 를 통해 자동으로 서버연결 및 닫는 구조 가능 (아래 링크 참조)
            # https://soooprmx.com/archives/4079
            try:
                db_info = DataServer()
                db_info.connect_query()
                db_info.insert_query(route_str)
                db_info.disconnect_query()

            except Exception:
                raise exc.DataServerPutException('잘못된 서버 설정입니다')

        elif flag_str is 'csv':  # if file output
            print('file saving.....')
            try:
                print('done.....')
            except Exception:
                raise exc.DataDeniedException('파일 내 형식이 잘못되었습니다')
        else:
            raise exc.DataNotSupportedException('지원하지 않는 입력형식입니다')
        print('recording.... done')

    def get_data(self, route_str, flag_str):
        if flag_str is 'server':  # if server output
            pass
        elif flag_str is 'csv':  # if file output
            pass
        else:
            pass
        print('get data.... done')


def data_import_file(route_str):
    """
        작성자: cmlee
        작성일: 190416
        기능: 파일에서 추출하는 입력 구조를 함수로 분리시킴
        입력:
            파일 경로
        출력:
            DataNIRSIT inputs
        용례:
            []=data_import_file('~~~~.csv')
            ...
    """
    # TODO: meta, performance 에 대한 입력 필요
    print('file loading.....')
    try:
        if route_str.lower().endswith('.csv'):
            df_snr = pd.read_csv(route_str, header=None, error_bad_lines=False, skiprows=6, nrows=1)
            snr_calibration = df_snr

            df_data = pd.read_csv(route_str, header=None, error_bad_lines=False, skiprows=9)
            timestamp = df_data[0]
            raw780 = df_data[list(range(2, df_data.shape[1] - 7, 2))].T
            raw850 = df_data[list(range(3, df_data.shape[1] - 7, 2))].T
            battery = df_data[df_data.shape[1] - 7].T
            accel = df_data[list(range(df_data.shape[1] - 6, df_data.shape[1] - 3, 1))]
            gyro = df_data[list(range(df_data.shape[1] - 3, df_data.shape[1], 1))]

            # input for task_manager
            marker = df_data[1]

            # input for meta_information
            date, id_num, name, _, _, task_name, _ = route_str.replace('_', ' ').split()
            sex = []
            age = []
            inspector = []

            # input for performance
            acc = []
            rt = []

            # additional memo
            memo = ''

            # return
            return timestamp, raw780, raw850, accel, gyro, \
                   id_num, name, sex, age, inspector, date, task_name,\
                   acc, rt, marker, memo
        else:
            raise exc.DataNotSupportedException('본 함수는 csv 만 지원합니다')
    except Exception:
        raise exc.DataDeniedException('파일 내 형식이 잘못되었습니다')


def data_import_server(query_str):
    try:
        # 서버 연결은 나중에 작업하자
        db_info = DataServer()
        db_info.connect_query()
        data = db_info.select_query(query_str)
        db_info.disconnect_query()

    except Exception:
        raise exc.DataServerGetException('잘못된 서버 설정입니다')


def function_test():
    # test set/get attr
    test = DataNIRSIT()
    print(test.__dict__.keys())
    for key in test.__dict__.keys():
        value = getattr(test, key)
        print(value)
        setattr(test, key, [1])
        value = getattr(test, key)
        print(value)


def function_test2():
    # test load
    test = DataNIRSIT()
    test.load_data('save')
    print('this')


def function_test3():
    b = DataTask()
    b.set_value(np.array([1000, 0, 0, 0, 0, 0, 2000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1001]))
    print(b.task_block)


if __name__ == "__main__":
    function_test3()



