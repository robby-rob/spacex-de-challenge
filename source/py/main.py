from requests import Session
import json
from sqlalchemy import create_engine
from psycopg2.extensions import register_adapter
from psycopg2.extras import Json
import pandas as pd

# config general
raw_fp = 'data'
base_url = 'https://api.spacexdata.com/v4'

# config postgres
db_host = 'host.docker.internal'
engine = create_engine(f'postgresql://postgres:mysecretpassword@{db_host}:5432/spacex')
register_adapter(dict, Json)

# spacex-api v4
endpoints = [
    #'capsules',
    #'company',
    #'cores',
    #'crew',
    #'dragons',
    #'history',
    'landpads',
    'launches',
    #'launchpads',
    'payloads',
    'rockets',
    #'ships',
    #'starlink'
]


def spacex_extract(endpoints):
    print('Starting extract...')

    with Session() as s:
        for endpoint in endpoints:
            uri = f'{base_url}/{endpoint}'
            response = s.get(uri)
            
            if response.status_code != 200:
                print(f'  {endpoint}: {response.status_code} {response.reason}')
                continue

            file_name = f'{raw_fp}/{endpoint}.jsonl'

            with open(file_name, 'w') as f:
                for record in response.json():
                    json.dump(record, f)
                    _ = f.write('\n')
            
            print(f'  {endpoint} success')

    print('Extract complete')


def spacex_load(endpoints):
    print('Starting load...')
    
    for endpoint in endpoints:
        try:
            file_name = f'{raw_fp}/{endpoint}.jsonl'
            table_name = f'raw_{endpoint}'
            df = pd.read_json(file_name, lines=True)
            df.to_sql(table_name, engine, if_exists='replace')

        except Exception as e:
            print(f'  {endpoint} failed: {e}')

        print(f'  {endpoint} success')

    print('Load complete')


spacex_extract(endpoints)
spacex_load(endpoints)
