
from airflow import DAG
from airflow import version
from airflow.models import Variable
from airflow.exceptions import AirflowException
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.hooks.gcs_hook import GoogleCloudStorageHook
from airflow.contrib.operators.gcs_to_bq import GoogleCloudStorageToBigQueryOperator
from airflow.contrib.operators.bigquery_operator import BigQueryOperator

from airflow.utils.dates import days_ago

PROJECT_ID = Variable.get('project')
LANDING_BUCKET = Variable.get('landing_bucket')
BACKUP_BUCKET = Variable.get('backup_bucket')



default_arguments = {'owner': 'Amos Bunde', 'start_date':days_ago(0)}

def list_ob(bucket=None):
    hook = GoogleCloudStorageHook()
    storage_objects = hook.list(bucket)

    kwargs['ti'].xcom_push(value=storage_objects)


def move_objects(
    source_bucket=None,
    destination_bucket=None,
    prefix=None,
    **kwargs):

    storage_objects = kwargs['ti'].xcom_pull(task_id='list_files')

    hook = GoogleCloudStorageHook()

    for storage_object in storage_objects:
        destination_object = storage_object

        if prefix:
            destination_object = "{}/{}".format(prefix,storage_object)


        hook.copy(source_bucket, storage_object,destination_bucket)
        hook.delete(source_bucket,storage_object)

    



with DAG('loading_to_big_query',
    schedule_interval ='@daily', 
    catchup =False, 
    default_args= default_arguments,
    max_active_runs =1,
    user_defined_macros = {"project" : PROJECT_ID}) as dag:


        list_files = PythonOperator(
            task_id ='list_files',
            python_callable = list_ob,
            op_kwargs = {'bucket': LANDING_BUCKET}
        )

        loading_data = GoogleCloudStorageToBigQueryOperator(
            task_id = 'loading_data',
            bucket = LANDING_BUCKET,
            source_objects = ['*'],
            source_format='CSV',
            skip_leading_rows = 1,
            field_delimiter = ',',
            destination_project_dataset_table ='Veriff.veriff_iot_data.IoT_Indexed_Processed',
            create_disposition ='CREATE_IF_NEEDED',
            write_disposition = 'WRITE_APPEND',
            bigquery_conn_id = 'google_cloud_default',
            google_cloud_storage_conn_id= 'google_cloud_deafult'

        )

        query = '''
        SELECT * except (rank)
        FROM (
            SELECT 
               *,
               ROW_NUMBER() OVER (
                   PARTITION BY player ORDER BY Date DESC
               )as RANK
            FROM  'Veriff.all_players.players_details') as New
        WHERE rank=1    

        )
        '''

        create_table = BigQueryOperator(
            task_id = 'create_table',
            sql =query,
            destination_dataset_table = "{{ project }}.veriff_iot_data.Incremental_IOT_indexes",
            write_disposition = 'WRITE_TRUNCATE',
            create_disposition ='CREATE_IF_NEEDED',
            use_legacy_sql = False,
            location='europe-north1',
            bigquery_conn_id = 'google_cloud_deafult'

        )

         move_files = PythonOperator(
             task_id = 'move_files',
             python_callable = move_objects,
             op_kwargs = {"source_bucket": LANDING_BUCKET,
                          "destination_bucket ": BACKUP_BUCKET,
                          "prefix": "{{ts_nodash}}"},
             provide_context = True,             
         )

list_files >>loading_data >> create_table >> move_files
