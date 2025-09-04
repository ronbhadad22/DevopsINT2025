# Nexus Example Package

A sample Python package demonstrating how to build and publish to a Nexus repository.

## Installation

```bash
pip install nexus-example-package
```

## Usage

```python
from nexus_example_package import hello

# Print a greeting
hello.greet("World")

# Get package version
print(hello.get_version())
```

## Development

### Building the package

```bash
python -m build
```

### Publishing to Nexus

```bash
python upload_to_nexus.py
```

## License

MIT License
