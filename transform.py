import pandas as pd
import numpy as np
import re
import glob
from datetime import datetime
from sqlalchemy.dialects.oracle import VARCHAR2,NUMBER,FLOAT,DATE
from sqlalchemy import create_engine

files = glob.glob("*.csv")

def load(filename,csv=False):
    lines = open(filename).read().split('\n')

    lines = list(filter(lambda x: x != '',lines))
    header = list(filter(lambda x:x,[ i if not re.match('^[1-9]',d) else None for i,d in enumerate(lines) ]))
    cols = lines[header[-1]].split(',')
    rows_ = list(map(lambda x:x.split(','),lines[header[-1] + 1:]))
    rows_ = list(map(lambda x: x + [None]*(6 - len(x)) if len(x) < 6 else x,rows_))
    rows = np.array(rows_)

    fecha = list(filter(lambda x:re.match('^Fecha',x),lines[:header[-1]]))[0].split(' ')[1]

    sistema = list(filter(lambda x:re.match('^Sistema',x),lines[:header[-1]]))[0].split(' ')
    sistema = ''.join(list(map(lambda x:x[0],sistema)))


    meses = [
        ('enero','01'),
        ('febrero','02'),
        ('marzo','03'),
        ('abril','04'),
        ('mayo','05'),
        ('junio','06'),
        ('julio','07'),
        ('agosto','08'),
        ('septiembre','09'),
        ('octubre','10'),
        ('noviembre','11'),
        ('diciembre','12')
    ]

    for m in meses:
        fecha = re.sub(m[0],m[1],fecha.lower())

    df = pd.DataFrame(rows,columns=cols)
    col_rename = {
        'Hora':'HORA',
        'Clave del nodo':'CLAVE_NODO',
        'Precio marginal local ($/MWh)':'PML_MXN_MWH',
        'Componente de energia ($/MWh)':'ENERGIA_MXN_MWH',
        'Componente de perdidas ($/MWh)':'PERDIDAS_MXN_MWH',
        'Componente de congestion ($/MWh)':'CONGESTION_MXN_MWH'
    }

    df.rename(columns=col_rename,inplace=True)

    df['FECHA'] = [pd.to_datetime(fecha)] * len(df)
    df['SISTEMA'] = [sistema] * len(df)

    datatypes = {
        'SISTEMA':VARCHAR2(100),
        'FECHA':DATE,
        'HORA':NUMBER(28,22),
        'CLAVE_NODO':VARCHAR2(100),
        'PML_MXN_MWH':NUMBER(28,22),
        'ENERGIA_MXN_MWH':NUMBER(28,22),
        'PERDIDAS_MXN_MWH':NUMBER(28,22),
        'CONGESTION_MXN_MWH':NUMBER(28,22)
    }

    for i in ['HORA','PML_MXN_MWH','ENERGIA_MXN_MWH','PERDIDAS_MXN_MWH','CONGESTION_MXN_MWH']:
        df[i] = df[i].replace('',np.nan)
        df[i] = df[i].astype(float)


    df = df[['SISTEMA','FECHA','HORA','CLAVE_NODO','PML_MXN_MWH','ENERGIA_MXN_MWH','PERDIDAS_MXN_MWH','CONGESTION_MXN_MWH']]

    if csv:
        df.to_csv('forMongo/' + filename,index=False)
    else:
        df.to_sql('datos_precios_margloc_mda',conn,index=False,if_exists='append',dtype=datatypes)


def toCsv(files):
    faulty = []
    for i,f in enumerate(files):
        try:
            load(f,csv=True)
            if i % 100 == 0:
                print(i)
        except:
            faulty.append(f)
            print('\n')
            print('Error: ' + f)
            print('\n')
    return faulty
