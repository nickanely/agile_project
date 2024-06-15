import pendulum
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator, BranchPythonOperator

from image_loader import load_image
from quote_loader import load_quote
from teams_notifier import send_to_teams

DATES_TO_SKIP = ["11.06", "13.06", "15.06", "25.06", ]


def check_skip_date(**kwargs):
    execution_date = kwargs["execution_date"].format("DD.MM")
    if execution_date in DATES_TO_SKIP:
        return "skip_message"
    else:
        return "send_to_teams"


with DAG(
        dag_id="agile_project_MSI_7",
        description="A simple DAG to send daily quote with image to Teams",
        start_date=pendulum.today(),
        schedule_interval="@daily",
        catchup=False,
) as dag:
    start = EmptyOperator(
        task_id="start",
    )

    load_quote_task = PythonOperator(
        task_id="load_quote",
        provide_context=True,
        python_callable=load_quote,
    )

    load_image_task = PythonOperator(
        task_id="load_image",
        provide_context=True,
        python_callable=load_image,
    )

    check_skip_date_task = BranchPythonOperator(
        task_id="check_skip_date",
        provide_context=True,
        python_callable=check_skip_date,
    )

    send_to_teams_task = PythonOperator(
        task_id="send_to_teams",
        provide_context=True,
        python_callable=send_to_teams,
    )
    skip_message = EmptyOperator(
        task_id="skip_message",
    )
    end = EmptyOperator(
        task_id="end",
    )

start >> [load_quote_task, load_image_task] >> check_skip_date_task
check_skip_date_task >> [send_to_teams_task, skip_message]
send_to_teams_task >> end
skip_message >> end
