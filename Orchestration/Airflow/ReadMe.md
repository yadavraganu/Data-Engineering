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
