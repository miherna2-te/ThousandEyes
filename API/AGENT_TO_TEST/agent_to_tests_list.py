import requests
from rich.console import Console
from rich.table import Table
from getpass import getpass


table = Table(title="Agents - Tests List")
table.add_column("TEST NAME", justify="left", style="cyan", no_wrap=True)
table.add_column("TEST ID", style="magenta")
table.add_column("TEST TYPE", justify="left", style="green")
table.add_column("AGENT #1", justify="left", style="green")
table.add_column("AGENT #2", justify="left", style="green")
table.add_column("AGENT #3", justify="left", style="green")
table.add_column("AGENT #4", justify="left", style="green")


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

    agents_list = []
    for index in range(4):
        try:
            agent = agents_in_test[index]
            agent_name = agent.get("agentName")
            agents_list.append(agent_name)
        except (IndexError, TypeError):
            agents_list.append(None)

    table.add_row(
        test_name,
        test_id,
        test_type,
        agents_list[0],
        agents_list[1],
        agents_list[2],
        agents_list[3],
    )

console = Console()
console.print(table)