# Basic pytest Setup
####  **1. Install `pytest`**
```bash
pip install pytest
```
#### **2. Project Structure Example**
```
my_project/
├── app/
│   └── calculator.py
├── tests/
│   └── test_calculator.py
└── requirements.txt
```
#### **3. Sample Code (`calculator.py`)**
```python
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b
```
#### **4. Sample Test (`test_calculator.py`)**
```python
from app.calculator import add, subtract

def test_add():
    assert add(2, 3) == 5

def test_subtract():
    assert subtract(5, 3) == 2
```
#### **5. Run Tests**
From the root directory:
```bash
pytest
```
You’ll see output like:
```
============================= test session starts =============================
collected 2 items

tests/test_calculator.py ..                                           [100%]

============================== 2 passed in 0.01s ==============================
```
