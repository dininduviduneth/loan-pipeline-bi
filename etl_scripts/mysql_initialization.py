import mysql.connector

server_connection = mysql.connector.connect(
  host="localhost",
  user="root",
  password="odnel"
)

server_cursor = server_connection.cursor()

# CREATING THE DATABASE IF IT DOESN'T EXIST
server_cursor.execute("CREATE DATABASE IF NOT EXISTS odnel")

database_connection = mysql.connector.connect(
  host="localhost",
  user="root",
  password="odnel",
  database="odnel"
)

database_cursor = database_connection.cursor()

# CREATING THE APPLICATIONS STAGING TABLE
database_cursor.execute("""
    CREATE TABLE IF NOT EXISTS staging_applications (
            acceptance_date DATE,
            accepted_loan_status VARCHAR(255),
            application_accepted_by_user_type VARCHAR(255),
            application_created_by_user_type VARCHAR(255),
            application_creation_date DATE NOT NULL,
            application_id VARCHAR(255) PRIMARY KEY,
            application_user_agent VARCHAR(255),
            has_co_applicant BOOLEAN,
            paid_out_date DATE,
            refinance BOOLEAN,
            tracking_source_group_id INT,
            tracking_source_id INT,
            accepted_loan_amount DECIMAL(10,2),
            amortization_length INT,
            applied_loan_amount DECIMAL(10,2),
            highest_approved_amount DECIMAL(10,2),
            paid_out_loan_amount DECIMAL(10,2)
        )
""")

# CREATING THE RESPONSES STAGING TABLE
database_cursor.execute("""
    CREATE TABLE IF NOT EXISTS staging_responses (
        accepted_by_customer BOOLEAN,
        accepted_loan_purpose VARCHAR(255),
        application_id VARCHAR(255),
        bank_name VARCHAR(255),
        response_creation_date DATE NOT NULL,
        response_type VARCHAR(255),
        response_withdrawn_date DATE,
        interest_rate_effective DECIMAL(10,2),
        missing_response INT,
        offered_amount DECIMAL(10,2),
        rank_interest_rate INT,
        rank_offered_amount INT,
        response_id INT AUTO_INCREMENT PRIMARY KEY
    )
""")

# Close the cursor and connection
server_cursor.close()
database_cursor.close()
server_connection.close()
database_connection.close()