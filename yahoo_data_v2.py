import os
import re
import jwt
import json
import pprint
import time
import pandas as pd
import requests, zipfile, io
from dotenv import load_dotenv
from datetime import datetime, timedelta

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from google.cloud.sql.connector import Connector, IPTypes

# load env vars
load_dotenv()


from slack_sdk.webhook import WebhookClient
url = "https://hooks.slack.com/services/xxxxxxxxxx" # Your Slack Webhook URL
webhook = WebhookClient(url)

yesterday = datetime.now() - timedelta(hours=3)
yest_date = datetime.strftime(yesterday, '%Y%m%d%H')
# yest_date = '2024030501'


proxies = {
   'http': 'http://proxy.example.com:8080',
   'https': 'http://proxy.example.com:8080',
}

MAX_RETRY = 6

class PythonSample:
    def __init__(self):
        self.b2bHost = "id.b2b.yahooinc.com"
        self.accessTokenURL = "https://" + self.b2bHost + "/identity/oauth2/access_token"
        self.grantType = "client_credentials"
        self.scope = "pi-api-access"
        self.realm = "pi"
        self.clientAssertionType = 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer'
        self.clientId = "Fill your client id"
        self.clientSecret = "Fill your client secret"

    def generateJWT(self):
        audience = "https://" + self.b2bHost + "/identity/oauth2/access_token?realm=" + self.realm
        payload = {"aud": audience, "iss": self.clientId, "sub": self.clientId, "iat": int(time.time()),
                   "exp": int(time.time()) + 300}
        token = jwt.encode(payload, self.clientSecret)
        # print(token)
        time.sleep(5)
        return token

    def getAccessToken(self, date):
        data = {"grant_type": self.grantType, "client_assertion_type": self.clientAssertionType,
                "realm": self.realm, "scope": self.scope, "client_assertion": self.generateJWT()}
        s = requests.Session()
        response = s.post(self.accessTokenURL, data=data)
        jsonObject1 = json.loads(response.text)
        accessToken = jsonObject1["access_token"]

        types_hourly = f"https://api-partnerinsights.yahoo.com/PartnerAnalytics/service/ReportsAPI/getDataAvailability?reportType=Fast%20Type&startDate={yest_date}&endDate={yest_date}&rollup=Hourly&format=json"
        head = {'Authorization': 'Bearer {}'.format(accessToken)}
        response = s.get(types_hourly, headers=head, verify=False,proxies=proxies)

        is_available = json.loads(response.text)
        pprint.pprint(is_available)

        if is_available['ResultSet']['Row']['IS_AVAILABLE'] == 'YES':
            tags_agg = f"https://api-partnerinsights.yahoo.com/PartnerAnalytics/service/ReportsAPI/getFastTypeDetailReport?dateRange=HOURLY&startDate={yest_date}&endDate={yest_date}&dateRollup=hourly&product=ALL&attributeList=market%2Cdevice_type%2Cad_type&mrkt_id=ALL&sourceTag=*surprisesavings*&partnerList=ALL&device=ALL&currency=1&startRow=1&returnRows=1000000&orderBy=Revenue&type=ASYNC&format=json"
            head = {'Authorization': 'Bearer {}'.format(accessToken)}
            response = s.get(tags_agg, headers=head, verify=False,proxies=proxies)

            jsonObject = json.loads(response.text)
            pprint.pprint(jsonObject)
            time.sleep(5)

            for i in range(1, MAX_RETRY):

                if jsonObject['MetaInfo']['ResponseStatus'] == 'SUCCESS':

                    job_id = jsonObject['ResultSet']['Row']['ID']
                    job = f"https://api-partnerinsights.yahoo.com/PartnerAnalytics/service/ReportsAPI/getAsyncJobStatus?asyncJobId={job_id}&fileFormat=json&format=json"
                    response = s.get(job, headers=head, verify=False,proxies=proxies)
                    data_file = json.loads(response.text)
                    pprint.pprint(data_file)
                    time.sleep(30)

                    if data_file['ResultSet']['Row']['REPORT_STATUS'] == 'Completed':

                        zip_file_url = data_file['ResultSet']['Row']['REPORT_OUTPUT_FILE']
                        r = s.get(zip_file_url, headers=head, verify=False,proxies=proxies)
                        z = zipfile.ZipFile(io.BytesIO(r.content))
                        json_data = z.read(z.namelist()[0])
                        fix_bytes_value = json_data.replace(b"'", b'"')
                        my_json = json.load(io.BytesIO(fix_bytes_value))

                        return my_json
                        break

                    else:
                        webhook.send(text=f"Yahoo API: Error While downloading the report, REPORT_STATUS: {data_file['ResultSet']['Row']['REPORT_STATUS']}")
                        time.sleep(20 * i)
                else:
                    webhook.send(text=f"Yahoo API: Error while generating the report, ResponseStatus: {jsonObject['MetaInfo']['ResponseStatus']}")
        else:
            webhook.send(text=f"Yahoo API: Error while generating the report, ResponseStatus: {is_available['ResultSet']['Row']}")


def flatten(l):
    return [item for sublist in l for item in sublist]

def date_func(datetime_str):
    date = datetime.strptime(datetime_str, '%Y%m%d%H')
    return date

def split_strings_updated(input_strings):
    results = []
    for s in input_strings:
        # Updated regex to capture the domain, and optionally, port or path after a colon
        match = re.search(r'MQ([a-zA-Z0-9]*)\.?([a-zA-Z0-9\.-]+)(?::([a-zA-Z0-9\._-]+))?', s)
        if match:
            part1 = match.group(1)
            # Combine the domain and the port/path, if present
            part2 = match.group(2)
            if match.group(3):  # If there's a port/path, append it to part2
                part2 += ":" + match.group(3)
        else:
            part1, part2 = "", ""
        results.append((part1, part2))
    return results

def data_cleaning(my_json):
    data = pd.DataFrame(my_json)
    df1 = data[~data['ResultSet'].isnull()]['ResultSet']
    df1 = df1.to_frame('data1')
    list2 = []
    for i in df1['data1']:
        list2.append(i)
    final_yahoo = flatten(list2)

    yahoo_df = pd.DataFrame(final_yahoo)
    # yahoo_df.to_csv('yahoo_types_hourly_api_data.csv')
    yahoo_df = yahoo_df.astype({'DATA_HOUR': 'str'})
    yahoo_df['datetime'] = yahoo_df['DATA_HOUR'].apply(date_func)
    yahoo_df['date'] = yahoo_df['datetime'].dt.date
    yahoo_df['hour'] = yahoo_df['datetime'].dt.hour

    split_data = split_strings_updated(yahoo_df['TYPE_TAG'])
    split_df = pd.DataFrame(split_data, columns=['type_tag', 'domain'])
    yahoo_df = pd.concat([yahoo_df, split_df], axis=1)

    yahoo_df = yahoo_df.drop(['DATA_HOUR','CURRENCY_CODE','AD_TYPE','BIDDED_SEARCHES', 'BIDDED_RESULTS','COVERAGE',
                  'CTR','PPC_LOCAL', 'SUGG_REVENUE_ALLOC_LOCAL', 'RN', 'datetime'],axis=1)

    yahoo_df['affiliate'] = 'xxxxxxx' # Your affiliate brand
    yahoo_df['partner'] = 'xxxxxxx' # Your partner brand

    market_codes = pd.read_csv('/Users/deepaksheoran/market_codes.csv')
    yahoo_df = yahoo_df.merge(market_codes, on='MARKET', how='left')
    yahoo_df = yahoo_df.rename({'ESTIMATED_GROSS_REVENUE_LOCAL':'est_revenue','BIDDED_CLICKS':'clicks','CODE':'market'},axis=1)

    yahoo_df['est_revenue'] = yahoo_df['est_revenue'].astype('float').round(6)

    yahoo_df = yahoo_df.reindex(columns=[ 'affiliate','domain', 'date', 'hour', 'partner', 'market', 'SOURCE_TAG', 'DEVICE_TYPE', 'type_tag',
       'SEARCHES', 'clicks','est_revenue', 'TQ_SCORE'])

    yahoo_df = yahoo_df.rename({'SOURCE_TAG': 'source_tag', 'DEVICE_TYPE': 'device', 'SEARCHES': 'searches',
                      'clicks': 'bidded_clicks', 'TQ_SCORE': 'tq_score'}, axis=1)

    yahoo_df = yahoo_df.astype({"searches": 'int', 'bidded_clicks': 'int', 'tq_score': 'int'})

    return yahoo_df


def init_connection_engine(connector: Connector) -> Engine:
    # if env var PRIVATE_IP is set to True, use private IP Cloud SQL connections
    ip_type = IPTypes.PRIVATE if os.getenv("PRIVATE_IP") is True else IPTypes.PUBLIC
    # if env var DB_IAM_USER is set, use IAM database authentication
    user, enable_iam_auth = (
        (os.getenv("DB_IAM_USER"), True)
        if os.getenv("DB_IAM_USER")
        else (os.getenv("DB_USER"), False)
    )

    # Cloud SQL Python Connector creator function
    def getconn():
        conn = connector.connect(
            os.getenv("INSTANCE_CONNECTION_NAME"),
            "pg8000",
            user=user,
            password=os.getenv("DB_PASS", ""),
            db=os.getenv("DB_NAME"),
            ip_type=ip_type,
            enable_iam_auth=enable_iam_auth,
        )
        return conn

    SQLALCHEMY_DATABASE_URL = "postgresql+pg8000://"

    engine = create_engine(SQLALCHEMY_DATABASE_URL, creator=getconn)
    return engine

Base = declarative_base()

# initialize Python Connector and connection pool engine
connector = Connector()
engine = init_connection_engine(connector)

def call_func():
    sample = PythonSample()
    if sample.clientId == "" or sample.clientSecret == "":
        print("Please fill the empty field before testing")
        exit()
    json_data = sample.getAccessToken(yest_date)
    df_fin = data_cleaning(json_data)
    return df_fin

try:
    postgres_df = call_func()
    postgres_df.to_csv(f'yahoo_types_{yest_date}.csv', index=False)
    postgres_df = postgres_df.rename({'SOURCE_TAG':'source_tag','DEVICE_TYPE':'device','SEARCHES':'searches',
                'clicks':'bidded_clicks','TQ_SCORE':'tq_score'},axis=1)

    postgres_df['date'] = pd.to_datetime(postgres_df['date'])

    with engine.connect() as db_conn:
        postgres_df.to_sql('yahoo_types_hourly', db_conn, if_exists='append', index=False, method='multi', chunksize=2500)
        db_conn.commit()
        print(f'Dumped data successfully! Date: {postgres_df["date"][0]} --> {postgres_df["hour"][0]}!')

    # cleanup connector
    connector.close()

except Exception as e:
    webhook.send(text=f"Yahoo API: Error while executing the script. Exception: [{e}]")








