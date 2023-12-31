# DocEvent API Script

This Python script analyzes user logs from the API and generates CSV files with the results. The script is designed to work with two environments: "edi" and "edisb." For the "edi" environment, it checks if the logs are older than 30 days, while for the "edisb" environment, it checks if the logs are older than 15 days.

## Prerequisites

Before using this script, make sure you have the following:

- Python 3.x installed
- Required Python packages installed. You can install them using `pip`:

## Installation

1. Clone this repository:

   ```bash
   git clone git@github.com:YgorSansone/docevent.git
   cd docevent
   
2. Install the required Python packages by running the following command:

    ```bash
    pip install -r requirements.txt
    ```
3. Configuration:

    Create a .env file in the project directory and add your DocEvent credentials:
    
    ```bash
    AUTH=your_cookie_value
    ```

    Note: Do not share or store your actual credentials in the ..env file. It's a good practice to use environment variables for sensitive information.

    Copy and rename the .env-sample file to .env to create a template for sharing without actual credentials.

4. Usage
    To run the script, execute the following command:

    ```bash
    python script.py
    ```

    Delete users:
    
     ```bash
    python delete_script.py
    ```

5. Deleting Unused Accounts

   If you need to delete unused user accounts in the specified environment, you can use the `delete_script.py` provided in this repository. This script uses the same authorization token as the main script (`script.py`) and allows you to specify a list of usernames to delete.

   To use the `delete_script.py`, follow the instructions in the [Usage](#usage) section of the main script README. Be sure to replace `"AUTH"` with your actual authorization token and customize the `user_list` and `environment` accordingly.

   When you run the `delete_script.py`, it will delete the specified user accounts and save information about which users were deleted and when they were deleted in a CSV file named after the environment (e.g., `edisb_deleted_users.csv`).

   Please use the deletion script with caution, as it permanently deletes the specified user accounts.