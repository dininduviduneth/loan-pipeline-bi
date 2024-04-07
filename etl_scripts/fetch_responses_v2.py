import json
import datetime
import os
import mysql.connector

from fetch_data import fetch_data

token = "XXXX"
etl_dates = [(datetime.datetime(2023, 1, 1) + datetime.timedelta(days=i)).strftime(f"%Y-%m-%d") for i in range(90)]

database_connection = mysql.connector.connect(
  host="localhost",
  user="root",
  password="odnel",
  database="odnel"
)

database_cursor = database_connection.cursor()

# Fetch responses data
for date in etl_dates:
    date_split = date.split(sep='-')
    responses_file_path = f"data/responses/{date_split[0]}/{date_split[1]}/{date}.json"
    os.makedirs(os.path.dirname(responses_file_path), exist_ok=True)

    with open(responses_file_path, "w") as json_file:
        responses_set = fetch_data(endpoint='responses', token=token, dateFrom=date, dateTo=date)

        records_added = 0
        for id, response in enumerate(responses_set):
            print(f"Attempting to insert {response['Application Id']} in {date}")
            database_cursor.execute(
                """
                INSERT INTO staging_responses (
                    accepted_by_customer,
                    accepted_loan_purpose,
                    application_id,
                    bank_name,
                    response_creation_date,
                    response_type,
                    response_withdrawn_date,
                    interest_rate_effective,
                    missing_response,
                    offered_amount,
                    rank_interest_rate,
                    rank_offered_amount
                )
                VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                """,
                (
                    response.get('Accepted By Customer'),
                    response.get('Accepted Loan Purpose'),
                    response.get('Application Id'),
                    response.get('Bank Name'),
                    response.get('Response Creation Date'),
                    response.get('Response Type'),
                    response.get('Response Withdrawn Date'),
                    response.get('Interest Rate Effective'),
                    response.get('Missing Response'),
                    response.get('Offered Amount'),
                    response.get('Rank Interest Rate'),
                    response.get('Rank Offered Amount')
                )
            )
            records_added = id

        database_connection.commit()
        print(f"{records_added} records inserted for {date}")

        json.dump(responses_set, json_file)