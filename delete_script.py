import requests
import pandas as pd
from datetime import datetime, timezone, timedelta
import os
from dotenv import load_dotenv

class UserDeletion:
    def __init__(self, auth_token):
        self.base_url = "https://api-us-east-1.docevent.io/sfs-v1/object/"
        self.user_endpoint = "/user"
        self.headers = {
            "authority": "api-us-east-1.docevent.io",
            "accept": "application/json, text/plain, */*",
            "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "authorization": auth_token,
            "origin": "https://us-east-1.docevent.io",
            "referer": "https://us-east-1.docevent.io/",
            "sec-ch-ua": "\"Chromium\";v=\"118\", \"Google Chrome\";v=\"118\", \"Not=A?Brand\";v=\"99\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "macOS",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
        }
        self.deletion_data = []  # List to store deleted user data

    def delete_users(self, environment, user_list):
        for username in user_list:
            url = f"{self.base_url}{environment}{self.user_endpoint}/{username}"
            response = requests.delete(url, headers=self.headers)

            if response.status_code == 200:
                print(f"Deleted user {username} in the {environment} environment.")
                self.deletion_data.append({'Username': username, 'Deleted At': datetime.now()})
            else:
                print(f"Failed to delete user {username} in the {environment} environment. Status code: {response.status_code}")

    def save_deletion_data_to_csv(self, environment):
        if self.deletion_data:
            file_name = f'{environment}_deleted_users.csv'
            deletion_df = pd.DataFrame(self.deletion_data)
            deletion_df.to_csv(file_name, index=False)
            print(f"Deleted user data saved to {file_name}.")
        else:
            print("No user data to save.")

def main():
    load_dotenv()
    authorization = os.getenv("AUTH")
    user_list = ["user_name"]  # Replace with the list of usernames you want to delete
    environment = "edisb"  # Specify the environment where the users should be deleted

    user_deletion = UserDeletion(authorization)
    user_deletion.delete_users(environment, user_list)
    user_deletion.save_deletion_data_to_csv(environment)

if __name__ == "__main__":
    main()
