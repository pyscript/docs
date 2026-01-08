# Interactive Colour Picker

A colour picker application demonstrating various event handling
patterns in PyScript.

## What it demonstrates

**Multiple event types:**
- `input` events - RGB sliders update in real-time.
- `change` events - Number inputs and hex input.
- `click` events - Preset buttons and history colours.

**Stacked decorators:**
- Single function handling multiple sliders with `@when` stacked three
  times.

**Custom events:**
- `colour_changed` Event for decoupling colour updates from history
  management.
- Shows how to separate concerns in your application.

**Working with form inputs:**
- Range sliders, number inputs, text inputs.
- Synchronising values across different input types.
- Validating and clamping values.

**Dynamic UI updates:**
- Updating display colour.
- Maintaining colour history.
- Creating history elements dynamically.

## Features

- Adjust colours using RGB sliders.
- Enter RGB values directly with number inputs.
- Enter hex colour codes.
- Quick selection from preset colours.
- Colour history (last 10 colours).
- Click history to restore colours.
- Real-time colour display with hex code.

## Files

- `index.html` - Page structure and styling.
- `main.py` - Event handling logic demonstrating various patterns.

## Key patterns demonstrated

### Stacking decorators

```python
@when("input", "#red-slider")
@when("input", "#green-slider")
@when("input", "#blue-slider")
def handle_slider_change(event):
    # Single function handles all three sliders.
    pass
```

### Custom events for decoupling

```python
# Define custom event.
colour_changed = Event()

# Trigger it when colour updates.
colour_changed.trigger(hex_colour)

# Handle it separately.
@when(colour_changed)
def handle_colour_changed(hex_colour):
    add_to_history(hex_colour)
```

### Working with form inputs

```python
@when("input", "#red-slider")
def handle_slider_change(event):
    # Get value from slider.
    value = int(event.target.value)
    # Update display.
    update_display(value)
```

## Running locally

Serve these files from a web server:

```bash
python3 -m http.server
```

Then open http://localhost:8000 in your browser.