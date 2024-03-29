# airflow_template
A template for managing workflows that require programmatic authoring, scheduling and monitoring.

### Usage
1. Define and test your dags in `~/git/airflow_template/dags`, then upload to `~/airflow/dags/airflow_template`

### Installation guide

**Module setup**
1. `python3 -m venv .env` and `pip3 install --upgrade pip` 
2. `source .env/bin/activate`
3. `sudo chmod 774 setup.sh` then `./setup.sh`
4. `pip3 install -e .`
5. `airflow info` (CLI should be available if your virtual environment is activated)
6. `airflow cheat-sheet` for general CLI guidance

Windows installation
1. `python3 -m venv .env` and `pip3 install --upgrade pip` 
2. Activate `.env`
3. `pip3 install "apache-airflow[postgres]==2.5.1" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.5.1/constraints-3.9.txt"`
4. Modify `setup.cfg` and `src`
5. `pip3 install -e .`

**PostgreSQL backend setup**
1. [Create database, user and grant privaleges to airflow](https://airflow.apache.org/docs/apache-airflow/stable/howto/set-up-database.html#setting-up-a-postgresql-database)
2. Modify `etc/postgresql/14/main/pg_hba.conf` to [authenticate](https://www.postgresql.org/docs/current/auth-pg-hba-conf.html) the airflow user
3. Restart postgres server, `sudo service postgresql restart`
4. Define SqlAlchemy [connection string](https://airflow.apache.org/docs/apache-airflow/stable/howto/set-up-database.html#setting-up-a-postgresql-database) in `~/airflow/airflow.cfg`
    - `postgresql+psycopg2://airflow_user:airflow_pass@localhost/airflow_db`
5. Initialize database `airflow db init` then `airflow db check`
6. `airflow db shell` to log into airflow database to confirm tables created

**Setup the webserver**
1. `airflow users create --help` to [create a user](https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/security/webserver.html#web-authentication) for UI access
2. `airflow webserver --port 8080` to start the web server
3. Open browser, navigate to `http://localhost:8080/` to access to UI
4. If using `screen`, ensure `AIRFLOW_HOME` is pointing to correct `~/airflow/airflow.cfg`
    - check with `airflow info`
    - start a named screen session, `screen -S airflow-webserver`

**Setup the scheduler**
1. Recommended Executor, `LocalExecutor`
    - Change `executor` parameter in `~/airflow/airflow.cfg`
2. `airflow info` to confirm intended [Executor](https://airflow.apache.org/docs/apache-airflow/2.5.1/core-concepts/executor/index.html)
3. `airflow scheduler`

**Usage instructions**
1. Ensure that the webserver and scheduler services are running.
2. The default dags directory is `~/airflow/dags`
    - Recommend that these dags be treated as production dags
    - Any testing should be done in `~/git/airflow_template/dags`
3. To disable tutorial dags, set `load_examples = False` in `~/airflow/airflow.cfg`
    - restart webserver and scheduler

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
    - Additional [sample IAM policies](https://docs.aws.amazon.com/systems-manager/latest/userguide/getting-started-restrict-access-examples.html) for Session Manager
2. SSM into server
    - `aws ssm start-session --target [instance_id] --region us-west-2`
    - switcher to user


### References
- Airflow
    - [Apache Airflow](https://airflow.apache.org/)
    - [Core concepts](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/index.html)
    - [Quick start](https://airflow.apache.org/docs/apache-airflow/stable/start.html)
    - [Installation](https://airflow.apache.org/docs/apache-airflow/stable/installation/installing-from-pypi.html)
    - [Set up database backend](https://airflow.apache.org/docs/apache-airflow/stable/howto/set-up-database.html)
    - PostgreSQL backend debugging
        - Check that the server is running, `service --status-all`. 
            - Restart if neccesary, `sudo service postgresql restart`
        - [Postgres + Airflow db: permission denied for schema public](https://stackoverflow.com/questions/74390647/postgres-airflow-db-permission-denied-for-schema-public)
    - Webserver debugging
        - [Error: Already running on PID XXXX](https://stackoverflow.com/questions/55729303/airflow-webserver-started-but-ui-doesnt-show-in-browser)
        - [airflow shell not initializing intended database](https://stackoverflow.com/questions/69093243/db-init-with-postgres-for-airflow)
    - UI debugging
        - `Do not use SequentialExecutor in production`
            - `airflow config get-value core executor` to confirm current Executor
            - Check `airflow.cfg` to see that inteded Executor has been defined
            - Restart the webserver
- AWS
    - [CLI installation](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
    - [SSM installation](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html#install-plugin-debian)
