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
