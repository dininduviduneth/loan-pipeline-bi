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

# Fetch applications data
for date in etl_dates:
    date_split = date.split(sep='-')
    applications_file_path = f"data/applications/{date_split[0]}/{date_split[1]}/{date}.json"
    os.makedirs(os.path.dirname(applications_file_path), exist_ok=True)

    with open(applications_file_path, "w") as json_file:
        applications_set = fetch_data(endpoint='applications', token=token, dateFrom=date, dateTo=date)
        records_added = 0
        for id, application in enumerate(applications_set):
            print(f"Attempting to insert {application['Application Id']} in {date}")
            database_cursor.execute(
                """
                INSERT INTO staging_applications (
                    acceptance_date,
                    accepted_loan_status,
                    application_accepted_by_user_type,
                    application_created_by_user_type,
                    application_creation_date,
                    application_id,
                    application_user_agent,
                    has_co_applicant,
                    paid_out_date,
                    refinance,
                    tracking_source_group_id,
                    tracking_source_id,
                    accepted_loan_amount,
                    amortization_length,
                    applied_loan_amount,
                    highest_approved_amount,
                    paid_out_loan_amount
                )
                VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                """,
                (
                    application.get('Acceptance Date'),
                    application.get('Accepted Loan Status'),
                    application.get('Application Accepted By User Type'),
                    application.get('Application Created By User Type'),
                    application.get('Application Creation Date'),
                    application.get('Application Id'),
                    application.get('Application User Agent'),
                    application.get('Has Co Applicant'),
                    application.get('Paid Out Date'),
                    application.get('Refinance'),
                    application.get('Tracking Source Group Id'),
                    application.get('Tracking Source Id'),
                    application.get('Accepted Loan Amount'),
                    application.get('Amortization Length'),
                    application.get('Applied Loan Amount'),
                    application.get('Highest Approved Amount'),
                    application.get('Paid Out Loan Amount')
                )
            )
            records_added = id

        database_connection.commit()
        print(f"{records_added} records inserted for {date}")

        json.dump(applications_set, json_file)
