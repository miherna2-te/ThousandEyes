from datetime import datetime
from getpass import getpass
import csv
import sys
import requests

USERNAME = input("Provide Username: ")
BASIC_TOKEN = getpass("Provide Basic Token: ")
AID_FILTER = input("Provide AID filter: ")


def api_get_call(USER, TOKEN, URL, AID=None):

    if len(AID) != 0:
        URL += f"?aid={AID}"

    response = requests.get(
        URL,
        headers={"content-type": "application/json"},
        auth=(USER, TOKEN),
    )

    if response.status_code != 200:
        print("Invalid Username or Password")
        sys.exit()

    result = response.json()
    result = result.get("test")
    return result


def main(USER, TOKEN, AID):
    tests_url = "https://api.thousandeyes.com/v6/tests.json"
    all_tests_configured = api_get_call(USER, TOKEN, tests_url, AID)

    now = datetime.now()
    date = now.strftime("%m%d%H%M%S")
    with open(f"tests_to_agents_{date}.csv", mode="w") as csv_file:
        fields = [
            "test_name",
            "test_id",
            "created",
            "modified",
            "modified_by",
            "test_type",
            "protocol",
            "url",
            "enabled",
            "alerts",
            "agents_information",
            "shared",
        ]
        writer = csv.DictWriter(csv_file, fieldnames=fields)
        writer.writeheader()

        for test in all_tests_configured:
            test_id = test.get("testId")
            details_url = f"https://api.thousandeyes.com/v6/tests/{test_id}.json"
            test_details = api_get_call(USER, TOKEN, details_url, AID)
            agents_in_test = test_details[0].get("agents")
            shared_accounts = test_details[0].get("sharedWithAccounts")
            shared_accounts = [account.get("name") for account in shared_accounts]
            shared_accounts = " - ".join(shared_accounts)

            if agents_in_test is not None:
                agent_information = str()
                for agent in agents_in_test:
                    agent_name = agent.get("agentName")
                    agent_type = agent.get("agentType")
                    agent_information += f"{agent_name} [{agent_type}] - "
                row = {
                    "test_name": test.get("testName"),
                    "test_id": test_id,
                    "created": test.get("createdDate"),
                    "modified": test.get("modifiedDate"),
                    "modified_by": test.get("modifiedBy"),
                    "test_type": test.get("type"),
                    "protocol": test.get("protocol"),
                    "url": test.get("url"),
                    "enabled": test.get("enabled"),
                    "alerts": test.get("alertsEnabled"),
                    "agents_information": agent_information,
                    "shared": shared_accounts,
                }
                writer.writerow(row)
                print(row)


if __name__ == "__main__":
    main(USERNAME, BASIC_TOKEN, AID_FILTER)
