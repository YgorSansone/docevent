import requests
import pandas as pd
from datetime import datetime, timezone, timedelta
import os
from dotenv import load_dotenv

class APIWrapper:
    def __init__(self, authorization):
        self.base_url = "https://api-us-east-1.docevent.io/sfs-v1/object/"
        self.log_endpoint = "/log"
        self.user_endpoint = "/user"
        self.env = ["edi", "edisb"]
        self.authorization = authorization
        self.headers = {
            "authority": "api-us-east-1.docevent.io",
            "accept": "application.json, text.plain, */*",
            "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "authorization": self.authorization,
            "content-type": "application/json; charset=UTF-8",
            "origin": "https://us-east-1.docevent.io",
            "referer": "https://us-east-1.docevent.io/",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "macOS",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
        }
    
    def get_users(self, env):
        user_url = self.base_url + env + self.user_endpoint
        response = requests.get(user_url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to retrieve users for environment {env}. Status code: {response.status_code}")
            return []

class UserLogAnalyzer:
    def __init__(self, users, authorization):
        self.api = APIWrapper(authorization)
        self.users = users
        self.op_list = ["put", "get"]
        self.result_data = []

    def analyze_logs(self, env):
        for op in self.op_list:
            for user in self.users:
                user_name = user["username"]
                payload = {
                    "fromDate": "2020-01-01T00:00:00+00:00",
                    "toDate": "2023-10-24T13:34:48+00:00",
                    "from": 0,
                    "size": 1,
                    "filter": [f"op:{op}", f"user:{user_name}"]
                }
                print(f"Get logs from this user_name: {user_name}, on this env: {env}")

                response = requests.post(self.api.base_url + env + self.api.log_endpoint, json=payload, headers=self.api.headers)

                if response.status_code == 200:
                    data = response.json()
                    hits = data.get('hits', [])
                    hits = hits.get('hits', [])

                    if not hits:  # If there are no hits for the user
                        user_data = self.process_user_without_logs(user_name, op, env)
                        self.result_data.append(user_data)
                    else:
                        user_data = self.process_user_with_logs(hits[0], user_name, op, env)
                        self.result_data.append(user_data)
                else:
                    print(f"Failed to retrieve logs for user {user_name} and operation {op} in environment {env}. Status code: {response.status_code}")

    def process_user_without_logs(self, user_name, op, env):
        current_date = datetime.now(timezone.utc)
        is_greater_than_x_days = 30 if env == "edi" else 15  # 30 days for "edi," 15 days for others
        field_name = f'is_greater_than_{is_greater_than_x_days}_days' if env == "edi" else 'is_greater_than_15_days'
        user_data = {
            'created': "",
            'user_name': user_name,
            'path': "",
            'type': op,
            'current_date': current_date,
            f'date_difference_days_{env}': "",
            field_name: True
        }
        return user_data

    def process_user_with_logs(self, log_entry, user_name, op, env):
        created_str = log_entry["_source"]["created"]
        created = datetime.fromisoformat(created_str)
        path = log_entry["_source"]["src_path"]
        doc_type = log_entry["_source"]["type"]
        current_date = datetime.now(timezone.utc)
        date_difference = (current_date - created).days
        is_greater_than_x_days = date_difference > 30 if env == "edi" else date_difference > 15
        field_name = f'is_greater_than_{is_greater_than_x_days}_days' if env == "edi" else 'is_greater_than_15_days'

        user_data = {
            'created': created,
            'user_name': user_name,
            'path': path,
            'type': doc_type,
            'current_date': current_date,
            f'date_difference_days_{env}': date_difference,
            field_name: is_greater_than_x_days
        }
        return user_data

    def save_results_to_csv(self, env, file_name):
        result_df = pd.DataFrame(self.result_data)
        result_df.to_csv(file_name, index=False)

def main():
    load_dotenv()
    authorization = os.getenv("JIRA_COOKIE")

    for env in APIWrapper(authorization).env:
        user_data = APIWrapper(authorization).get_users(env)
        
        if not user_data:
            print(f"No user data retrieved for environment {env}. Skipping.")
            continue
        else:
            print(f"number of users: {len(user_data)} on {env} env!")
        
        analyzer = UserLogAnalyzer(user_data, authorization)
        analyzer.analyze_logs(env)
        file_name = f'{env}_users_api_data.csv'
        analyzer.save_results_to_csv(env, file_name)

if __name__ == '__main__':
    main()