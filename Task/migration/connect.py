import sys
import os
import numpy as np
import pandas as pd
import pandas.io.sql as psql
import psycopg2

# DB 정보 업데이트
class Migration():
    def __connect__(self):
        host = ""
        user = ""
        dbname = ""
        password = ""
        sslmode = "require"

        # DB connector
        conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)
        try:
            conn = psycopg2.connect(conn_string) 
            print("연결 완료")
        except:
            print("연결 실패")
            pass

    def __sql__():
        cursor = conn.cursor()

        # insert 데이터명 from DB where ~~~ 

        try:
            cursor.execute("SQL 문장")  #  insert가 들어갈 것으로 보임 | SQL문장을 미리 작성
        except expression as identifier:
            print("sql 실행 불능")
    
    def __data_proccsing__():
        import math
        import operator
        import matplotlib as mpl
        import matplotlib.pylab as plt
        
        source = ""
        
        db1 = pd.read_csv(source)
        
        if source is exist:
            db2.drop(["칼럼명, 칼럼명, 칼럼명"], axis=1)
            db2.dropna()
            db3 = open("DB.csv", wr, encoding = "UTF-8")
        del math
        del operator
        del matplolib
        del matplotlib.pylab


    # clean up

    conn.commit()
    cursor.close()
    conn.close()
