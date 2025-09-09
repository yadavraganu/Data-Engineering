# JSON

## Read Options

| Option Name                     | Description                                                                 | Example Usage                                      |
|--------------------------------|-----------------------------------------------------------------------------|---------------------------------------------------|
| `multiLine`                    | Set to `true` if JSON records span multiple lines (pretty-printed JSON).   | `.option("multiLine", True)`                      |
| `mode`                         | Controls error handling: `PERMISSIVE`, `DROPMALFORMED`, or `FAILFAST`.     | `.option("mode", "PERMISSIVE")`                   |
| `dropMalformed`                | Deprecated. Use `mode = DROPMALFORMED` instead.                            | `.option("mode", "DROPMALFORMED")`                |
| `primitivesAsString`           | Treat primitive types (int, float, etc.) as strings.                       | `.option("primitivesAsString", True)`             |
| `allowComments`                | Allows comments in JSON using `//`.                                        | `.option("allowComments", True)`                  |
| `allowUnquotedFieldNames`      | Allows field names without quotes.                                         | `.option("allowUnquotedFieldNames", True)`        |
| `allowSingleQuotes`            | Allows single quotes instead of double quotes.                             | `.option("allowSingleQuotes", True)`              |
| `allowNumericLeadingZeros`     | Allows numbers with leading zeros (e.g., `0123`).                          | `.option("allowNumericLeadingZeros", True)`       |
| `allowBackslashEscapingAnyCharacter` | Allows backslash escaping of any character.                        | `.option("allowBackslashEscapingAnyCharacter", True)` |
| `columnNameOfCorruptRecord`    | Stores malformed records in a specified column.                            | `.option("columnNameOfCorruptRecord", "_corrupt_record")` |
| `dateFormat`                   | Specifies custom date format for parsing date fields.                      | `.option("dateFormat", "yyyy-MM-dd")`             |
| `timestampFormat`              | Specifies custom timestamp format.                                         | `.option("timestampFormat", "yyyy-MM-dd HH:mm:ss")` |
| `encoding`                     | Specifies character encoding (e.g., `UTF-8`, `ISO-8859-1`).                | `.option("encoding", "UTF-8")`                    |
| `lineSep`                      | Specifies line separator for multi-line JSON.                              | `.option("lineSep", "\\n")`                       |

### Example Usage

```python
df = spark.read \
    .option("multiLine", True) \
    .option("mode", "PERMISSIVE") \
    .option("columnNameOfCorruptRecord", "_corrupt_record") \
    .json("/path/to/json/file")
```
## Functions

### 1. `from_json()`

**Description**: Parses a JSON string column into a structured format (struct or array).

```python
#  Input
json_str = '{"user_id":"u1","events":[{"event_type":"click","timestamp":"2023-01-01"}]}'

#  Output
# Struct(user_id='u1', events=[{'event_type': 'click', 'timestamp': '2023-01-01'}])

#  Usage
from pyspark.sql.functions import from_json
from pyspark.sql.types import StructType, StructField, StringType, ArrayType

schema = StructType([
    StructField("user_id", StringType()),
    StructField("events", ArrayType(
        StructType([
            StructField("event_type", StringType()),
            StructField("timestamp", StringType())
        ])
    ))
])

df.withColumn("parsed", from_json("json_str", schema))
```

### 2. `to_json()`

**Description**: Converts a struct or map column back into a JSON string.

```python
#  Input
# Struct(user_id='u1', events=[{'event_type': 'click', 'timestamp': '2023-01-01'}])

#  Output
json_str = '{"user_id":"u1","events":[{"event_type":"click","timestamp":"2023-01-01"}]}'

#  Usage
from pyspark.sql.functions import to_json
df.withColumn("json_str", to_json("parsed"))
```

### 3. `get_json_object()`

**Description**: Extracts a specific field from a JSON string using a JSONPath expression.

```python
#  Input
json_str = '{"user_id":"u1","events":[...]}'

#  Output
user_id = "u1"

#  Usage
from pyspark.sql.functions import get_json_object
df.withColumn("user_id", get_json_object("json_str", "$.user_id"))
```
### 4. `json_tuple()`

**Description**: Extracts multiple fields from a JSON string into separate columns.

```python
#  Input
json_str = '{"user_id":"u1","event_type":"click"}'

#  Output
user_id = "u1", event_type = "click"

#  Usage
from pyspark.sql.functions import json_tuple
df.select(json_tuple("json_str", "user_id", "event_type"))
```

# Array

### 1. `explode()`

**Description**: Converts each element of an array into a separate row.

```python
#  Input
events = [{"type":"click"}, {"type":"view"}]

#  Output
Row 1: type = click  
Row 2: type = view

#  Usage
from pyspark.sql.functions import explode
df.select(explode("events").alias("event"))
```

### 2. `posexplode()`

**Description**: Like `explode()`, but also includes the position (index) of each element.

```python
#  Input
events = [{"type":"click"}, {"type":"view"}]

#  Output
Row 1: pos = 0, type = click  
Row 2: pos = 1, type = view

#  Usage
from pyspark.sql.functions import posexplode
df.select(posexplode("events").alias("pos", "event"))
```

### 3. `arrays_zip()`

**Description**: Combines multiple arrays into a single array of structs.

```python
#  Input
names = ["Alice", "Bob"], ages = [25, 30]

#  Output
[{"names":"Alice", "ages":25}, {"names":"Bob", "ages":30}]

#  Usage
from pyspark.sql.functions import arrays_zip
df.withColumn("zipped", arrays_zip("names", "ages"))
```

### 4. `array_contains()`

**Description**: Checks if an array contains a specific value.

```python
#  Input
tags = ["spark", "json"]

#  Output
True (if "json" is searched)

#  Usage
from pyspark.sql.functions import array_contains
df.filter(array_contains("tags", "json"))
```

### 5. `size()`

**Description**: Returns the number of elements in an array.

```python
#  Input
tags = ["spark", "json"]

#  Output
2

# Usage
from pyspark.sql.functions import size
df.withColumn("tag_count", size("tags"))
```

### 6. `sort_array()`

**Description**: Sorts the elements of an array.

```python
#  Input
scores = [3, 1, 2]

#  Output
[1, 2, 3]

#  Usage
from pyspark.sql.functions import sort_array
df.withColumn("sorted_scores", sort_array("scores"))
```

### 7. `flatten()`

**Description**: Flattens nested arrays into a single array.

```python
#  Input
nested = [[1, 2], [3, 4]]

#  Output
[1, 2, 3, 4]

#  Usage
from pyspark.sql.functions import flatten
df.withColumn("flat_array", flatten("nested"))
```
