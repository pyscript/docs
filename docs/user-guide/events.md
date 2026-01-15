# Events

Events are how your PyScript application responds to user actions:
clicks, key presses, form submissions, mouse movements, and more.
PyScript provides the `@when` decorator, a powerful and Pythonic way to
connect Python functions to browser events.

This guide explores the `@when` decorator and the custom `Event` class
for creating your own event system within Python code.

## The @when decorator

The `@when` decorator connects Python functions to browser events. When
the specified event occurs on matching elements, your function is
called automatically.

### Basic usage

The simplest form takes an event type and a CSS selector:

```python
from pyscript import when


@when("click", "#my-button")
def handle_click(event):
    """
    Called whenever the element with id 'my-button' is clicked.
    """
    print("Button was clicked!")
```

The decorator attaches the function to all elements matching the
selector. If multiple elements match, the function is called for each
one when its event fires.

### Event types

You can handle any browser event. Common ones include:

**Mouse events**: `click`, `dblclick`, `mousedown`, `mouseup`,
`mousemove`, `mouseenter`, `mouseleave`, `mouseover`, `mouseout`

**Keyboard events**: `keydown`, `keyup`, `keypress`

**Form events**: `submit`, `change`, `input`, `focus`, `blur`

**Document events**: `DOMContentLoaded`, `load`, `resize`, `scroll`

See the [MDN Event Reference](https://developer.mozilla.org/en-US/docs/Web/Events)
for a complete list.

### CSS selectors

The selector can be any valid CSS selector:

```python
from pyscript import when


# By ID.
@when("click", "#submit-button")
def handle_submit(event):
    print("Submit button clicked")


# By class.
@when("click", ".delete-btn")
def handle_delete(event):
    print("Delete button clicked")


# By attribute.
@when("click", "[data-action='save']")
def handle_save(event):
    print("Save button clicked")


# Complex selectors.
@when("click", "nav .menu-item:not(.disabled)")
def handle_menu(event):
    print("Menu item clicked")
```

### Working with Element objects

You can also pass `pyscript.web` Element objects directly instead of
CSS selectors:

```python
from pyscript import when, web


# Create an element.
button = web.button("Click me", id="my-button")
web.page.body.append(button)

# Attach event handler using the Element object.
@when("click", button)
def handle_click(event):
    print("Button clicked!")
```

This works with `ElementCollection` objects too:

```python
from pyscript import when, web


# Find multiple elements.
buttons = web.page.find(".action-button")

# Attach handler to all of them.
@when("click", buttons)
def handle_button_click(event):
    print(f"Button clicked: {event.target.textContent}")
```

## JavaScript event objects

When a browser event occurs, your function receives a JavaScript event object
containing information about what happened. Handling such events
[is optional](#functions-without-event-arguments).

### Common properties

```python
from pyscript import when


@when("click", ".item")
def handle_click(event):
    # The element that triggered the event.
    target = event.target
    
    # The element the listener is attached to.
    current_target = event.currentTarget
    
    # Event type.
    event_type = event.type  # "click"
    
    # Mouse position.
    x = event.clientX
    y = event.clientY
    
    # Keyboard keys.
    key = event.key
    ctrl_pressed = event.ctrlKey
    shift_pressed = event.shiftKey
```

### Preventing defaults

Some events have default browser behaviours you might want to prevent:

```python
from pyscript import when


@when("submit", "#my-form")
def handle_submit(event):
    # Prevent the form from actually submitting.
    event.preventDefault()
    
    # Handle the submission in Python instead.
    print("Form submitted via Python!")


@when("click", "a.external-link")
def handle_link(event):
    # Prevent navigation.
    event.preventDefault()
    
    # Handle the link click custom logic.
    print(f"Would navigate to: {event.target.href}")
```

### Stopping propagation

Events "bubble" up through the DOM tree. Stop this with
`stopPropagation()`:

```python
from pyscript import when


@when("click", ".outer")
def handle_outer(event):
    print("Outer clicked")


@when("click", ".inner")
def handle_inner(event):
    print("Inner clicked")
    # Stop the event from reaching .outer.
    event.stopPropagation()
```

## Custom Pythonic events

The `pyscript.Event` class lets you create custom events within your Python
code. This is useful for decoupling parts of your application or
creating your own event-driven architecture.

### Creating and using custom events

```python
from pyscript import Event, when


# Create a custom event.
data_loaded = Event()

# Add a listener using @when.
@when(data_loaded)
def handle_data_loaded(result):
    print(f"Data loaded: {result}")

# Later, trigger the event.
data_loaded.trigger({"items": [1, 2, 3], "count": 3})
```

### Multiple listeners

Custom events can have multiple listeners:

```python
from pyscript import Event, when


user_logged_in = Event()


@when(user_logged_in)
def update_ui(user_data):
    print(f"Welcome, {user_data['name']}!")


@when(user_logged_in)
def load_preferences(user_data):
    print(f"Loading preferences for {user_data['id']}")


@when(user_logged_in)
def track_analytics(user_data):
    print("Recording login event")


# Trigger once, all listeners are called.
user_logged_in.trigger({"id": 123, "name": "Alice"})
```

### Bridging DOM and custom events

You can trigger custom events from DOM event handlers:

```python
from pyscript import Event, when


# Custom event.
button_clicked = Event()

# Trigger custom event from DOM event.
@when("click", "#my-button")
def handle_dom_click(event):
    # Do some processing.
    button_text = event.target.textContent
    
    # Trigger custom event with processed data.
    button_clicked.trigger({"text": button_text, "timestamp": "now"})


# Handle the custom event elsewhere.
@when(button_clicked)
def handle_custom_event(data):
    print(f"Button '{data['text']}' was clicked at {data['timestamp']}")
```

This pattern decouples DOM handling from business logic.

## Advanced patterns

### Stacking decorators

You can stack `@when` decorators to handle multiple events with one
function:

```python
from pyscript import when


@when("mouseenter", ".highlight")
@when("focus", ".highlight")
def highlight_element(event):
    event.target.classList.add("highlighted")


@when("mouseleave", ".highlight")
@when("blur", ".highlight")
def unhighlight_element(event):
    event.target.classList.remove("highlighted")
```

### Async event handlers

Event handlers can be async functions:

```python
from pyscript import when
import asyncio


@when("click", "#fetch-data")
async def fetch_data(event):
    print("Fetching data...")
    
    # Simulate async operation.
    await asyncio.sleep(2)
    
    print("Data fetched!")
```

### Event options

Pass options to control how events are handled:

```python
from pyscript import when


# Fire only once.
@when("click", "#one-time-button", once=True)
def handle_once(event):
    print("This runs only once!")


# Use capture phase instead of bubble phase.
@when("click", "#container", capture=True)
def handle_capture(event):
    print("Captured during capture phase")


# Mark as passive (can't prevent default).
@when("scroll", window, passive=True)
def handle_scroll(event):
    # Can't call event.preventDefault() here.
    print("Scrolling...")
```

See [addEventListener options](https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener#options)
for details.

### Functions without event arguments

If your handler doesn't need the event object, you can omit it:

```python
from pyscript import when


@when("click", "#simple-button")
def simple_handler():
    """
    No event parameter needed.
    """
    print("Button clicked!")
```

PyScript detects whether your function accepts arguments and calls it
appropriately.

## Example: Interactive colour picker

Here's a complete example demonstrating various event handling
patterns:

<iframe src="../../example-apps/colour-picker/" style="border: 1px solid black; width:100%; min-height: 500px; border-radius: 0.2rem; box-shadow: var(--md-shadow-z1);"></iframe>

[View the complete source code](https://github.com/pyscript/docs/tree/main/docs/example-apps/colour-picker).

This example shows:

- Handling multiple event types (`input`, `click`, `change`).
- Working with form inputs.
- Updating the UI based on events.
- Custom events for decoupling logic.

## What's next

Now that you understand event handling, explore these related topics:

**[DOM Interaction](dom.md)** - Learn how to find and manipulate
elements that you're attaching events to.

**[Display](display.md)** - Discover how to show Python objects, images,
charts, and rich content on your page with the `display()` function.

**[Configuration](configuration.md)** - Configure how your scripts load
and when event handlers are attached.

**[Workers](workers.md)** - Discover how to handle events in background
threads for responsive applications.