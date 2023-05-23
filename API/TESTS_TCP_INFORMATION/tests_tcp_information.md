# ThousandEyes Tests Information

This script allows you to analyze the tests for each account group in ThousandEyes and retrieve details about each test, including the test ID, test name, test type, protocol, probe method, and path trace settings. The script interacts with the ThousandEyes API to fetch the necessary information.

## Usage
To run the script, use the following command:

```
python test_info_excel.py
```

## Author
Miguel Hernandez

## Date
May 22, 2023

## Functionality
The script consists of the following main functions:

### get_accounts(username, token)
Retrieves account information from the ThousandEyes API and returns a dictionary that maps account IDs to account names.

#### Arguments
- username (str): The username for authentication.
- token (str): The basic authentication token.

#### Returns
- dict: A dictionary mapping account IDs (aid) to account names (Account Group Name).

### get_tests(username, token, aid)
Retrieves tests information from the ThousandEyes API for a specific account group (aid) and returns a dictionary with the details of each test.

#### Arguments
- username (str): The username for authentication.
- token (str): The basic authentication token.
- aid (str): The account ID (aid) of the account group.

#### Returns
- dict: A dictionary with test information.

## Execution
Upon running the script, it prompts for your username and basic token for authentication. The script then fetches the account information using the `get_accounts()` function and displays it.

A workbook is created to store the test information. The script generates a sheet named "ACCOUNTS" with the headers "AID" and "ACCOUNT_NAME". The headers are formatted with bold font and an orange background.

For each account group, the script retrieves the corresponding tests using the `get_tests()` function. It creates a sheet for each account group (named after the account identifier) and populates it with the test details, including the headers "TEST_ID", "TEST_NAME", "TEST_TYPE", "PROTOCOL", "PROBE", and "PATH_TRACE_MODE". Similar to the "ACCOUNTS" sheet, the headers in each account sheet are formatted with bold font and an orange background.

The final workbook is saved as "output.xlsx" containing the test information for all account groups.

Note: Ensure that the required libraries (`getpass`, `pprint`, `openpyxl`, and `requests`) are installed before running the script.

Feel free to reach out to the author, Miguel Hernandez (miherna2@cisco.com), for any questions or concerns.
