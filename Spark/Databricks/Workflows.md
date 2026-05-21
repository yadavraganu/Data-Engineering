### Passing Values Between Notebook Tasks
Use the taskValues subutility to dynamically push a value from one upstream task and pull it into any downstream task. [1] 
#### 1. Push a value (Upstream Task)
```python
# Max size: 48 KB. Must be JSON serializable (string, number, boolean).
dbutils.jobs.taskValues.set(key="status_flag", value="RUN_PIPELINE")
dbutils.jobs.taskValues.set(key="row_count", value=1500)
```
#### 2. Pull a value (Downstream Task)
```python
flag = dbutils.jobs.taskValues.get(taskKey="data_prep", key="status_flag", default="SKIP")
```
#### 3. SQL Notebook / Task Parameter UI:
```sql
SELECT * FROM silver_table WHERE row_count > {{tasks.data_prep.values.row_count}}
```
### Passing the job parameter to the task's parameter
Reference the job parameter inside the task's parameter field using the syntax ``{{job.parameters.<JOB_PARAM_NAME>}}``.
