## Types of Function Arguments

| Argument Type                  | Definition Syntax         | Description                                                    |
|--------------------------------|---------------------------|----------------------------------------------------------------|
| Positional                     | `def f(a, b):`            | Values assigned by their position in the call                  |
| Keyword                        | `def f(a, b):`            | Values assigned by name using `a=…`, `b=…`                     |
| Default                        | `def f(a, b=10):`         | Provides a default for `b` if it’s not passed                  |
| Variable-length Positional     | `def f(*args):`           | Gathers extra positional arguments into a tuple `args`         |
| Variable-length Keyword        | `def f(**kwargs):`        | Gathers extra keyword arguments into a dict `kwargs`           |
| Keyword-only                   | `def f(a, *, b):`         | Parameters after `*` must be passed by keyword (`b=…`)         |
| Positional-only (Python 3.8+)  | `def f(a, b, /, c):`      | Parameters before `/` must be passed positionally (`a, b`)     |

## Lambda vs. Regular Functions

| Feature                  | `lambda` Function                              | `def` Function                                  |
|--------------------------|------------------------------------------------|-------------------------------------------------|
| **Syntax**               | `lambda args: expression`                      | `def func_name(args): statements`               |
| **Function Name**        | Anonymous (unless assigned to a variable)      | Requires a name                                 |
| **Return Behavior**      | Implicitly returns the expression result       | Uses `return` explicitly                        |
| **Number of Expressions**| Only one expression allowed                    | Can contain multiple statements and expressions |
| **Readability**          | Less readable for complex logic                | More readable and maintainable                  |
| **Use Case**             | Short, throwaway functions                     | Reusable, complex logic                         |
| **Supports Loops/Conditions** | ❌ Not allowed                            | ✅ Fully supported                               |
| **Docstrings**           | ❌ Not supported                                | ✅ Can include docstrings                        |
| **Pickling Support**     | ❌ Cannot be pickled (no unique name)       | ✅ Can be pickled                                |

### When to Use What?

- Use **lambda** when:
  - You need a quick, one-liner function (e.g., in `map()`, `filter()`, or `sorted()`).
  - You don’t need to reuse the function elsewhere.

- Use **def** when:
  - The function has multiple steps or conditions.
  - You want to document the function or reuse it.
  - You need better debugging and introspection support.

Want to see how lambdas are used in functional programming patterns like `map`, `filter`, or `reduce`?
