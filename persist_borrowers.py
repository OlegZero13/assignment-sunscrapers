import pandas as pd
from os.path import join
import http.client as client
from urllib import request
import json


DOMAIN = 'localhost:8000'
DATAPATH = './data'
DATAFILE = 'borrowers_tbl.csv'
LIMIT = 100


def upload(row):
    pk = row.member_id
    body = row.to_json()
    try:
        conn = client.HTTPConnection(DOMAIN)
        path = '/borrower/' + str(pk) + '/'
        conn.request('POST', path, body=body)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        print (data)
    except Exception as e:
        print (e)

if __name__ == '__main__':
    df = pd.read_csv(join(DATAPATH, DATAFILE))
    df = df[[c for c in df.columns if not c.startswith('Unnamed')]]
    df = df.rename(columns={
        'addr_state': 'address_state',
        'annual_inc': 'annual_income',
    })

    nrecords = LIMIT if LIMIT is not None else len(df)
    for i in range(nrecords):
        row = df.iloc[i]
        upload(row)
    print ("DONE.")

    


