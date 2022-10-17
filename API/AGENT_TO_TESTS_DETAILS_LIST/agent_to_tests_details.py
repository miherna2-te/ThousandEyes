import requests
import csv
from getpass import getpass

#######################################################
# User needs to provide authentication parameters
#######################################################
USERNAME = input("Username: ")
BASIC_TOKEN = getpass("Basic Token: ")
HEADERS = {"content-type": "application/json"}

#######################################################
# This call returns all the tests configured
#  by the user, then the data is formatted in JSON.
#######################################################
TESTS_API = requests.get(
    "https://api.thousandeyes.com/v6/tests.json",
    headers=HEADERS,
    auth=(USERNAME, BASIC_TOKEN),
)

ALL_TESTS_CONFIGURED = TESTS_API.json()
ALL_TESTS_CONFIGURED = ALL_TESTS_CONFIGURED.get("test")

#######################################################
# Opening a CSV file and formatting its headers
#######################################################
with open("tests_to_agents_details.csv", mode="w") as CSV_FILE:
    FIELDS = [
        "TEST_NAME",
        "TEST_ID",
        "CREATED_BY",
        "CREATED",
        "MODIFIED",
        "MODIFIED_BY",
        "TEST_TYPE",
        "PROTOCOL",
        "URL",
        "ENABLED",
        "ALERTS",
        "AGENTS_NAME",
        "AGENT_TYPE",
        "SHARED",
    ]
    WRITER = csv.DictWriter(CSV_FILE, fieldnames=FIELDS)
    WRITER.writeheader()

    #######################################################
    # Getting multiple values, the test_id is used 
    # to make an additional call to the API and 
    # get additional information agents and if the test is shared
    #######################################################
    for test in ALL_TESTS_CONFIGURED:
        test_name = test.get("testName")
        test_id = test.get("testId")
        created_by = test.get("createdBy")
        created_date = test.get("createdDate")
        modified_date = test.get("modifiedDate")
        modified_by = test.get("modifiedBy")
        test_type = test.get("type")
        protocol = test.get("protocol")
        url = test.get("url")
        enabled = test.get("enabled")
        alerts = test.get("alertsEnabled")
        tests_details = requests.get(
            f"https://api.thousandeyes.com/v6/tests/{test_id}.json",
            headers=HEADERS,
            auth=(USERNAME, BASIC_TOKEN),
        ).json()
        #######################################################
        # The call returns nested data, therefore it is
        # required to walk down in the hierarchy using multiple
        # types of data to extract the intended value.
        # While doing this information the data
        # is saved in the same variable
        #######################################################
        test_type = tests_details.get("test")
        test_type = test_type[0].get("type")
        agents_in_test = tests_details.get("test")
        agents_in_test = agents_in_test[0].get("agents", None)
        shared_accounts = tests_details.get("test")
        shared_accounts = shared_accounts[0].get("sharedWithAccounts", None)
        shared_accounts = [account.get("name", None) for account in shared_accounts]
        shared_accounts = " - ".join(shared_accounts)
        #######################################################
        # Verifying if there are agents configured in the test
        #######################################################
        if agents_in_test != None:
            for agent in agents_in_test:
                agent_name = agent.get("agentName")
                agent_type = agent.get("agentType")
                WRITER.writerow(
                    {
                        "TEST_NAME": test_name,
                        "TEST_ID": test_id,
                        "CREATED_BY": created_by,
                        "CREATED": created_date,
                        "MODIFIED": modified_date,
                        "MODIFIED_BY": modified_by,
                        "TEST_TYPE": test_type,
                        "PROTOCOL": protocol,
                        "URL": url,
                        "ENABLED": enabled,
                        "ALERTS": alerts,
                        "AGENTS_NAME": agent_name,
                        "AGENT_TYPE": agent_type,
                        "SHARED": shared_accounts,
                    }
                )
        #######################################################
        # if there is NOT agents in the test the line
        # will print out the values with the exception
        # of the last three values: AGENTS_NAME,
        # AGENTS_TYPE and SHARED.
        #######################################################
        else:
            WRITER.writerow(
                {
                    "TEST_NAME": test_name,
                    "TEST_ID": test_id,
                    "CREATED_BY": created_by,
                    "CREATED": created_date,
                    "MODIFIED": modified_date,
                    "MODIFIED_BY": modified_by,
                    "TEST_TYPE": test_type,
                    "PROTOCOL": protocol,
                    "URL": url,
                    "ENABLED": enabled,
                    "ALERTS": alerts,
                    "AGENTS_NAME": "",
                    "AGENT_TYPE": "",
                    "SHARED": "",
                }
            )
