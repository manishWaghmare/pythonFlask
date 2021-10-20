from django.http import JsonResponse
from django.db import connection
from django.http import HttpResponse
from datetime import date
import json

import pandas as pd

def process(request):
    with connection.cursor() as cursor:
        cursor.execute("select TRANSACTION_DATE,MEMBER_DATE,SCHEME_JOIN_DATE,NOM_DOB,MEM_ACTIVE_STAT_DATE,OPERATION_DATE,TRANSACTION_DATE from MEM_WEL_MASTER")
        # for column in  cursor.description:
        #     print(column)
        # columns = [col[0] for col in cursor.description]
        data = cursor.fetchall()
        connection.commit()
        df = pd.DataFrame(data , columns=[i[0] for i in  cursor.description])
        for columName in df.columns:
            if columName == 'TRANSACTION_DATE' or columName == 'MEMBER_DATE' or columName == 'SCHEME_JOIN_DATE' or columName == 'NOM_DOB' or columName == 'MEM_ACTIVE_STAT_DATE' or columName == 'OPERATION_DATE':
                df['MEMBER_DATE'] = df['MEMBER_DATE'].astype(str)
                df['SCHEME_JOIN_DATE'] = df['SCHEME_JOIN_DATE'].astype(str)
                df['NOM_DOB'] = df['NOM_DOB'].astype(str)
                df['MEM_ACTIVE_STAT_DATE'] = df['MEM_ACTIVE_STAT_DATE'].astype(str)
                df['OPERATION_DATE'] = df['OPERATION_DATE'].astype(str)
                df['TRANSACTION_DATE'] = df['TRANSACTION_DATE'].astype(str)
        json_list = list(df.T.to_dict().values())        
        # json_list = json.loads(json.dumps(list(df.T.to_dict().values())))        
        moduleResp = dict()
        moduleResp['cursor'] = json_list
        resp = json.dumps(moduleResp)
        cursor.close()
        connection.close()
        finalResp = json.loads(resp)
        return JsonResponse(finalResp)

def index(request):
    return HttpResponse("<h1>MyClub Event Calendar</h1>")         