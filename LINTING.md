# Linting Guide

This file describes common lint checks for this Python project, including code style, best practices, naming conventions, security checks, and other lint-related validations.

## 1. Setup

Use the project virtual environment if available:

```bash
source ./venv/bin/activate
```

Install the recommended lint tools:

```bash
python -m pip install ruff pylint bandit
```

If you also want type checking and docstring/style checks:

```bash
python -m pip install mypy pydocstyle
```

## 2. Common lint checks

### Code quality and style

Use `ruff` to catch style issues, code smells, and common best-practice violations.

```bash
ruff check src test
```

`ruff` covers:
    - formatting issues
    - unused imports and variables
    - syntax and AST issues
    - naming conventions
    - complexity issues
    - common bug patterns

### Naming conventions and quality

`pylint` provides more detailed code quality and naming rule checks.

```bash
pylint src test
```

If you want to run targeted checks only, use:

```bash
pylint --disable=R,C src test
```

### Security checks

`bandit` scans Python code for common security issues.

```bash
bandit -r src
```

This checks for issues such as:
- insecure use of subprocess or shell commands
- risky file permissions
- insecure cryptography patterns
- unsanitized input handling

## 3. Other lint-style validations

### Type checking

If the repository grows and adds type hints, use `mypy` to validate annotations.

```bash
cd src && mypy .
```

Note: Run mypy from the `src` directory to avoid duplicate module name issues.

### Code complexity

Use `radon` to compute the cyclomatic complexity of each function and identify complex code paths.

```bash
python -m radon cc -s src
```

A function with a complexity score of `A` is simple, while `B`, `C`, `D`, `E`, and `F` indicate increasing complexity.

### Maintainability index

Use `radon` to compute the maintainability index across the source directory.

```bash
python -m radon mi src
```

A score of `A` is best; lower scores may indicate areas worth refactoring.

### Documentation style

Optionally check docstring formatting with `pydocstyle`.

```bash
pydocstyle src test
```

### Syntax checking

A simple Python syntax check can be done with the compile module:

```bash
python -m compileall src test
```

## 4. Recommended command sequence

Run these commands in order for a broad lint sweep:

```bash
source ./venv/bin/activate
python -m pip install ruff pylint bandit mypy pydocstyle
ruff check src test
pylint src test
bandit -r src
cd src && mypy .
pydocstyle src test
python -m compileall src test
```

## 5. Notes

- `ruff` can also fix many style issues automatically with `ruff check --fix src test`.
- If the project later adds a `pyproject.toml`, the configuration for these tools can be centralized there.
- Adjust the target paths (`src`, `test`) if additional code directories are added.
