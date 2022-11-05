import csv
import requests
from getpass import getpass

USERNAME = input("Provide Username: ")
BASIC_TOKEN = getpass("Provide Basic Token: ")
AID_FILTER = input("Provide AID filter: ")

def api_get_call(USER, TOKEN, URL, AID = None):

    if len(AID) != 0:
        URL += f"?aid={AID}"

    response = requests.get(
        URL,
        headers = {"content-type": "application/json"},
        auth=(USER, TOKEN),
    )

    result = response.json()
    result = result.get("test")
    return result


def main(USER, TOKEN, AID):
    tests_url = "https://api.thousandeyes.com/v6/tests.json"
    all_tests_configured = api_get_call(USER, TOKEN, tests_url, AID)

    with open("tests_to_agents_details.csv", mode="w") as csv_file:
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
            "agent_name",
            "agent_type",
            "shared",
        ]
        writer = csv.DictWriter(csv_file, fieldnames=fields)
        writer.writeheader()

        for test in all_tests_configured:
            test_name = test.get("testName")
            test_id = test.get("testId")
            created_date = test.get("createdDate")
            modified_date = test.get("modifiedDate")
            modified_by = test.get("modifiedBy")
            test_type = test.get("type")
            protocol = test.get("protocol")
            url = test.get("url")
            enabled = test.get("enabled")
            alerts = test.get("alertsEnabled")
            details_url = f"https://api.thousandeyes.com/v6/tests/{test_id}.json"
            test_details = api_get_call(USER, TOKEN, details_url, AID)
            agents_in_test = test_details[0].get("agents")
            shared_accounts = test_details[0].get("sharedWithAccounts")
            shared_accounts = [account.get("name") for account in shared_accounts]
            shared_accounts = " - ".join(shared_accounts)
            row =  {
                    "test_name": test_name,
                    "test_id": test_id,
                    "created": created_date,
                    "modified": modified_date,
                    "modified_by": modified_by,
                    "test_type": test_type,
                    "protocol": protocol,
                    "url": url,
                    "enabled": enabled,
                    "alerts": alerts,
                    "agent_name": "",
                    "agent_type": "",
                    "shared": shared_accounts,
                    }
            if agents_in_test is not None:
                for agent in agents_in_test:
                    row["agent_name"] = agent.get("agentName")
                    row["agent_type"] = agent.get("agentType")
                    writer.writerow(row)
                    print(row)
            else:
                writer.writerow(row)
                print(row)


if __name__ == "__main__":
    main(USERNAME, BASIC_TOKEN, AID_FILTER)
