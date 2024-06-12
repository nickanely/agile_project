import pendulum
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from MSI_2.quote_loader import load_quote
from MSI_2.image_loader import load_image
from MSI_2.teams_notifier import send_to_teams


with DAG(
        dag_id="agile_project_MSI_2",
        description="A simple DAG to send daily quote with image to Teams",
        start_date=pendulum.today(),
        schedule_interval="@daily",
        catchup=False,
) as dag:
    start = EmptyOperator(
        task_id='start',
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

    send_to_teams_task = PythonOperator(
        task_id="send_to_teams",
        provide_context=True,
        python_callable=send_to_teams,
    )

    end = EmptyOperator(
        task_id='end',
    )

start >> [load_quote_task, load_image_task] >> send_to_teams_task >> end
