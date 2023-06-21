# ThousandEyes Tests URL Information

This script analyzes the tests for each account group in ThousandEyes and provides the test's identifier, name and url for each entry.

## Usage

To run the script, execute the following command:

```bash
python tests_url.py
```

## Requirements

The script requires the following Python packages:

- `csv`
- `re`
- `requests`
- `getpass`

These packages can be installed using pip:

```bash
pip install csv re requests
```

## Configuration

Before running the script, you need to provide your authentication details:

1. When prompted, enter your ThousandEyes username.
2. When prompted, enter your ThousandEyes basic authentication token. The token will not be visible during input.

## Function Documentation

### `get_accounts(username, token)`

Retrieves account information from the ThousandEyes API and returns a dictionary mapping account IDs to account names.

#### Parameters

- `username` (str): The username for authentication.
- `token` (str): The basic authentication token.

#### Returns

- `dict`: A dictionary mapping account IDs (`aid`) to account names (`Account Group Name`).

#### Raises

- `requests.exceptions.RequestException`: If there was an error making the API request.

### `get_tests(username, token, aid)`

Retrieves tests information from the ThousandEyes API for a specific account ID and returns a dictionary with the details of each test.

#### Parameters

- `username` (str): The username for authentication.
- `token` (str): The basic authentication token.
- `aid` (str): The account ID for which test information is to be retrieved.

#### Returns

- `dict`: A dictionary with the test information.

#### Raises

- `requests.exceptions.RequestException`: If there was an error making the API request.

### `get_tests_url(username, token, accounts)`

Retrieves test URL information for all the accounts and writes the data to a CSV file.

#### Parameters

- `username` (str): The username used for authentication.
- `token` (str): The authentication token.
- `accounts` (list): A list of account IDs for which test information is to be retrieved.

#### Returns

- None

#### File Output

The function writes the test name, test id and URL information to a CSV file named "tests_url.csv". The file is created in the current directory. If a file with the same name already exists, it will be overwritten.

## Author

Miguel Hernandez

## Date

June 21, 2023
