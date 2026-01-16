# Interactive Colour Picker

[Run the app](index.html) | 
[View the code on GitHub](https://github.com/pyscript/docs/tree/main/docs/example-apps/colour-picker) 

A colour picker application demonstrating various event handling
patterns in PyScript.

## What it demonstrates

* Multiple event types with `input` events (RGB sliders update in real-time), 
`change` events (number inputs and hex input) and `click` events (preset
buttons and history colours).
* Stacked decorators with a single function handling multiple sliders with
  `@when` stacked three times.
* Custom events via the `colour_changed` Event for decoupling colour updates
  from app history and to show how to separate concerns in your application.
* Working with form inputs of different types:
    - Range sliders, number inputs, text inputs.
    - Synchronising values across different input types.
    - Validating and clamping values.
* Dynamic UI updates:
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

## How it works

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
