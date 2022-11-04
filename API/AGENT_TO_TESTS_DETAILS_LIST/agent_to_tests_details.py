import requests
import csv
from getpass import getpass

USERNAME = input("Provide Username: ")
BASIC_TOKEN = getpass("Provide Basic Token: ")
AID = input("Provide AID filter: ")


def get_tests_information(USERNAME, BASIC_TOKEN, AID):
    headers = {"content-type": "application/json"}

    if AID:
        url = f"https://api.thousandeyes.com/v6/tests.json?aid={AID}"
    else:
        url = "https://api.thousandeyes.com/v6/tests.json"

    tests_api = requests.get(
        url,
        headers=headers,
        auth=(USERNAME, BASIC_TOKEN),
    )

    all_tests_configured = tests_api.json()
    all_tests_configured = all_tests_configured.get("test")

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
            "agents_name",
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
            if AID:
                url_details = (
                    f"https://api.thousandeyes.com/v6/tests/{test_id}.json?aid={AID}"
                )
            else:
                url_details = f"https://api.thousandeyes.com/v6/tests/{test_id}.json"
            tests_details = requests.get(
                url_details,
                headers=headers,
                auth=(USERNAME, BASIC_TOKEN),
            ).json()

            agents_in_test = tests_details.get("test")
            agents_in_test = agents_in_test[0].get("agents")
            shared_accounts = tests_details.get("test")
            shared_accounts = shared_accounts[0].get("sharedWithAccounts")
            shared_accounts = [account.get("name") for account in shared_accounts]
            shared_accounts = " - ".join(shared_accounts)

            if agents_in_test is not None:
                for agent in agents_in_test:
                    agent_name = agent.get("agentName")
                    agent_type = agent.get("agentType")
                    if agent_name:
                        writer.writerow(
                            {
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
                                "agents_name": agent_name,
                                "agent_type": agent_type,
                                "shared": shared_accounts,
                            }
                        )
                        print(
                            test_name,
                            test_id,
                            created_date,
                            modified_date,
                            modified_by,
                            test_type,
                            protocol,
                            url,
                            enabled,
                            alerts,
                            agent_name,
                            agent_type,
                            shared_accounts,
                        )
            else:
                writer.writerow(
                    {
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
                        "agents_name": "",
                        "agent_type": "",
                        "shared": "",
                    }
                )
                print(
                    test_name,
                    test_id,
                    created_date,
                    modified_date,
                    modified_by,
                    test_type,
                    protocol,
                    url,
                    enabled,
                    alerts,
                    " ",
                    " ",
                    " ",
                )


if __name__ == "__main__":
    get_tests_information(USERNAME, BASIC_TOKEN, AID)
