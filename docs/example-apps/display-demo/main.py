"""
Display Demo - showcasing display() capabilities in PyScript.

Demonstrates:
- Displaying basic Python types
- HTML content with the HTML() wrapper
- Custom objects with _repr_html_()
- Multiple values at once
- Building UIs incrementally
- Replacing vs. appending content
"""
from pyscript import display, HTML, when
import asyncio


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
        # Very simple darkening - just for demo purposes.
        if colour == "#667eea":
            return "#764ba2"
        elif colour == "#f093fb":
            return "#f5576c"
        elif colour == "#4facfe":
            return "#00f2fe"
        return "#333333"


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


@when("click", "#btn-basic")
def show_basic_types(event):
    """
    Display basic Python types.
    """
    display("=== Basic Types ===", target="basic-output", append=True)
    display("String: Hello, World!", target="basic-output", append=True)
    display(f"Number: {42}", target="basic-output", append=True)
    display(f"Float: {3.14159}", target="basic-output", append=True)
    display(f"Boolean: {True}", target="basic-output", append=True)
    display(f"List: {[1, 2, 3, 4, 5]}", target="basic-output", append=True)
    display(f"Dict: {{'name': 'Alice', 'age': 30}}", target="basic-output", append=True)


@when("click", "#btn-html")
def show_html_content(event):
    """
    Display HTML content.
    """
    # Clear and show HTML.
    display(HTML("<h3 style='color: #3498db;'>Rich HTML Content</h3>"), 
            target="html-output", append=False)
    
    display(HTML("""
        <p>This is <strong>bold</strong> and this is <em>italic</em>.</p>
    """), target="html-output")
    
    display(HTML("""
        <div style='background: #e8f4f8; padding: 1rem; border-radius: 4px;'>
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
    Display custom objects with _repr_html_.
    """
    display("=== Custom Object ===", 
            target="custom-output", append=False)
    
    # Display a table.
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
    Display multiple values at once.
    """
    display("First value", "Second value", "Third value",
            target="multi-output", append=True)


@when("click", "#btn-cards")
def show_metric_cards(event):
    """
    Display metric cards.
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


# Initial message.
display(HTML("<p style='color: #666;'>Click buttons to see different "
             "display examples.</p>"), 
        target="basic-output")