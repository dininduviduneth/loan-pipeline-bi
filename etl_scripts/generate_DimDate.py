import datetime
import mysql.connector

from fetch_data import fetch_data

token = "49c56f5c-0726-4f27-a333-5275390caa45"
etl_dates = [(datetime.datetime(2023, 1, 1) + datetime.timedelta(days=i)).strftime(f"%Y-%m-%d") for i in range(90)]

database_connection = mysql.connector.connect(
  host="localhost",
  user="root",
  password="odnel",
  database="odnel"
)

database_cursor = database_connection.cursor()

for date in etl_dates:
    print(f"Attempting to insert {date} to the table..")
    database_cursor.execute(
        f"""
        INSERT INTO DimDate (Date, Day, DayName, Week, ISOWeek, DayOfWeek, Month, MonthName, Quarter, Year, FirstOfMonth, LastOfYear, DayOfYear)
        VALUES (
            '{date}',                                                 -- Date
            DAY('{date}'),                                            -- Day
            DAYNAME('{date}'),                                        -- DayName
            WEEK('{date}'),                                           -- Week
            WEEK('{date}', 3),                                        -- ISOWeek
            DAYOFWEEK('{date}'),                                      -- DayOfWeek
            MONTH('{date}'),                                          -- Month
            MONTHNAME('{date}'),                                      -- MonthName
            QUARTER('{date}'),                                        -- Quarter
            YEAR('{date}'),                                           -- Year
            DATE_FORMAT('{date}', '%Y-%m-01'),                        -- FirstOfMonth
            DATE_FORMAT(LAST_DAY('{date}'), '%Y-%m-%d'),              -- LastOfYear
            DAYOFYEAR('{date}')                                       -- DayOfYear
        );
        """
    )
    database_connection.commit()