# Quick-start

```python
import io
file = io.StringIO("""
foo = 1
""")

import os
os.environ["GRAOU_BAZ"] = "OUAF"

u = Ulticonf(configuration_file=file, environment_prefix="GRAOU_")
u.add_argument("--foo", type=int)
u.add_argument("--bar", type=int)
u.add_argument("--baz", type=str)
out = u.parse_args(["--bar", "2"])

assert out.foo == 1
assert out.bar == 2
assert out.baz == "OUAF"
```

# API reference

For `add_argument`, see `argparse`s documentation of the same method.


# What

Simplify parameterization of scripts

# How

By providing a single interface for handling various sources of parameterization

# How but in details

## Configuration sources

Using the same interface as `argparse`, `ulticonf` also checks value defined in:
`ulticonf` checks value defined in:

1. command line
2. environment variable
3. configuration file
4. default value (**NOT IMPLEMENTED YET**)

## Configuration file

For now, only a flat TOML file is supported. Oops :)


# TODOs

1. support various filetypes
2. implement extra `argparse` functions (e.g. `subgroup`)
3. support non-flat config
4. tests...
5. doc.......
