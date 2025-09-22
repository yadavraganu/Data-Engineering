## **Types of Attributes**

Attributes are variables associated with a class or instance.

### 1. **Instance Attributes**
Defined inside the `__init__` method and tied to a specific object.
```python
class Car:
    def __init__(self, brand):
        self.brand = brand  # instance attribute
```

### 2. **Class Attributes**
Shared across all instances of the class.
```python
class Car:
    wheels = 4  # class attribute
```

### 3. **Private Attributes**
Prefixed with double underscore `__`, not truly private but name-mangled.
```python
class Car:
    def __init__(self):
        self.__engine = "V8"
```

### 4. **Protected Attributes**
Prefixed with a single underscore `_`, meant for internal use.
```python
class Car:
    def __init__(self):
        self._mileage = 10000
```

## **Types of Methods**

Methods are functions defined inside a class.

### 1. **Instance Methods**
Operate on instance data. First parameter is always `self`.
```python
class Car:
    def drive(self):
        print("Driving")
```

### 2. **Class Methods**
Operate on class-level data. First parameter is `cls`. Use `@classmethod` decorator.
```python
class Car:
    count = 0

    @classmethod
    def increment_count(cls):
        cls.count += 1
```

### 3. **Static Methods**
Don’t access instance or class data. Use `@staticmethod` decorator.
```python
class Car:
    @staticmethod
    def honk():
        print("Beep!")
```
