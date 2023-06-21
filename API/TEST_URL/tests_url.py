"""
ThousandEyes Tests Information

This script analyzes the tests for each account group in ThousandEyes
nd provides details about each test, including the name, test ID, test type,
protocol, probe method, and path trace settings.

Usage:
    python tests_url.py

Author: Miguel Hernandez
Date: June 21, 2023
"""
import csv
import re
import requests
from getpass import getpass


def get_accounts(username, token):
    """
    Retrieves account information from the ThousandEyes API and returns a
    dictionary mapping account IDs to account names.

    Args:
        username (str): The username for authentication.
        token (str): The basic authentication token.

    Returns:
        dict: A dictionary mapping account IDs (aid) to account names (Account Group Name).

    Raises:
        requests.exceptions.RequestException: If there was an error making the API request.
    """
    headers = {"content-type": "application/json"}

    url = "https://api.thousandeyes.com/v6/account-groups.json"

    try:
        response = requests.get(url, headers=headers, auth=(username, token), timeout=5)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        print("Get Accounts Exception: Request timed out to getting accounts")
    except requests.exceptions.RequestException as error:
        print("Get Accounts Exception:", str(error))
    account_groups = response.json().get("accountGroups")
    accounts = {
        entry.get("aid"): entry.get("accountGroupName") for entry in account_groups
    }
    return accounts


def get_tests(username, token, aid):
    """
    Retrieves tests information from the ThousandEyes API and returns a
    dictionary with the details of each test.

    Args:
        username (str): The username for authentication.
        token (str): The basic authentication token.

    Returns:
        dict: A dictionary with test's information.

    Raises:
        requests.exceptions.RequestException: If there was an error making the API request.
    """
    headers = {"content-type": "application/json"}

    url = f"https://api.thousandeyes.com/v6/tests.json?aid={aid}"

    try:
        response = requests.get(url, headers=headers, auth=(username, token), timeout=5)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        print("Get Tests Exception: Request timed out to getting accounts")
    except requests.exceptions.RequestException as error:
        print("Get Tests Exception:", str(error))
    tests_configured = response.json().get("test")
    return tests_configured


def get_tests_url(username, token, accounts):
    """
    Retrieves test information for multiple accounts and writes the data to a CSV file.

    Args:
        username (str): The username used for authentication.
        token (str): The authentication token.
        accounts (list): A list of account IDs for which test information is to be retrieved.

    Returns:
        None

    File Output:
        The function writes the test information to a CSV file named "tests_url.csv".
        The file is created in the current directory. If a file with the same name
        already exists, it will be overwritten.
    """
    for aid in accounts:
        tests = get_tests(username, token, aid)
        with open("tests_url.csv", mode="w") as csv_file:
            writer = csv.writer(
                csv_file,
            )
            writer.writerow(["AID", "TEST_ID", "TEST_NAME", "URL"])
            for test in tests:
                test_id = str(test.get("testId"))
                test_name = str(test.get("testName"))
                url = str(test.get("url"))
                print(aid, test_id, test_name, url)
                writer.writerow([aid, test_id, test_name, url])


if __name__ == "__main__":
    USERNAME = input("Provide Username: ")
    BASIC_TOKEN = getpass("Provide Basic Token: ")

    accounts_dict = get_accounts(USERNAME, BASIC_TOKEN)
    get_tests_url(USERNAME, BASIC_TOKEN, accounts_dict)
