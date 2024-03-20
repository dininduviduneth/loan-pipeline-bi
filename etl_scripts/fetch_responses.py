import json
import datetime
import os
from fetch_data import fetch_data

token = "49c56f5c-0726-4f27-a333-5275390caa45"
etl_dates = [(datetime.datetime(2023, 1, 1) + datetime.timedelta(days=i)).strftime(f"%Y-%m-%d") for i in range(90)]

# Fetch responses data
for date in etl_dates:
    date_split = date.split(sep='-')
    responses_file_path = f"data/responses/{date_split[0]}/{date_split[1]}/{date}.json"
    os.makedirs(os.path.dirname(responses_file_path), exist_ok=True)

    with open(responses_file_path, "w") as json_file:
        json.dump(fetch_data(endpoint='responses', token=token, dateFrom=date, dateTo=date), json_file)