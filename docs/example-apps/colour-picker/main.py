"""
Interactive Colour Picker - demonstrating event handling in PyScript.

Shows:
- Multiple event types (input, click, change)
- Custom events for decoupled logic
- Working with form inputs
- Dynamic UI updates
"""
from pyscript import when, Event
from pyscript.web import page


# Custom event for when colour changes.
colour_changed = Event()

# Colour history (limited to 10).
history = []


def rgb_to_hex(r, g, b):
    """
    Convert RGB values to hex colour string.
    """
    return f"#{r:02X}{g:02X}{b:02X}"


def hex_to_rgb(hex_colour):
    """
    Convert hex colour string to RGB tuple.
    """
    hex_colour = hex_colour.lstrip("#")
    return tuple(int(hex_colour[i:i+2], 16) for i in (0, 2, 4))


def get_current_rgb():
    """
    Get current RGB values from sliders.
    """
    r = int(page["#red-slider"].value)
    g = int(page["#green-slider"].value)
    b = int(page["#blue-slider"].value)
    return r, g, b


def update_display(hex_colour):
    """
    Update the colour display with the given hex colour.
    """
    display = page["#colour-display"]
    display.style.backgroundColor = hex_colour
    display.content = hex_colour


def update_controls(r, g, b):
    """
    Update all controls to match RGB values.
    """
    # Update sliders.
    page["#red-slider"].value = r
    page["#green-slider"].value = g
    page["#blue-slider"].value = b
    
    # Update number inputs.
    page["#red-value"].value = r
    page["#green-value"].value = g
    page["#blue-value"].value = b
    
    # Update hex input.
    hex_colour = rgb_to_hex(r, g, b)
    page["#hex-input"].value = hex_colour
    
    # Update display.
    update_display(hex_colour)
    
    # Trigger custom event.
    colour_changed.trigger(hex_colour)


def add_to_history(hex_colour):
    """
    Add colour to history, maintaining max of 10 items.
    """
    if hex_colour in history:
        return
    
    history.insert(0, hex_colour)
    if len(history) > 10:
        history.pop()
    
    # Update history display.
    render_history()


def render_history():
    """
    Render colour history.
    """
    from pyscript.web import div
    
    container = page["#history-colours"]
    container.clear()
    
    for colour in history:
        colour_div = div(Class="history-colour", title=colour)
        colour_div.style.backgroundColor = colour
        colour_div.dataset.colour = colour
        container.append(colour_div)


@when("input", "#red-slider")
@when("input", "#green-slider")
@when("input", "#blue-slider")
def handle_slider_change(event):
    """
    Handle RGB slider changes.
    """
    r, g, b = get_current_rgb()
    update_controls(r, g, b)


@when("change", "#red-value")
@when("change", "#green-value")
@when("change", "#blue-value")
def handle_number_change(event):
    """
    Handle number input changes.
    """
    r = int(page["#red-value"].value)
    g = int(page["#green-value"].value)
    b = int(page["#blue-value"].value)
    
    # Clamp values.
    r = max(0, min(255, r))
    g = max(0, min(255, g))
    b = max(0, min(255, b))
    
    update_controls(r, g, b)


@when("change", "#hex-input")
def handle_hex_change(event):
    """
    Handle hex input changes.
    """
    hex_colour = event.target.value.strip()
    
    # Validate hex colour.
    if not hex_colour.startswith("#"):
        hex_colour = "#" + hex_colour
    
    try:
        r, g, b = hex_to_rgb(hex_colour)
        update_controls(r, g, b)
    except (ValueError, IndexError):
        # Invalid hex colour, ignore.
        pass


@when("click", ".preset-btn")
def handle_preset_click(event):
    """
    Handle preset colour button clicks.
    """
    hex_colour = event.target.dataset.colour
    r, g, b = hex_to_rgb(hex_colour)
    update_controls(r, g, b)


@when("click", ".history-colour")
def handle_history_click(event):
    """
    Handle clicks on history colours.
    """
    hex_colour = event.target.dataset.colour
    r, g, b = hex_to_rgb(hex_colour)
    update_controls(r, g, b)


@when(colour_changed)
def handle_colour_changed(hex_colour):
    """
    Handle custom colour changed event.
    
    This demonstrates decoupling - the history management doesn't need
    to know about sliders, presets, or hex inputs.
    """
    add_to_history(hex_colour)


# Initial setup.
r, g, b = get_current_rgb()
hex_colour = rgb_to_hex(r, g, b)
update_display(hex_colour)
add_to_history(hex_colour)