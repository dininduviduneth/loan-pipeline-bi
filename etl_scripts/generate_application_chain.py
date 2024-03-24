import mysql.connector

database_connection = mysql.connector.connect(
  host="localhost",
  user="root",
  password="odnel",
  database="odnel"
)

database_cursor = database_connection.cursor()

# Drop the existing application_chain table
database_cursor.execute(
    """
    DROP TABLE IF EXISTS application_chain;
    """
)

database_cursor.execute(
    """
    -- Create the application_chain table
    CREATE TABLE IF NOT EXISTS application_chain (
        application_id VARCHAR(255) PRIMARY KEY,
        application_creation_date DATE,
        response_creation_date DATE,
        acceptance_date DATE,
        paid_out_date DATE,
        response_withdrawn_date DATE,
        lt_apre INT,
        lt_reac INT,
        lt_acpa INT,
        lt_acwi INT,
        bank_name VARCHAR(255),
        accepted_loan_purpose VARCHAR(255),
        applied_loan_amount DECIMAL(10, 2),
        offered_amount DECIMAL(10, 2),
        highest_approved_amount DECIMAL(10, 2),
        accepted_loan_amount DECIMAL(10, 2),
        paid_out_loan_amount DECIMAL(10, 2),
        amortization_length INT,
        interest_rate_effective DECIMAL(5, 2),
        accepted_loan_status VARCHAR(50),
        has_co_applicant BOOLEAN,
        refinance BOOLEAN,
        pending_payment BOOLEAN,
        rank_interest_rate INT,
        rank_offered_amount INT
    );
    """
)

database_connection.commit()

database_cursor.execute(
    """
    -- Insert data from the query into the application_chain
    INSERT INTO application_chain
    SELECT
        l.application_id AS application_id,
        l.application_creation_date AS application_creation_date,
        r.response_creation_date AS response_creation_date,
        l.acceptance_date AS acceptance_date,
        l.paid_out_date AS paid_out_date,
        r.response_withdrawn_date AS response_withdrawn_date,
        (r.response_creation_date - l.application_creation_date) AS lt_apre,
        (l.acceptance_date - r.response_creation_date) AS lt_reac,
        (l.paid_out_date - l.acceptance_date) AS lt_acpa,
        (r.response_withdrawn_date - l.acceptance_date) AS lt_acwi,
        r.bank_name AS bank_name,
        r.accepted_loan_purpose AS accepted_loan_purpose,
        l.applied_loan_amount AS applied_loan_amount,
        r.offered_amount AS offered_amount,
        l.highest_approved_amount AS highest_approved_amount,
        l.accepted_loan_amount AS accepted_loan_amount,
        l.paid_out_loan_amount AS paid_out_loan_amount,
        l.amortization_length AS amortization_length,
        r.interest_rate_effective AS interest_rate_effective,
        l.accepted_loan_status AS accepted_loan_status,
        l.has_co_applicant AS has_co_applicant,
        l.refinance AS refinance,
        CASE WHEN l.paid_out_date IS NULL THEN 1 ELSE 0 END AS pending_payment,
        r.rank_interest_rate AS rank_interest_rate,
        r.rank_offered_amount AS rank_offered_amount
    FROM
        (
            SELECT
                application_id,
                application_creation_date,
                acceptance_date,
                paid_out_date,
                accepted_loan_status,
                has_co_applicant,
                refinance,
                amortization_length,
                accepted_loan_amount,
                applied_loan_amount,
                highest_approved_amount,
                paid_out_loan_amount
            FROM staging_applications
        ) AS l
        LEFT OUTER JOIN
        (
            SELECT
                application_id,
                response_creation_date,
                accepted_loan_purpose,
                bank_name,
                response_withdrawn_date,
                offered_amount,
                interest_rate_effective,
                rank_interest_rate,
                rank_offered_amount
            FROM staging_responses
            WHERE accepted_by_customer = 1
        ) AS r
        ON l.application_id = r.application_id;
    """
)

# Check result status
if database_cursor.rowcount > 0:
    print("Query executed successfully and returned {} rows.".format(database_cursor.rowcount))
else:
    print("Query did not return any rows.")

database_connection.commit()
# Close the cursor and connection
database_cursor.close()
database_connection.close()