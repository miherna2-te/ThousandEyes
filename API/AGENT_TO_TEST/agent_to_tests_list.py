import requests
import csv
from rich.console import Console
from rich.table import Table
from getpass import getpass

###########################################################################
# Setting up the parameters for printing in the console with ricn module
###########################################################################
table = Table(title="Agents - Tests List")
table.add_column("TEST NAME", justify="left", style="cyan", no_wrap=True)
table.add_column("TEST ID", style="magenta")
table.add_column("TEST TYPE", justify="left", style="green")
table.add_column("AGENTS", justify="left", style="green")

###########################################################################
# Requesting the user to type email and Basic Authentication Token
###########################################################################
username = input("Email: ")
api_key = getpass("Basic Authentication Token: ")
headers = {"content-type": "application/json"}

###########################################################################
# Getting all the tests configured in the account
###########################################################################
TESTS_API = requests.get(
    "https://api.thousandeyes.com/v6/tests.json",
    headers=headers,
    auth=(username, api_key),
)

###########################################################################
# Getting the information in JSON and extracting the key test
###########################################################################
ALL_TESTS_CONFIGURED = TESTS_API.json()
ALL_TESTS_CONFIGURED = ALL_TESTS_CONFIGURED.get("test")

###########################################################################
# Generating the CSV file and its headers
###########################################################################
with open('tests_to_agents.csv', mode='w') as csv_file:
    fieldnames = ['TESTNAME', 'TESTID', 'TESTTYPE', 'AGENTS']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    
    ###########################################################################
    # Walking through the tests list and getting and name and ID for each test
    ###########################################################################
    for test in ALL_TESTS_CONFIGURED:
        test_name = test.get("testName")
        test_id = str(test.get("testId"))
        ###########################################################################
        # The ID is used in a new API call to get the agents
        ###########################################################################
        tests_details = requests.get(
            f"https://api.thousandeyes.com/v6/tests/{test_id}.json",
            headers=headers,
            auth=(username, api_key),
        ).json()
        test_type = tests_details.get("test")[0].get("type")
        agents_in_test = tests_details.get("test")[0].get("agents", None)
        ###########################################################################
        # Saving the agent list in different format for csv file and console
        ###########################################################################
        agents_list = ""
        agents_csv = ""
        ###########################################################################
        # If agents is not empty, iterate through the list and get name
        ###########################################################################
        if agents_in_test != None:
            for agent in agents_in_test:
                agent_name = agent.get("agentName")
                agents_list += f"{agent_name}\n"
                agents_csv += agent_name + " - "
        ###########################################################################
        # Formatting the output fo the console and writes in the CSV file
        ###########################################################################
        writer.writerow({'TESTNAME': test_name , 'TESTID': test_id, 'TESTTYPE': test_type, 'AGENTS': agents_csv})
        table.add_row(test_name, test_id, test_type, agents_list)

    ###########################################################################
    # Prints out to the console 
    ###########################################################################
    console = Console()
    console.print(table)
