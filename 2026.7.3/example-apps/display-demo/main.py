"""
Display Demo - showcasing display() capabilities in PyScript.

The functions in this code demonstrate:

- Displaying basic Python types
- HTML content with the HTML() wrapper
- Custom objects with _repr_html_()
- Multiple values at once
- Building UIs incrementally
- Replacing vs. appending content
- Pandas DataFrames
- Matplotlib plots
"""
from pyscript import display, HTML, when
import asyncio
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


# Classes with custom representations.


class MetricCard:
    """
    A metric card that displays with custom HTML.
    """

    def __init__(self, label, value, colour="#667eea"):
        self.label = label
        self.value = value
        self.colour = colour
    
    def _repr_html_(self):
        """
        Custom HTML representation.
        """
        return f"""
        <div class="data-card" style="background: linear-gradient(135deg, 
             {self.colour} 0%, {self._darken_colour(self.colour)} 100%);">
            <div class="label">{self.label}</div>
            <div class="metric">{self.value}</div>
        </div>
        """
    
    def _darken_colour(self, colour):
        """
        Simple colour darkening for gradient.
        """
        darkening_map = {
            "#667eea": "#764ba2",
            "#f093fb": "#f5576c",
            "#4facfe": "#00f2fe",
        }
        return darkening_map.get(colour, "#333333")


class DataTable:
    """
    A table with multiple representation formats.
    """

    def __init__(self, headers, rows):
        self.headers = headers
        self.rows = rows
    
    def _repr_html_(self):
        """
        HTML table representation.
        """
        html = "<table style='width: 100%; border-collapse: collapse;'>"
        # Headers.
        html += "<tr style='background: #3498db; color: white;'>"
        for header in self.headers:
            html += f"<th style='padding: 8px; text-align: left;'>"
            html += f"{header}</th>"
        html += "</tr>"
        # Rows.
        for i, row in enumerate(self.rows):
            bg = "#f8f9fa" if i % 2 == 0 else "white"
            html += f"<tr style='background: {bg};'>"
            for cell in row:
                html += f"<td style='padding: 8px;'>{cell}</td>"
            html += "</tr>"
        html += "</table>"
        return html
    
    def __repr__(self):
        """
        Plain text representation.
        """
        lines = ["\t".join(self.headers)]
        lines.extend(["\t".join(str(c) for c in row) for row in self.rows])
        return "\n".join(lines)


# Event handlers for buttons to demonstrate display() in different ways.


@when("click", "#btn-basic")
def show_basic_types(event):
    """
    Display basic Python types.
    """
    display("=== Basic Types ===", target="basic-output", append=False)
    display("String: Hello, World!", target="basic-output")
    display(f"Number: {42}", target="basic-output")
    display(f"Float: {3.14159}", target="basic-output")
    display(f"Boolean: {True}", target="basic-output")
    display(f"List: {[1, 2, 3, 4, 5]}", target="basic-output")
    display(f"Dict: {{'name': 'Alice', 'age': 30}}", 
            target="basic-output")


@when("click", "#btn-html")
def show_html_content(event):
    """
    Display raw unescaped HTML content of various sorts.
    """
    display(
        HTML("<h3 style='color: #3498db;'>Rich HTML Content</h3>"), 
        target="html-output",
        append=False
    )
    display(HTML("""
        <p>This is <strong>bold</strong> and this is <em>italic</em>.</p>
    """), target="html-output")
    display(HTML("""
        <div style='background: #e8f4f8; padding: 1rem; 
             border-radius: 4px;'>
            <p style='margin: 0;'>📊 Styled content box</p>
        </div>
    """), target="html-output")
    display(HTML("""
        <ul>
            <li>Item one</li>
            <li>Item two</li>
            <li>Item three</li>
        </ul>
    """), target="html-output")


@when("click", "#btn-custom")
def show_custom_object(event):
    """
    Display a custom DataTable object with _repr_html_.
    """
    display("=== Custom Object ===", 
            target="custom-output", append=False)
    table = DataTable(
        ["Name", "Score", "Grade"],
        [
            ["Alice", 95, "A"],
            ["Bob", 87, "B"],
            ["Carol", 92, "A"],
            ["Dave", 78, "C"]
        ]
    )
    display(table, target="custom-output")


@when("click", "#btn-multi")
def show_multiple_values(event):
    """
    Display multiple values via a single call.
    """
    display(
        "First value",
        "Second value",
        "Third value",
        target="multi-output",
    )


@when("click", "#btn-cards")
def show_metric_cards(event):
    """
    Display metric cards (with bespoke _repr_html_). See the
    MetricCard class above.
    """
    display(MetricCard("Total Users", "1,234", "#667eea"),
            target="cards-output", append=False)
    display(MetricCard("Revenue", "$56,789", "#f093fb"),
            target="cards-output")
    display(MetricCard("Growth", "+23%", "#4facfe"),
            target="cards-output")


@when("click", "#btn-incremental")
async def show_incremental_updates(event):
    """
    Build UI incrementally with delays.
    """
    display(HTML("<h3>Loading data...</h3>"), 
            target="incremental-output", append=False)
    await asyncio.sleep(0.5)
    display(HTML("<p>✓ Connected to server</p>"), 
            target="incremental-output")
    await asyncio.sleep(0.5)
    display(HTML("<p>✓ Fetching records</p>"), 
            target="incremental-output")
    await asyncio.sleep(0.5)
    display(HTML("<p>✓ Processing data</p>"), 
            target="incremental-output")
    await asyncio.sleep(0.5)
    display(HTML("<h4 style='color: #27ae60;'>Complete! ✓</h4>"), 
            target="incremental-output")


@when("click", "#btn-dataframe")
def show_dataframe(event):
    """
    Display a Pandas DataFrame.
    """
    # Numpty sample data.
    data = {
        'Product': ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headset'],
        'Price': [999.99, 24.99, 79.99, 299.99, 149.99],
        'Stock': [15, 87, 43, 28, 56],
        'Rating': [4.5, 4.2, 4.7, 4.4, 4.6]
    }
    # Real pandas!
    df = pd.DataFrame(data)
    # Calculate summary statistics.
    total_value = (df['Price'] * df['Stock']).sum()
    avg_rating = df['Rating'].mean()
    display(HTML("<h3>Product Inventory</h3>"),
            target="dataframe-output", append=False)
    # Natively render the DataFrame.
    display(df, target="dataframe-output")
    display(HTML(f"""
        <div style='margin-top: 1rem; padding: 0.5rem; 
             background: #e8f4f8; border-radius: 4px;'>
            <strong>Summary:</strong> Total inventory value: 
            ${total_value:,.2f} | Average rating: {avg_rating:.1f}/5.0
        </div>
    """), target="dataframe-output")


@when("click", "#btn-plot")
def show_matplotlib_plot(event):
    """
    Display a single matplotlib plot.
    """
    # Generate sample data.
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    # Create plot.
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(x, y, 'b-', linewidth=2, label='sin(x)')
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_title('Sine Wave')
    ax.grid(True, alpha=0.3)
    ax.legend()
    display(HTML("<h3>Sine Wave Plot</h3>"),
            target="plot-output", append=False)
    # Natively render the Matplotlib figure.
    display(fig, target="plot-output")
    plt.close(fig)


@when("click", "#btn-multiplot")
def show_multiple_plots(event):
    """
    Display multiple subplots. A more complex Matplotlib example.
    """
    # Generate data.
    x = np.linspace(0, 10, 100)
    # Create subplots.
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    # Plot 1: Sine.
    axes[0, 0].plot(x, np.sin(x), 'b-')
    axes[0, 0].set_title('Sine')
    axes[0, 0].grid(True, alpha=0.3)
    # Plot 2: Cosine.
    axes[0, 1].plot(x, np.cos(x), 'r-')
    axes[0, 1].set_title('Cosine')
    axes[0, 1].grid(True, alpha=0.3)
    # Plot 3: Exponential.
    axes[1, 0].plot(x, np.exp(-x/5), 'g-')
    axes[1, 0].set_title('Exponential Decay')
    axes[1, 0].grid(True, alpha=0.3)
    # Plot 4: Scatter.
    axes[1, 1].scatter(x, np.random.randn(100), alpha=0.5)
    axes[1, 1].set_title('Random Scatter')
    axes[1, 1].grid(True, alpha=0.3)
    plt.tight_layout()
    display(HTML("<h3>Multiple Plots</h3>"),
            target="multiplot-output", append=False)
    # Natively render the Matplotlib figure with subplots.
    display(fig, target="multiplot-output")
    plt.close(fig)


# Replace loading message with ready message once Pyodide with pandas
# and matplotlib is fully loaded.
display(
    HTML("<p style='color: #666;'>Click buttons to see different "
         "display examples.</p>"), 
    target="basic-output",
    append=False
)