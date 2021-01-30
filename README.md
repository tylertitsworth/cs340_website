# Getting Started
After fetching all of the necessary files from the master branch and verifying that you have python3 and pip installed in your current terminal session, run the following commands in the root directory:

`python3 -m venv venv`

`source venv/bin/activate`

`pip install -r requirements.txt`

Afterwards, acquire the `config.py` `database_config.py` files from your development administrator and place them in the `/app` directory. This in order to access the mariaDB session hosted on the `engr` domain.

To sync your database instance with the current run the following commands in the root directory:

`flask db init`

`flask db migrate`

Any time you make a change to the `app/models.py` file you need to run `flask db migrate` followed by `flask db upgrade`. In the event that upgrade fails, contact your development administrator.

To run the project you simply invoke `flask run` and browse to `localhost:5000`.
