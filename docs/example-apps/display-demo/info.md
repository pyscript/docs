# Display Demo

A comprehensive demonstration of PyScript's `display()` function and its
various capabilities.

## What it demonstrates

**Basic types:**
- Strings, numbers, booleans, lists, dictionaries.
- Automatic HTML escaping for safety.

**HTML content:**
- Using `HTML()` to render unescaped HTML.
- Creating styled content boxes.
- Building rich interfaces.

**Custom objects:**
- Implementing `_repr_html_()` for custom rendering.
- Creating reusable display components.
- Table generation with custom styling.

**Multiple values:**
- Displaying several values in one call.
- Appending vs. replacing content.

**Incremental updates:**
- Building UIs progressively.
- Showing status updates with delays.
- Creating loading sequences.

## Features

Six interactive panels demonstrating:

1. **Basic Types** - Standard Python objects.
2. **HTML Content** - Rich formatted content.
3. **Custom Objects** - Classes with custom display logic.
4. **Multiple Values** - Batch display operations.
5. **Data Cards** - Styled metric cards using custom classes.
6. **Incremental Updates** - Progressive UI building with async.

## Files

- `index.html` - Page structure and styling.
- `main.py` - Display demonstrations with custom classes.

## Key patterns demonstrated

### Custom display representations

```python
class MetricCard:
    def __init__(self, label, value, colour):
        self.label = label
        self.value = value
        self.colour = colour
    
    def _repr_html_(self):
        return f"<div class='card'>{self.label}: {self.value}</div>"

# Displays with custom HTML.
display(MetricCard("Users", "1,234", "#667eea"))
```

### Multiple format support

```python
class DataTable:
    def _repr_html_(self):
        return "<table>...</table>"
    
    def __repr__(self):
        return "Plain text table"

# Automatically uses HTML when available.
display(table)
```

### Incremental building

```python
async def build_ui():
    display("Step 1", target="output", append=False)
    await asyncio.sleep(1)
    display("Step 2", target="output")
    await asyncio.sleep(1)
    display("Complete!", target="output")
```

## Running locally

Serve these files from a web server:

```bash
python3 -m http.server
```

Then open http://localhost:8000 in your browser.