# PyScript documentation

Welcome to the PyScript documentation directory, where you can find
and contribute to discussions around PyScript and related topics.

## Getting started

Before you start contributing to the documentation, it's worthwhile to
take a look at the general contributing guidelines for the PyScript project. You can find these guidelines here
[Contributing Guidelines](https://github.com/pyscript/pyscript/blob/main/CONTRIBUTING.md)

## Setup

The `docs` directory in the pyscript repository contains a
[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) documentation project. Material is a system
that takes plaintext files containing documentation written in Markdown, along with
static files like templates and themes, to build the static end result.

To setup the documentation development environment simply run `make setup` from this folder and, once it's done,
activate your environment by running `conda activate ./_env`

## Build

Simply run `mkdocs serve`

## Cross-referencing

You can link to other pages in the documentation by using the `{doc}` role. For example, to link to the `docs/README.md` file, you would use:

```markdown
{doc}`docs/README.md`
```

You can also cross-reference the python glossary by using the `{term}` role. For example, to link to the `iterable` term, you would use:

```markdown
{term}`iterable`
```

You can also cross-reference functions, methods or data attributes by using the `{attr}` for example:

```markdown
{py:func}`repr`
```

This would link to the `repr` function in the python builtins.
