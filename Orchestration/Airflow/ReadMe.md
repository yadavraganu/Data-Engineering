# Defining DAGS
Airflow 3 offers three first-class patterns for declaring DAGs. Each style has its own ergonomics and use cases:

### 1. Context Manager (`with DAG(...) as dag:`)

You wrap your task definitions inside a `with` block. Anything instantiated inside inherits that DAG automatically.

```python
from airflow.sdk import DAG
from airflow.providers.standard.operators.empty import EmptyOperator
import datetime

with DAG(
    dag_id="my_context_dag",
    start_date=datetime.datetime(2025, 1, 1),
    schedule="@daily",
) as dag:
    
    t1 = EmptyOperator(task_id="task_1")
    t2 = EmptyOperator(task_id="task_2")
    t1 >> t2
```

- Pros:  
  - Extremely concise  
  - No need to pass `dag=` everywhere  
- Cons:  
  - Harder to reference the DAG object outside the block  

### 2. Explicit Constructor + Passing `dag` to Tasks

You create a DAG instance, assign it to a variable, then pass that to each operator.

```python
from airflow.sdk import DAG
from airflow.providers.standard.operators.empty import EmptyOperator
import datetime

my_dag = DAG(
    dag_id="my_explicit_dag",
    start_date=datetime.datetime(2025, 1, 1),
    schedule="@daily",
)

t1 = EmptyOperator(task_id="task_1", dag=my_dag)
t2 = EmptyOperator(task_id="task_2", dag=my_dag)
t1 >> t2
```

- Pros:  
  - DAG object is readily available for imports or external tooling  
  - Clear separation of definition and wiring  
- Cons:  
  - Slightly more verbose  

### 3. `@dag` Decorator (TaskFlow API)

You decorate a function that instantiates tasks; calling the function at the bottom registers the DAG.

```python
from airflow.sdk import dag, task
from airflow.providers.standard.operators.empty import EmptyOperator
import datetime

@dag(
    dag_id="my_decorated_dag",
    start_date=datetime.datetime(2025, 1, 1),
    schedule="@daily",
)
def generate_workflow():
    t1 = EmptyOperator(task_id="task_1")
    t2 = EmptyOperator(task_id="task_2")
    t1 >> t2

generate_workflow()
```
- Pros:  
  - Enforces Pythonic structure  
  - Makes it easy to factor out common subgraphs as functions  
- Cons:  
  - Decorator syntax can hide the DAG object if you need to introspect it

# xCom
XComs, which stands for "cross-communication," are a mechanism in Airflow that allows tasks to exchange small amounts of data. They're primarily used to pass information from one task to another within the same DAG run.

## How XComs Work

An XCom is essentially a key-value store. When a task "pushes" an XCom, it stores a value associated with a key, a task ID, and a DAG ID in Airflow's metadata database. When another task "pulls" an XCom, it retrieves this stored value using the key and task ID.

  * **Pushing an XCom:** By default, the return value of a `PythonOperator`'s `python_callable` is automatically pushed to XCom. You can also explicitly push an XCom using the `xcom_push()` method in a task's context.
  * **Pulling an XCom:** You can retrieve an XCom's value using the `xcom_pull()` method. This is typically done within the `op_kwargs` of a downstream task.

The XCom data is stored in the Airflow database, so it's only suitable for small payloads (e.g., file paths, IDs, or short JSON strings). It's not designed for passing large datasets.

## Key Parameters and Methods

| Parameter/Method | Description |
| :--- | :--- |
| `xcom_push(key, value)` | Pushes a value to XCom with the specified key. The `value` can be any JSON-serializable object. |
| `xcom_pull(task_ids, key)` | Pulls a value from XCom. `task_ids` can be a single string or a list of task IDs. `key` is the key of the XCom to retrieve. |
| `do_xcom_push` | A boolean parameter for operators. If `False`, it prevents the task's return value from being pushed to XCom. The default is `True`. |

## Example

Let's illustrate with a simple example where one task generates a report filename and another task uses that filename.

```python
from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id='xcom_example',
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
    catchup=False
) as dag:
    
    def generate_report_filename():
        # This function returns a string, which is automatically pushed to XCom
        return f"/tmp/report_{datetime.now().strftime('%Y%m%d')}.csv"

    def print_filename(**kwargs):
        # The 'ti' (task instance) object is used to pull the XCom value
        ti = kwargs['ti']
        filename = ti.xcom_pull(task_ids='generate_filename_task')
        print(f"The report filename is: {filename}")

    generate_filename_task = PythonOperator(
        task_id='generate_filename_task',
        python_callable=generate_report_filename
    )

    print_filename_task = PythonOperator(
        task_id='print_filename_task',
        python_callable=print_filename
    )

    # The tasks are executed sequentially
    generate_filename_task >> print_filename_task
```
### Best Practices

  * **Small Payloads Only:** XComs are not a substitute for a shared file system or a database. Only use them for small, lightweight data.
  * **Default `return_value` Key:** When an operator returns a value, it's pushed with the key `return_value`. You can specify a different key with `xcom_push(key='my_custom_key', ...)`.
  * **Avoid Over-Reliance:** If your tasks need to share large amounts of data, consider writing the data to an external location (like a shared S3 bucket or a database table) and only using XCom to pass the pointer (e.g., the file path or database ID) to the downstream tasks.
# Common Airlow Params
Airflow has a rich set of parameters that you can use to configure every aspect of your workflows, from high-level DAG properties to the specific behavior of individual tasks. These parameters can be set in different places, with a clear order of precedence.

Here is a comprehensive, category-wise list of key Airflow parameters.

## 1. DAG-Level Parameters

These parameters are defined when you instantiate the `DAG` object and control the overall behavior of the workflow.

| Parameter | Description |
| :--- | :--- |
| `dag_id` | A unique string identifier for the DAG. Required. |
| `start_date` | The `datetime` object indicating when the DAG should begin scheduling. It's a best practice to use a fixed, non-dynamic date. |
| `end_date` | The `datetime` object after which the DAG should stop being scheduled. Defaults to `None`. |
| `schedule_interval` | A cron expression or `timedelta` object that defines how often the DAG should run. Examples: `'@daily'`, `'0 0 * * *'`, `timedelta(hours=1)`. |
| `default_args` | A dictionary of parameters that are inherited by all tasks in the DAG. This is a crucial way to keep your DAG code clean and consistent. |
| `catchup` | A boolean. If `True`, the scheduler will backfill any missed DAG runs between the `start_date` and the current date. Defaults to `True` but is often set to `False` in development. |
| `tags` | A list of strings used to categorize and filter DAGs in the Airflow UI. |
| `max_active_tasks` | The maximum number of task instances allowed to run concurrently for a single DAG run. |
| `max_active_runs` | The maximum number of active DAG runs allowed to run concurrently for this DAG. |
| `dagrun_timeout` | The maximum time a DAG run is allowed to be in a running state. If exceeded, the DAG run fails. |
| `on_success_callback` | A function to be called when a DAG run succeeds. |
| `on_failure_callback` | A function to be called when a DAG run fails. |
| `params` | A dictionary of DAG-level parameters. These can be defined in the UI and are accessible to tasks via the `params` context variable. |
| `render_template_as_native_obj` | A boolean that, when set to `True`, renders Jinja templates as native Python objects instead of strings. |

## 2. Task-Level Parameters (Common to all Operators)

These parameters are part of the `BaseOperator` class and can be set for individual tasks or defined in `default_args` to be applied to all tasks in a DAG.

| Parameter | Description |
| :--- | :--- |
| `task_id` | A unique, meaningful ID for the task within the DAG. Required. |
| `owner` | The owner of the task, useful for logging and notifications. |
| `retries` | The number of times a failed task will be automatically retried. |
| `retry_delay` | The `timedelta` object representing the delay between retries. |
| `retry_exponential_backoff` | A boolean. If `True`, the retry delay will increase exponentially with each retry. |
| `email` | A list of email addresses to send notifications to. |
| `email_on_failure` | A boolean. If `True`, an email is sent when the task fails. |
| `email_on_retry` | A boolean. If `True`, an email is sent when the task is retried. |
| `depends_on_past` | A boolean. If `True`, a task instance will only run if the previous instance of the *same task* (in the previous DAG run) was successful. |
| `wait_for_downstream` | A boolean. If `True`, a task will wait for its downstream tasks from the previous DAG run to complete successfully before it starts. |
| `execution_timeout` | The maximum allowed runtime for a task instance. If exceeded, the task will be marked as failed. |
| `pool` | The name of a resource pool to which the task belongs. Useful for limiting the number of simultaneous task runs across different DAGs. |
| `queue` | The name of the queue to which the task should be submitted for execution. Only applicable with certain executors like `CeleryExecutor` and `KubernetesExecutor`. |
| `priority_weight` | An integer representing the task's priority. The scheduler will prioritize tasks with higher `priority_weight` when resources are limited. |
| `trigger_rule` | The rule that determines when a task instance should run, based on the state of its upstream tasks. The default is `'all_success'`. Other options include `'all_done'`, `'one_success'`, `'none_failed'`, and more. |

## 3. Operator-Specific Parameters

Each operator has its own set of parameters tailored to its function. These are defined when you instantiate the specific operator.

#### `BashOperator`
* `bash_command`: The bash command to execute.

#### `PythonOperator`
* `python_callable`: The Python function to call.
* `op_args`: A list of positional arguments to pass to `python_callable`.
* `op_kwargs`: A dictionary of keyword arguments to pass to `python_callable`.

#### `ExternalTaskSensor`
* `external_dag_id`: The ID of the external DAG to monitor.
* `external_task_id`: The ID of the external task to monitor.
* `poke_interval`: The time in seconds between each check.
* `timeout`: The maximum time in seconds to wait for the external task.

## 4. Airflow Configuration Parameters

These are not set in the DAG file but in the global `airflow.cfg` file or via environment variables. They affect the entire Airflow instance.

| Parameter | Description |
| :--- | :--- |
| `parallelism` | The maximum number of task instances that can run concurrently across the entire Airflow instance. |
| `dag_concurrency` | The maximum number of task instances that can run concurrently by the scheduler. |
| `max_active_runs_per_dag` | The maximum number of concurrent active DAG runs for each individual DAG. |
| `executor` | The executor class that Airflow should use (e.g., `LocalExecutor`, `CeleryExecutor`, `KubernetesExecutor`). |
| `dags_folder` | The path to the directory where DAG files are stored. |
| `sql_alchemy_conn` | The database connection string for Airflow's metadata database. |
