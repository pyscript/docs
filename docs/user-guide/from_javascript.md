# PyScript in JavaScript

PyScript provides several APIs for JavaScript developers who want to
integrate Python functionality into their applications without writing
PyScript script tags. This guide covers three JavaScript APIs: shared
storage for data persistence between JavaScript and Python, the "Donkey"
for on-demand execution of Python as a worker based computation engine,
and the PyScript bridge, for importing Python modules directly into
JavaScript code.

## Shared storage

The storage API provides a shared key-value store accessible from both
JavaScript and Python. Data written from Python appears immediately in
JavaScript, and vice versa. This makes it simple to coordinate state
between languages without manual serialisation or message passing.

### Accessing storage in Python

Python code accesses storage through the `pyscript.storage` module:

```python title="Access storage from Python."
from pyscript import storage


my_store = await storage("shared")

# Write data that JavaScript can read.
my_store["user_count"] = 42
my_store["status"] = "active"

# Read data written by JavaScript.
config = my_store.get("config", {})
```

Storage operations are synchronous in Python. Values are automatically
serialised to formats JavaScript can understand.

### Accessing storage in JavaScript

JavaScript code imports the storage module from PyScript core:

```javascript title="Access storage in JavaScript."
import storage from 'https://pyscript.net/releases/2025.11.2/storage.js';


const my_store = await storage(name="shared");

// Read data written by Python.
const userCount = my_store["user_count"];
const status = my_store["status"];

// Write data that Python can read.
my_store["config"] = {
  theme: 'dark',
  language: 'en'
};

// Delete entries.
delete my_store["user_count"];
```

The storage object behaves like a regular JavaScript object, with
property access automatically synchronising with Python's view of the
data.

## The PyScript Donkey

The Donkey API provides an asynchronous Python worker ready to evaluate
code on demand. Think of it as a Python backend that shoulders the
burden of computation whilst keeping your JavaScript code simple. By
default any output from Python is piped to a terminal added to your
page (although this can be changed).

The name "donkey" reflects its purpose: something that waits patiently
until needed and carries heavy loads without complaint. This API lets you
use Python from pure JavaScript without writing PyScript tags.

### Asking for a Donkey

Import the `donkey` function and create a worker with it:

```javascript title="Call for the PyScript donkey."
import { donkey } from 'https://pyscript.net/releases/2025.11.2/core.js';

const py_donkey = await donkey({
  type: 'mpy',        // Use MicroPython ('py' for Pyodide).
  persistent: false,  // Reset state between executions.
  terminal: '',       // Optional terminal element selector.
  config: {}          // PyScript configuration object.
});
```

The donkey creates a worker with a terminal interface. The donkey function
returns a promise that resolves to an object with several methods for
executing Python code.

### Evaluate Python

The donkey worker provides six methods:

#### `process(code)`

Execute code and display it in the terminal:

```javascript
await py_donkey.process('print("Hello from Python!")');
```

This is the primary method for running Python code. The code executes
in the worker and output appears in the terminal. This behaves like
typing code into a Python REPL.

#### `execute(statement)`

Execute Python statements using Python's `exec()` function:

```javascript
await py_donkey.execute('x = 42');
await py_donkey.execute('print(x)');
```

Unlike `process()`, the code doesn't appear in the terminal, only the output
does.

#### `evaluate(expression)`

Evaluate a Python expression using Python's `eval()` function:

```javascript
const result = await py_donkey.evaluate('2 + 2');
console.log(result); // 4
```

Returns the result of the expression to JavaScript.

#### `clear()`

Clear terminal output:

```javascript
await py_donkey.clear();
```

This removes all content from the terminal display.

#### `reset()`

Reset the terminal including colours and state:

```javascript
await py_donkey.reset();
```

This completely resets the terminal to its initial state, including
clearing any colour or formatting settings.

#### `kill()`

Terminate the worker associated with the donkey:

```javascript
await py_donkey.kill();
```

You cannot use the donkey reference after calling `kill()`.
Ask for a new donkey if you need Python execution again.

### State management

The `persistent` option controls whether state persists between
executions:

```javascript title="State persistence."
// Non-persistent: each execution starts fresh.
const worker1 = await donkey({ type: 'mpy', persistent: false });
await worker1.execute('x = 10');
await worker1.evaluate('x'); // Error: x is not defined

// Persistent: variables remain available.
const worker2 = await donkey({ type: 'mpy', persistent: true });
await worker2.execute('x = 10');
await worker2.evaluate('x'); // 10
```

Non-persistent workers are simpler and prevent state leaking between
operations. Persistent workers let you build up context across multiple
executions.

### Terminal integration

The `terminal` option specifies where Python output appears:

```javascript title="Terminal output."
const py_donkey = await donkey({
  type: 'mpy',
  terminal: '#py_donkey-output'
});

await py_donkey.process('print("Hello from Python!")');
// Output appears in the element with id="py_donkey-output".
```

If no terminal is specified, PyScript creates a default terminal
element. To hide the terminal, point it to a hidden element:

```javascript title="Hiding the terminal output."
const py_donkey = await donkey({
  type: 'mpy',
  terminal: '#hidden-terminal'
});
```

Then style `#hidden-terminal` with `display: none` in your CSS.

### Configuration

The `config` option accepts [standard PyScript configuration](./configuration.md):

```javascript title="Configure the donkey."
const py_donkey = await donkey({
  type: 'py',
  config: {
    packages: ['numpy', 'pandas'],
    files: {
      'data.csv': './data.csv'
    }
  },
  persistent: true
});

await py_donkey.execute('import numpy as np');
const result = await py_donkey.evaluate('np.array([1, 2, 3]).sum()');
console.log(result); // 6
```

This loads packages and files before the worker becomes available,
ensuring all dependencies are ready.

## The Bridge API

The Bridge API lets you import Python modules directly into JavaScript
code. Python functions are proxied into JavaScript functions, to ensure
Python and JavaScript integrate well together.

This is perhaps the most seamless way to integrate specific Python
functionality into JavaScript: define Python functions, import them in
JavaScript, and call them as if they were JavaScript functions.

### Basic usage

Create a Python file with functions you want to export:

```python title="A simple Python module to use in JavaScript."
# calculations.py
def add(a, b):
    """
    Add two numbers.
    """
    return a + b


def multiply(a, b):
    """
    Multiply two numbers.
    """
    return a * b


def factorial(n):
    """
    Calculate factorial.
    """
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```

Create a JavaScript bridge module adjacent to the Python file:

```javascript title="Use the bridge to create a JavaScript module."
// calculations.js
import bridge from 'https://esm.run/@pyscript/bridge';

export const pystuff = bridge(import.meta.url, {
  type: 'mpy',
  worker: false
});
```

The bridge automatically finds `calculations.py` in the same directory
as `calculations.js` and makes available its top level functions.

Et voila! Import and use the Python functions in your JavaScript:

```javascript title="Use Python within JavaScript."
// main.js
import { pystuff } from './calculations.js';

// Wait for Python to load.
const { add, multiply, factorial } = await pystuff;

// Call Python functions from JavaScript.
console.log(await add(5, 3));        // 8
console.log(await multiply(4, 7));   // 28
console.log(await factorial(5));     // 120
```

Python functions become async JavaScript functions. Always use `await`
when calling them.

### Bridge options

The second argument to `bridge()` configures how Python loads:

#### `type`

The Python interpreter to use (`'py'` for Pyodide, `'mpy'` for
MicroPython). Default is `'py'`.

```javascript
export const pystuff = bridge(import.meta.url, { type: 'mpy' });
```

#### `worker`

Whether to run Python in a worker. Default is `true`.

```javascript
export const pystuff = bridge(import.meta.url, { worker: false });
```

Running in a worker keeps the main thread responsive but adds
serialisation overhead for arguments and return values. Running on the
main thread is faster for simple functions but can block the UI.

#### `config`

Standard [PyScript configuration](./configuration.md) for things like
packages and files:

```javascript title="Configure PyScript environment for the bridged code."
export const pystuff = bridge(import.meta.url, {
  type: 'py',
  config: {
    packages: ['numpy'],
    files: {
      'data.json': './data.json'
    }
  }
});
```

When `config` is specified, `worker` becomes implicitly `true` to avoid
configuration conflicts on the main thread.

#### `env`

Share environments across multiple modules:

```javascript title="Shared environments."
// Both modules share the same Python environment.
export const pystuff1 = bridge(import.meta.url, { env: 'shared' });
export const pystuff2 = bridge(import.meta.url, { env: 'shared' });
```

Shared environments let different bridge modules access the same Python
state and imports.

#### `pyscript`

The PyScript version to load if not already on the page:

```javascript title="Specify the PyScript version."
export const pystuff = bridge(import.meta.url, {
  pyscript: '2025.11.2'
});
```

If omitted, the latest version loads automatically. **Specify a version
for production stability**.

### Working with Python modules

The bridge imports all top-level functions from the Python file. You
can also import from Python packages:

```python title="A more complex module."
# utils.py
import json


def parse_json(text):
    """
    Parse JSON string.
    """
    return json.loads(text)


def stringify_json(obj):
    """
    Convert object to JSON string.
    """
    return json.dumps(obj)
```

```javascript title="Use the complex module in JavaScript."
import { pystuff } from './utils.js';

const { parse_json, stringify_json } = await pystuff;

const data = await parse_json('{"name": "Alice", "age": 30}');
console.log(data.name); // "Alice"

const text = await stringify_json({ status: 'ok', code: 200 });
console.log(text); // '{"status": "ok", "code": 200}'
```

### Error handling

Python exceptions propagate to JavaScript as rejected promises:

```python title="A contrived example that raises an exception."
# errors.py
def divide(a, b):
    """
    Divide two numbers.
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

```javascript title="Handle Python exceptions in JavaScript."
import { pystuff } from './errors.js';

const { divide } = await pystuff;

try {
  const result = await divide(10, 0);
} catch (error) {
  console.error(error.message); // "Cannot divide by zero"
}
```

Use try-catch blocks to handle Python errors in JavaScript.

## What's next

These JavaScript APIs complement the main PyScript functionality covered
in the user guide:

The [FFI guide](./ffi.md) explains how Python code calls JavaScript,
which is the reverse of what these APIs provide.

The [Workers guide](./workers.md) covers how workers affect performance
and responsiveness, relevant for understanding the `worker` option in
Donkey and Bridge APIs.

The [Configuration guide](./configuration.md) explains package loading and
file management, which applies to the `config` option in these APIs.
