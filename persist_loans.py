import pandas as pd
from os.path import join
import http.client as client
from urllib import request
import json


DOMAIN = 'localhost:8000'
DATAPATH = './data'
DATAFILE = 'loans_tbl.csv'
LIMIT = 200


def upload(row):
    pk = row.member_id
    body = row.to_json()
    try:
        conn = client.HTTPConnection(DOMAIN)
        path = '/loan/' + str(pk) + '/'
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

    df['meets_policy'] = ~df['loan_status'].str.contains('Does not meet the credit policy')

    df = df.rename(columns={
        'funded_amnt':  'funded_amount',
        'total_pymnt':  'total_payments',
        'sub_grade':    'grade',
        'int_rate':     'interest_rate',
        'loan_amnt':    'amount',
        'loan_status':  'status',
    })

    nrecords = LIMIT if LIMIT is not None else len(df)
    for i in range(nrecords):
        row = df.iloc[i]
        upload(row)
    print ("DONE.")

    


