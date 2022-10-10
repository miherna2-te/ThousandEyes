import requests
import csv
from rich.console import Console
from rich.table import Table
from getpass import getpass

table = Table(title="Agents - Tests List")
table.add_column("TEST NAME", justify="left", style="cyan", no_wrap=True)
table.add_column("TEST ID", style="magenta")
table.add_column("TEST TYPE", justify="left", style="green")
table.add_column("AGENTS", justify="left", style="green")

username = input("Email: ")
api_key = getpass("Token: ")
headers = {"content-type": "application/json"}

TESTS_API = requests.get(
    "https://api.thousandeyes.com/v6/tests.json",
    headers=headers,
    auth=(username, api_key),
)

ALL_TESTS_CONFIGURED = TESTS_API.json()
ALL_TESTS_CONFIGURED = ALL_TESTS_CONFIGURED.get("test")

with open('tests_to_agents.csv', mode='w') as csv_file:
    fieldnames = ['TESTNAME', 'TESTID', 'TESTTYPE', 'AGENTS']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    
    for test in ALL_TESTS_CONFIGURED:
        test_name = test.get("testName")
        test_id = str(test.get("testId"))
        tests_details = requests.get(
            f"https://api.thousandeyes.com/v6/tests/{test_id}.json",
            headers=headers,
            auth=(username, api_key),
        ).json()
        test_type = tests_details.get("test")[0].get("type")
        agents_in_test = tests_details.get("test")[0].get("agents", None)

        agents_list = ""
        agents_csv = ""
        if agents_in_test != None:
            for agent in agents_in_test:
                agent_name = agent.get("agentName")
                agents_list += f"{agent_name}\n"
                agents_csv += agent_name + " - "
        writer.writerow({'TESTNAME': test_name , 'TESTID': test_id, 'TESTTYPE': test_type, 'AGENTS': agents_csv})
        table.add_row(test_name, test_id, test_type, agents_list)


    console = Console()
    console.print(table)
