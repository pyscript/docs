# PyScript documentation

Welcome to the PyScript documentation repository.

This source code becomes the official PyScript documentation hosted here:

[https://docs.pyscript.net](https://docs.pyscript.net/)

Contribute prose and participate in discussions about the written support of
PyScript and related topics.

## Getting started

Before you start contributing to the documentation, it's worthwhile to
take a look at the general contributing guidelines for the PyScript project.
You can find these guidelines here
[Contributing Guidelines](https://github.com/pyscript/pyscript/blob/main/CONTRIBUTING.md)

## Setup

The `docs` directory in the pyscript repository contains a
[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
documentation project. Material is a system that takes plaintext files
containing documentation written in Markdown, along with static files like
templates and themes, to build the static end result.

To setup the documentation development environment simply create a new
virtual environment, then `pip install -r requirements.txt` (from in the root
of this repository).

```sh
# example of a simple virtual environment
# creation from the root of this project
python -m venv .
./bin/pip install --upgrade setuptools
./bin/pip install -r requirements.txt
```

## Build

Simply run `mkdocs serve` or `./bin/mkdocs serve`.

## Cross-referencing

Link to other pages in the documentation by using the `{doc}` role. For
example, to link to the `docs/README.md` file, you would use:

```markdown
{doc}`docs/README.md`
```

Cross-reference the Python glossary by using the `{term}` role. For example, to
link to the `iterable` term, you would use:

```markdown
{term}`iterable`
```

Cross-reference functions, methods or data attributes by using the `{attr}` for
example:

```markdown
{py:func}`repr`
```

This would link to the `repr` function in the python builtins.
