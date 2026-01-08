# Prime Number Calculator with Workers

A demonstration of PyScript workers showing how to keep the main thread
responsive whilst performing heavy computation in a background worker.

## What it demonstrates

**Worker architecture:**
- **Main thread**: MicroPython (lightweight, fast startup, responsive UI).
- **Worker thread**: Pyodide with numpy (heavy computation, numerical
  libraries).
- Clear separation of concerns.

**Key patterns:**
- Starting a worker from the main thread.
- Calling worker methods with `await`.
- Sending incremental results back via callbacks.
- Using `pyscript.sync` to expose functions between threads.
- Keeping the main thread responsive during computation.

**Visual feedback:**
- Animated "heartbeat" proves main thread never blocks.
- Real-time display of primes as they're found.
- Status updates showing worker progress.

## How it works

### Main thread (MicroPython)

The main thread handles the user interface:

1. Gets reference to the worker via `pyscript.workers`.
2. Registers a callback function (`handle_prime`) via `pyscript.sync`.
3. Calls the worker's `find_primes()` method when the button is clicked.
4. Receives prime numbers via the callback and updates the display.
5. Stays responsive throughout (watch the pulsing green dot).

### Worker thread (Pyodide)

The worker does the heavy lifting:

1. Exposes `find_primes()` method via `@sync` decorator.
2. Uses numpy's efficient array operations for the Sieve of Eratosthenes.
3. Calls back to the main thread's `handle_prime()` for each prime found.
4. Sends results in batches with small delays to keep UI smooth.
5. Returns a summary when complete.

## Files

- `index.html` - Page structure and styling.
- `main.py` - Main thread logic (MicroPython).
- `worker.py` - Worker thread logic (Pyodide with numpy).
- `worker-config.json` - Worker configuration (numpy package).

## Key code patterns

### Starting the worker

```python
# Main thread gets reference to worker defined in HTML.
from pyscript import workers

worker = await workers.py  # Name from script tag's type.
```

### Calling worker methods

```python
# Main thread calls worker method (must be decorated with @sync).
result = await worker.find_primes(10000)
```

### Worker exposing methods

```python
# Worker exposes method to main thread.
from pyscript import sync

@sync
async def find_primes(limit):
    # Do computation.
    return result
```

### Callbacks from worker to main

```python
# Main thread registers callback.
from pyscript import sync

async def handle_prime(prime):
    print(f"Got prime: {prime}")

sync.handle_prime = handle_prime

# Worker calls back to main thread.
handle_prime = await sync.handle_prime
await handle_prime(42)
```

## Why this architecture?

**MicroPython on main thread:**
- Fast startup (no heavy packages to load).
- Lightweight (perfect for UI interactions).
- Stays responsive (no blocking operations).

**Pyodide in worker:**
- Full Python with scientific libraries (numpy).
- Heavy computation off the main thread.
- Can use the full Python ecosystem.

**Best of both worlds:**
- Fast, responsive UI.
- Powerful computation when needed.
- Users never see a frozen interface.

## Try it

1. Enter a number (10 to 100,000).
2. Click "Find Primes".
3. Watch the green heartbeat - it never stops pulsing.
4. See primes appear in real-time.

Try interacting with the page whilst it's computing - everything stays
smooth because the main thread is never blocked.

## Running locally

Serve these files from a web server:

```bash
python3 -m http.server
```

Then open http://localhost:8000 in your browser.

**Note**: You'll need to serve with appropriate CORS headers for workers
to access `window` and `document`. See the
[workers guide](../../user-guide/workers.md#http-headers) for details.