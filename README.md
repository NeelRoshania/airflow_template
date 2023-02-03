# airflow_template
A template for managing workflows that require programmatic authoring, scheduling and monitoring 

### Usage
1. TBD

### Installation guide

**Module setup**
1. `python3 -m venv .env` and `pip3 install --upgrade pip` 
2. `source .env/bin/activate` then `sudo chmod 774 setup.sh`
3. Modify `setup.cfg` and `src`
4. `pip3 install -e .`
5. `./setup.sh`
6. `airflow info` (CLI should be available if your virtual environment is activated)
7. `airflow cheat-sheet` for general CLI guidance

**POSTGRESQL backend setup**
1. [Create database, user and grant privaleges to airflow](https://airflow.apache.org/docs/apache-airflow/stable/howto/set-up-database.html#setting-up-a-postgresql-database)
2. Modify `pg_hba.conf` to authenticate airflow user
3. Restart postgres server, `sudo service postgresql restart`
4. Initialize database `airflow db init` then `airflow db check`
5. `airflow db shell` to log into airflow database to confirm tables created

**Starting the webserver**
1. `airflow users create --help` to [create a user](https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/security/webserver.html#web-authentication) for UI access
2. `airflow webserver --port 8080` to start the web server
3. Open browser, navigate to `http://localhost:8080/` to access to UI

**Jupyter kernel setup**
1. `jupyter kernelspec uninstall .example_env` - remove existing kernels called .example_env
2. `python3 -m ipykernel install --user --name=.example_env`- install new kernel

**Environment & application setup**
1. `pytest -v`
2. `pytest tests/scripts/test_requestservices.py > tests/test_outcomes/010123` to dump results to file. Use `grep` to search through dump

### Repository setup

1. Authenticate with github 
    - SSH Agent
        - `eval "$(ssh-agent -s)"` to start agent 
        - `ssh-add -l` to check for existing keys
        - `ssh-add ~/.ssh/id_ed25519` to add SSH private key to ssh-agen
    - Test connection & authenticate, 
        - `ssh -T git@github.com`. See [Github SSH Authentication](https://docs.github.com/en/authentication).
2. Authentication troubleshooting
    - [Permission denied (publickey)](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)

### Server navigation

1. Access Airflow UI: port forward server to `http://localhost:8082/home` 
    - `aws ssm start-session --target [instance_id] --region us-west-2 --document-name AWS-StartPortForwardingSession --parameters '{"portNumber":["8080"], "localPortNumber":["8082"]}'`
2. SSM into server
    - `aws ssm start-session --target [instance_id] --region us-west-2`
    - switcher to user


### References
- Airflow
    - [Apache Airflow](https://airflow.apache.org/)
    - [Quick start](https://airflow.apache.org/docs/apache-airflow/stable/start.html)
    - [Installation](https://airflow.apache.org/docs/apache-airflow/stable/installation/installing-from-pypi.html)
    - [Set up database backend](https://airflow.apache.org/docs/apache-airflow/stable/howto/set-up-database.html)
- AWS
    - [CLI installation](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
    - [SSM installation](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html#install-plugin-debian)
