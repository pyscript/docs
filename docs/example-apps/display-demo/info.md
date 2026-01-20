# Display Demo

[Run the app](index.html) | 
[View the code on GitHub](https://github.com/pyscript/docs/tree/main/docs/example-apps/display-demo)

A comprehensive demonstration of PyScript's `display()` function and its
various capabilities including Pandas DataFrames and Matplotlib plots.

## What it demonstrates

Rather a lot! Most of the common `display()` patterns are covered:

* Basic types:
    - Strings, numbers, booleans, lists, dictionaries.
    - Automatic HTML escaping for safety.
* HTML content:
    - Using `HTML()` to render unescaped HTML.
    - Creating styled content boxes.
    - Building rich interfaces.
* Custom objects:
    - Implementing `_repr_html_()` for custom rendering.
    - Creating reusable display components.
    - Table generation with custom styling.
* Multiple values:
    - Displaying several values in one call.
    - Appending vs. replacing content.
* Incremental updates:
    - Building UIs progressively.
    - Showing status updates with delays.
    - Creating loading sequences.
* Pandas DataFrames:
    - Displaying tabular data with Pandas.
    - Automatic HTML table rendering.
    - Computing summary statistics.
* Matplotlib plots:
    - Creating line plots, scatter plots.
    - Multiple subplots in a single figure.
    - Customising axes, labels, and styling.

## Features

Nine interactive panels. Once PyScript has loaded they reveal how
`display()` can be used to handle:

1. Basic Types - Standard Python objects.
2. HTML Content - Rich formatted content.
3. Custom Objects - Classes with custom display logic.
4. Multiple Values - Batch display operations.
5. Data Cards - Styled metric cards using custom classes.
6. Incremental Updates - Progressive UI building with async.
7. Pandas DataFrame - Tabular data with Pandas.
8. Matplotlib Plot - Single plot with sine wave.
9. Multiple Plots - Four subplots showing different functions.

## Files

- `index.html` - Page structure, styling, and PyScript configuration.
- `main.py` - Display demonstrations with custom classes, DataFrames,
  and plots.

## How it works

### Custom display representations

```python
class MetricCard:
    """
    A metric card with custom HTML rendering.
    """
    def __init__(self, label, value, colour):
        self.label = label
        self.value = value
        self.colour = colour
    
    def _repr_html_(self):
        """
        Return custom HTML.
        """
        return f"<div class='card'>{self.label}: {self.value}</div>"


# Displays with custom HTML.
display(MetricCard("Users", "1,234", "#667eea"))
```

### Pandas DataFrames

```python
import pandas as pd

data = {
    'Product': ['Laptop', 'Mouse', 'Keyboard'],
    'Price': [999.99, 24.99, 79.99],
    'Stock': [15, 87, 43]
}

df = pd.DataFrame(data)

# Displays as formatted HTML table.
display(df, target="output")
```

### Matplotlib plots

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
y = np.sin(x)

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(x, y, 'b-', linewidth=2)
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_title('Sine Wave')
ax.grid(True)

# Displays plot as image.
display(fig, target="output")
plt.close(fig)
```

### Incremental building

```python
async def build_ui():
    """
    Build UI progressively.
    """
    display("Step 1", target="output", append=False)
    await asyncio.sleep(1)
    display("Step 2", target="output")
    await asyncio.sleep(1)
    display("Complete!", target="output")
```