# Pirate Translator 🦜 💬 🇬🇧 ➡️ 🏴‍☠️

A simple PyScript application that translates English text into Pirate speak.

## What it demonstrates

- Basic PyScript application structure (HTML, Python, configuration).
- Using `pyscript.web` to interact with page elements.
- Event handling with the `@when` decorator.
- Installing and using third-party Python packages ([arrr](https://arrr.readthedocs.io/en/latest/)).

## Files

- `index.html` - The web page to display.
- `main.py` - Python code that handles the translation.
- `pyscript.json` - Configuration specifying required packages.

## How it works

1. User types English text into an input field.
2. User clicks the "Translate" button.
3. The `@when` decorator connects the button's click event to `translate_english`.
4. Function retrieves the input text using `web.page["english"]`.
5. Text is translated using the `arrr` library.
6. Result is displayed in the output div using `web.page["output"]`.

## Running locally

Simply serve these files from a web server. For example:

```bash
python3 -m http.server
```

Then open http://localhost:8000 in your browser.