from requests import Session
import requests
import json
from sqlalchemy import create_engine
from psycopg2.extensions import register_adapter
from psycopg2.extras import Json
import pandas as pd

# config general
raw_fp = 'data'
base_url = 'https://api.spacexdata.com/v4'
gdp_url = 'https://www.imf.org/imf/weodatabase/downloadreport?c=512,914,612,171,614,311,213,911,314,193,122,912,313,419,513,316,913,124,339,638,514,218,963,616,223,516,918,748,618,624,522,622,156,626,628,228,924,233,632,636,634,238,662,960,423,935,128,611,321,243,248,469,253,642,643,939,734,644,819,172,132,646,648,915,134,652,174,328,258,656,654,336,263,268,532,944,176,534,536,429,433,178,436,136,343,158,439,916,664,826,542,967,443,917,544,941,446,666,668,672,946,137,546,674,676,548,556,678,181,867,682,684,273,868,921,948,943,686,688,518,728,836,558,138,196,278,692,694,962,142,449,564,565,283,853,288,293,566,964,182,359,453,968,922,714,862,135,716,456,722,942,718,724,576,936,961,813,726,199,733,184,524,361,362,364,732,366,144,146,463,528,923,738,578,537,742,866,369,744,186,925,869,746,926,466,112,111,298,927,846,299,582,487,474,754,698,&s=NGDPD,PPPGDP,&sy=2020&ey=2021&ssm=0&scsm=0&scc=0&ssd=1&ssc=0&sic=0&sort=country&ds=.&br=1&wsid=f0fb76c5-f774-4759-92bf-316f8381540e'

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
