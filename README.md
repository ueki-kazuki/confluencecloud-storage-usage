

# ORIGINAL
- [Finding storage usage of Confluence space and page using REST API | Confluence | Atlassian Documentation](https://confluence.atlassian.com/confkb/finding-storage-usage-of-confluence-space-and-page-using-rest-api-1063555292.html)

# HOW TO SETUP

- Crate API Token [Manage API tokens for your Atlassian account | Atlassian Support](https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/)

- Install python modules
- Save token into `.env` file
```
$ pipenv install
$ pipenv shell
$ cp .env.sample .env
$ edit .env
```

# Usage
- Run the script.
```
$ python app.py

(output per_space.csv and per_page.csv)
```

- Import CSV files to MS-Excel and Google Spreadsheet
- Have a fun!