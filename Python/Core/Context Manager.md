### What Is a Context Manager?
A **context manager** is a construct that handles the setup and teardown of resources automatically. It’s most commonly used with the `with` statement.
```python
with open('file.txt', 'r') as f:
    data = f.read()
# File is automatically closed here
```
This ensures the file is closed even if an error occurs during reading.
### Why Use Context Managers?

- **Automatic cleanup**: Frees resources like files, sockets, or DB connections.
- **Exception-safe**: Cleanup happens even if an error is raised.
- **Cleaner code**: Replaces verbose `try-finally` blocks.
- **Custom control**: You can manage any resource using `__enter__` and `__exit__` methods.

### Real-World Use Cases

- **File handling**: `open()`
- **Database connections**: `psycopg2.connect()`
- **Thread locks**: `threading.Lock()`
- **Web scraping**: Closing browser sessions
- **Socket programming**: Managing open sockets
- **Subprocesses**: Cleaning up child processes

### Custom Context Manager with Exception Handling
```python
class SafeDivision:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __enter__(self):
        print("Entering context: preparing to divide")
        return self

    def divide(self):
        print("➗ Performing division")
        return self.a / self.b

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            print(f"Exception occurred: {exc_value}")
        print("Exiting context: cleaning up")
        # Suppress exception if handled
        return True  # Change to False to propagate exception
```
### Usage with Explanation

#### Case 1: No Exception
```python
with SafeDivision(10, 2) as sd:
    result = sd.divide()
    print(f"Result: {result}")
```
**Execution Flow:**
1. `__init__` is called → sets `a = 10`, `b = 2`
2. `__enter__` is called → prints "Entering context"
3. `divide()` is called → prints "Performing division"
4. `__exit__` is called → prints "Exiting context"
#### Case 2: With Exception (division by zero)
```python
with SafeDivision(10, 0) as sd:
    result = sd.divide()
    print(f"Result: {result}")
```
**Execution Flow:**
1. `__init__` is called → sets `a = 10`, `b = 0`
2. `__enter__` is called → prints "Entering context"
3. `divide()` raises `ZeroDivisionError`
4. `__exit__` is called → catches exception, prints it
5. Exception is **suppressed** because `__exit__` returns `True`

### Summary of Method Calls

| Method         | When It’s Called                          |
|----------------|--------------------------------------------|
| `__init__`     | When the context manager object is created |
| `__enter__`    | At the start of the `with` block           |
| `divide()`     | Inside the `with` block                    |
| `__exit__`     | At the end of the `with` block or on error |
