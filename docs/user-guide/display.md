# Display

The `display()` function is how to show Python objects, text, HTML,
images, and rich content in your web page. It introspects objects to
determine the best way to render them, supporting everything from
simple strings to matplotlib plots.

Heavily inspired by [IPython's rich display system](https://ipython.readthedocs.io/en/stable/api/generated/IPython.display.html).

Think of `display()` as Python's `print()` for the web - but with
superpowers.

## Basic usage

The simplest use is displaying text:

```python
from pyscript import display


display("Hello, World!")
display("Multiple", "values", "at", "once")
```

By default, `display()` outputs to the current script's location in the
page. Each call appends content unless you specify otherwise.

### Display targets

Control where content appears using the `target` parameter:

```python
from pyscript import display


# Display in a specific element by ID.
display("Hello", target="output-div")

# The '#' prefix is optional (and ignored if present).
display("Hello", target="#output-div")
```

### Replacing vs. appending

By default, `display()` appends content. Use `append=False` to replace
existing content:

```python
from pyscript import display


# Replace any existing content.
display("New content", target="output-div", append=False)

# Append to existing content (default behaviour).
display("More content", target="output-div", append=True)
```

## Displaying different types

### Strings

Plain strings are automatically HTML-escaped for safety:

```python
from pyscript import display


# This is safe - HTML tags are escaped.
display("<script>alert('XSS')</script>")
# Displays: &lt;script&gt;alert('XSS')&lt;/script&gt;
```

### HTML content

To display unescaped HTML, wrap it in the `HTML` class:

```python
from pyscript import HTML, display


# Render actual HTML.
display(HTML("<h1>Hello, World!</h1>"))
display(HTML("<p>This is <strong>bold</strong> text.</p>"))
```

!!! warning

    Only use `HTML()` with content you trust. Never use it with
    user-provided data as it can create security vulnerabilities.

### Python objects

Most Python objects display using their `__repr__()` method:

```python
from pyscript import display


# Numbers.
display(42)
display(3.14159)

# Lists and dictionaries.
display([1, 2, 3, 4, 5])
display({"name": "Alice", "age": 30})

# Custom objects.
class Person:
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return f"Person(name='{self.name}')"

display(Person("Bob"))
```

### Images

Display images from various sources:

```python
from pyscript import display


# From a URL (using HTML).
from pyscript import HTML

display(HTML('<img src="https://example.com/image.png">'))

# From matplotlib (if you have it configured).
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4], [1, 4, 2, 3])
display(fig)
```

PyScript automatically detects matplotlib figures and renders them as
PNG images.

## Rich display system

As has already been mentioned, PyScript's display system is inspired by
[IPython's rich display system](https://ipython.readthedocs.io/en/stable/api/generated/IPython.display.html).
Objects can implement special methods to control how they're rendered.

### Representation methods

Objects are checked for these methods in order of preference:

1. `_repr_mimebundle_()` - Returns multiple format options.
2. `_repr_png_()` - Returns PNG image data.
3. `_repr_jpeg_()` - Returns JPEG image data.
4. `_repr_svg_()` - Returns SVG graphics.
5. `_repr_html_()` - Returns HTML content.
6. `_repr_json_()` - Returns JSON data.
7. `__repr__()` - Returns plain text representation.

### Custom display for your objects

Create objects that display beautifully:

```python
from pyscript import display


class ColourSwatch:
    """
    A colour swatch that displays as a coloured box.
    """
    def __init__(self, colour, name):
        self.colour = colour
        self.name = name
    
    def _repr_html_(self):
        return f"""
        <div style="display: inline-block; margin: 5px;">
            <div style="width: 100px; height: 100px; 
                        background-color: {self.colour};
                        border: 2px solid #333;
                        border-radius: 8px;">
            </div>
            <div style="text-align: center; margin-top: 5px;">
                {self.name}
            </div>
        </div>
        """


# These display as visual colour swatches.
display(ColourSwatch("#FF0000", "Red"))
display(ColourSwatch("#00FF00", "Green"))
display(ColourSwatch("#0000FF", "Blue"))
```

### Multiple format support

Provide multiple representations for maximum compatibility:

```python
from pyscript import display


class DataTable:
    """
    A table that can display as HTML or plain text.
    """
    def __init__(self, data):
        self.data = data
    
    def _repr_mimebundle_(self):
        """
        Return multiple formats.
        """
        html = "<table border='1'>"
        for row in self.data:
            html += "<tr>"
            for cell in row:
                html += f"<td>{cell}</td>"
            html += "</tr>"
        html += "</table>"
        
        text = "\n".join(["\t".join(str(c) for c in row) 
                         for row in self.data])
        
        return {
            "text/html": html,
            "text/plain": text
        }


table = DataTable([
    ["Name", "Age", "City"],
    ["Alice", 30, "London"],
    ["Bob", 25, "Paris"]
])

display(table)
```

## Working with scripts

### Script tag output

When PyScript runs a `<script type="mpy">` tag, `display()` outputs to
that script's location by default:

```html
<div>
  <h2>Output appears here:</h2>
  <script type="mpy">
    from pyscript import display
    display("Hello from the script!")
  </script>
</div>
```

### Targeting specific elements

Use the `target` attribute on your script tag to send output elsewhere:

```html
<div id="results"></div>

<script type="mpy" target="results">
  from pyscript import display
  # This goes to #results, not the script's location.
  display("Output in the results div!")
</script>
```

## Example: Data visualisation dashboard

Here's a complete example showing various display capabilities:

<iframe src="../../example-apps/display-demo/" style="border: 1px solid black; width:100%; min-height: 600px; border-radius: 0.2rem; box-shadow: var(--md-shadow-z1);"></iframe>

[View the complete source code](https://github.com/pyscript/docs/tree/main/docs/example-apps/display-demo).

This example demonstrates:

- Displaying different data types.
- Creating custom display representations.
- Building UIs with `HTML()` (but prefer to use `pyscript.web` for this).
- Updating content dynamically.
- Using display targets effectively.

## Best practices

### Security

**Never use `HTML()` with untrusted content:**

```python
# DANGEROUS - don't do this!
user_input = "<script>alert('XSS')</script>"
display(HTML(user_input))

# SAFE - plain strings are escaped automatically.
display(user_input)
```

### Performance

For frequent or rapid updates:

- Use `append=False` to replace content rather than accumulating it.
- For interactive UIs, use `pyscript.web` to manipulate elements directly
  rather than repeatedly calling `display()`.
- When you need fine control over the DOM, `display()` **is for output,
  not UI building**.

### Organisation

Keep display logic close to your data:

```python
class Report:
    def __init__(self, data):
        self.data = data
    
    def _repr_html_(self):
        """
        Encapsulate display logic in the class.
        """
        return f"<div class='report'>{self.data}</div>"


# Clean usage.
report = Report({"sales": 1000})
display(report)
```

## What's next

Now that you understand how to display content, explore these related
topics:

**[Configuration](configuration.md)** - Configure how your scripts load
and when event handlers are attached.

**[DOM Interaction](dom.md)** - Learn how to create and manipulate
elements for more control than `display()` provides.

**[Events](events.md)** - Make your displayed content interactive by
handling user events.

**[Workers](workers.md)** - Display content from background threads
(requires explicit `target` parameter).