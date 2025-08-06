### Types of Windows in PySpark Structured Streaming

#### 1. **Tumbling Windows**
- Fixed-size, non-overlapping windows.
- Each event belongs to exactly one window.

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import window, col

spark = SparkSession.builder.appName("TumblingWindowExample").getOrCreate()

df = spark.readStream.format("socket").option("host", "localhost").option("port", 9999).load()
df = df.withColumn("timestamp", current_timestamp())

windowedCounts = df.groupBy(window(col("timestamp"), "10 minutes")).count()

query = windowedCounts.writeStream.outputMode("complete").format("console").start()
query.awaitTermination()
```

#### 2. **Sliding Windows**
- Fixed-size windows that slide at a specified interval.
- Events can belong to multiple overlapping windows.

```python
windowedCounts = df.groupBy(window(col("timestamp"), "10 minutes", "5 minutes")).count()
```

#### 3. **Session Windows**
- Windows based on user activity sessions.
- A session window closes after a period of inactivity.

```python
from pyspark.sql.functions import session_window

sessionized = df.groupBy(session_window(col("timestamp"), "30 minutes")).count()
```
