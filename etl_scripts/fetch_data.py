import requests

def fetch_data(endpoint, token, dateFrom, dateTo):
    api_url = f"https://sample-database-case-hholxbesyq-lm.a.run.app/{endpoint}?token={token}&dateFrom={dateFrom}&dateTo={dateTo}"

    response = requests.get(api_url)

    if response.status_code == 200:
        print(f"Fetched {endpoint} in [{dateFrom} - {dateTo}]")
        return response.json()
    else:
        print(f"Error: {response.status} - could not load {endpoint} in [{dateFrom} - {dateTo}]")