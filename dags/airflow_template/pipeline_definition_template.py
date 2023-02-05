from datetime import datetime, timedelta
from textwrap import dedent

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG
from airflow.models import dag

# Operators; we need this to operate!
from airflow.operators.bash import BashOperator

"""
    DAG definition file
    
    References
        - DAGS
            - https://airflow.apache.org/docs/apache-airflow/stable/tutorial/fundamentals.html#instantiate-a-dag
            - https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html

        - Tasks
            - https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/tasks.html
        
        - Best practices
            - Avoid unnecesary top level python code. DAGs should resolve in seconds, not minutes
                - Import modules within tasks
                - https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html#top-level-python-code 

        - Test your DAGS

            To debug DAGs in an IDE, 
                - You can set up the dag.test command in your dag file and run through your DAG in a single serialized python process.
                - https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/executor/debug.html

            Ensure no syntax errors - run the python script

            Measure  “real time” to process DAG
                time python dags/pipeline_definition_tempate.py
                https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html#testing-a-dag

            Command Line Metadata Validation, https://airflow.apache.org/docs/apache-airflow/stable/tutorial/fundamentals.html#testing
                airflow db init # initialize the database tables
                airflow dags list # print the list of active DAGs
                airflow tasks list tutorial # prints the list of tasks in the "tutorial" DAG
                airflow tasks list tutorial --tree # prints the hierarchy of tasks in the "tutorial" DAG
"""

# instantiate the DAG
with DAG(
    "pipeline_definition_template",
    # These args will get passed on to each operator
    # You can override them on a per-task basis during operator initialization
    default_args={
        "depends_on_past": False,
        "email": ["airflow@example.com"],
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
        # 'queue': 'bash_queue',
        # 'pool': 'backfill',
        # 'priority_weight': 10,
        # 'end_date': datetime(2016, 1, 1),
        # 'wait_for_downstream': False,
        # 'sla': timedelta(hours=2),
        # 'execution_timeout': timedelta(seconds=300),
        # 'on_failure_callback': some_function,
        # 'on_success_callback': some_other_function,
        # 'on_retry_callback': another_function,
        # 'sla_miss_callback': yet_another_function,
        # 'trigger_rule': 'all_success'
    },
    description="This a pipeline definition template or a DAG definition file",
    schedule=timedelta(days=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["example"],
) as dag:

    # t1, t2 and t3 are examples of tasks created by instantiating operators
    t1 = BashOperator(
        task_id="print_date",
        bash_command="date",
    )

    t2 = BashOperator(
        task_id="sleep",
        depends_on_past=False,
        bash_command="sleep 5",
        retries=3,
    )
    t1.doc_md = dedent(
        """\
    #### Task Documentation
    You can document your task using the attributes `doc_md` (markdown),
    `doc` (plain text), `doc_rst`, `doc_json`, `doc_yaml` which gets
    rendered in the UI's Task Instance Details page.
    ![img](http://montcs.bloomu.edu/~bobmon/Semesters/2012-01/491/import%20soul.png)
    **Image Credit:** Randall Munroe, [XKCD](https://xkcd.com/license.html)
    """
    )

    dag.doc_md = __doc__  # providing that you have a docstring at the beginning of the DAG; OR
    dag.doc_md = """
    This is a documentation placed anywhere
    """  # otherwise, type it like this
    templated_command = dedent(
        """
    {% for i in range(5) %}
        echo "{{ ds }}"
        echo "{{ macros.ds_add(ds, 7)}}"
    {% endfor %}
    """
    )

    t3 = BashOperator(
        task_id="templated",
        depends_on_past=False,
        bash_command=templated_command,
    )

    # define sequence of tasks
    t1 >> [t2, t3]

# testing
if __name__ == "__main__":
    dag.test()