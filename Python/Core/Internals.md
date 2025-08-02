# String Interning
String interning is an optimization technique used by interpreters and compilers to save memory and improve the performance of string comparisons. In essence, it means that for identical immutable string values, only one copy of that string is stored in memory. When a new string literal with the same value is encountered, instead of creating a new object, the system reuses the reference to the existing interned string

Python (specifically CPython, the most common implementation) employs automatic string interning for certain types of strings and also provides a way for manual interning
Python automatically interns strings that meet specific criteria, primarily for performance and memory optimization of frequently used strings:
- __String Literals (Identifier-like and Short Strings):__
  
  - Identifiers: Strings that look like Python identifiers (alphanumeric characters and underscores, no spaces, no special characters, not starting with a digit) are often interned. This includes variable names, function names, class names, keywords, etc.
  - Short Strings: Python typically interns short string literals. The exact length threshold can vary between Python versions and implementations, but generally, small strings (e.g., up to 20 characters) without spaces or special characters are good candidates
```python
a = "hello"
b = "hello"
print(a is b) # Output: True (likely interned)

x = "my_variable_name"
y = "my_variable_name"
print(x is y) # Output: True (likely interned)
```
- __Compile-Time Constants:__
  -  Strings that are constant literals appearing in your code (e.g., within function definitions or module scope) are often interned during the compilation phase.
```python
def greet():
    return "welcome"

s1 = greet()
s2 = "welcome"
print(s1 is s2) # Output: True (often interned because "welcome" is a literal)
```
- __Strings resulting from literal concatenation:__
  -  If you concatenate string literals directly in your code, Python's peephole optimizer at compile time might pre-compute the result and intern it, especially if the resulting string is short and "internable."
```python
s = "hello" + "world"
t = "helloworld"
print(s is t) # Output: True (concatenation of literals at compile time)
```
### When Automatic Interning Might NOT Occur:
  - __Dynamically Generated Strings:__
    Strings created at runtime through operations like concatenation of variables, f-strings, or string formatting are generally not automatically interned unless they happen to match an already interned string and Python decides to reuse it (which is not guaranteed).
  - __Strings with Spaces or Special Characters:__
    Strings containing spaces or non-alphanumeric characters are less likely to be automatically interned unless they are very short.
### Manual Interning with sys.intern():
  For situations where automatic interning doesn't occur, but you want to force it (e.g., if you have many identical long strings read from a file), you can use sys.intern()
  ```python
import sys

long_string_1 = "this is a very very very very long string that might not be automatically interned"
long_string_2 = "this is a very very very very long string that might not be automatically interned"

print(long_string_1 is long_string_2) # Output: False (not automatically interned)

interned_long_string_1 = sys.intern(long_string_1)
interned_long_string_2 = sys.intern(long_string_2)

print(interned_long_string_1 is interned_long_string_2) # Output: True (forced interning)
```
