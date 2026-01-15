# PyGame Support

PyScript includes experimental support for
[PyGame Community Edition](https://pyga.me/), a Python library for
building games. PyGame-CE runs in the browser through PyScript, letting
you share games via URL without requiring players to install Python or
any dependencies.

This guide explains how to use PyGame-CE with PyScript, covering the
differences from traditional PyGame development and techniques for
making games work well in the browser.

!!! warning

    PyGame-CE support is experimental. Behaviour may change based on
    community feedback and bug reports. Please share your experiences
    via Discord or GitHub to help improve this feature.

## Quick start

Create a PyGame-CE application by using the `py-game` script type:

```html
<script type="py-game" src="my_game.py"></script>
```

PyGame-CE loads automatically - no pip installation needed. Your game
runs in the browser and can be shared via URL like any other web page.

Refer to [PyGame-CE's documentation](https://pyga.me/docs/) for game
development techniques. Most features work in the browser, though some
may behave differently due to the browser environment.

## Browser considerations

PyGame-CE in the browser differs from local development in several key
ways. Understanding these differences helps you write games that work
well in both environments.

The browser needs regular opportunities to update the canvas displaying
your game. Replace `clock.tick(fps)` with `await asyncio.sleep(1/fps)`
to give the browser time to render. Better timing techniques exist and
are covered later in this guide.

Media files like images and sounds must be explicitly loaded using
PyScript's configuration system. Use the `files` section in your
configuration to make assets available.

Python and PyGame-CE versions in the browser may lag behind the latest
releases. Check the browser console when PyGame-CE starts to see which
versions are available. Functions marked "since 2.5" in the
documentation won't work if version 2.4.1 is bundled.

## Complete example

Here's a complete bouncing ball game demonstrating PyGame-CE in the
browser:

<iframe src="../../example-apps/bouncing-ball/" style="border: 1px solid black; width:100%; min-height: 500px; border-radius: 0.2rem; box-shadow: var(--md-shadow-z1);"></iframe>

[View the complete source code](https://github.com/pyscript/docs/tree/main/docs/example-apps/bouncing-ball).

This example shows the essential pattern for PyGame-CE in PyScript. The
game uses `await asyncio.sleep(1/60)` to yield control to the browser
for canvas updates.

The Python code:

```python
import asyncio
import sys
import pygame

pygame.init()

size = width, height = 320, 240
speed = [2, 2]
black = 0, 0, 0

screen = pygame.display.set_mode(size)
ball = pygame.image.load("intro_ball.gif")
ballrect = ball.get_rect()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]

    screen.fill(black)
    screen.blit(ball, ballrect)
    pygame.display.flip()
    await asyncio.sleep(1/60)
```

The only addition to standard PyGame code is `await asyncio.sleep(1/60)`,
which gives the browser time to render. The `await` at the top level
works in PyScript's async context but won't run locally without
modification (covered below).

The HTML file needs a canvas element and the script tag:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <title>PyScript PyGame-CE Example</title>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1.0">
  <link rel="stylesheet" 
    href="https://pyscript.net/releases/2025.11.2/core.css">
  <script type="module" 
    src="https://pyscript.net/releases/2025.11.2/core.js"></script>
</head>
<body>
  <canvas id="canvas" style="image-rendering: pixelated"></canvas>
  <script type="py-game" src="quickstart.py" 
    config="pyscript.toml"></script>
</body>
</html>
```

!!! info

    The `style="image-rendering: pixelated"` preserves the pixelated
    look on high-DPI screens. Remove it for smoothed rendering.

The configuration file lists game assets:

```toml
[files]
"intro_ball.gif" = ""
```

Download `intro_ball.gif` from the
[example on this website](../example-apps/bouncing-ball/intro_ball.gif).

## Running locally and in browser

The top-level `await` in the example isn't valid in standard Python (it
should be inside an async function). PyScript provides an async context
automatically, but local Python doesn't.

Wrap your game in an async function and use a try-except block to detect
the environment:

```python
import asyncio
import sys
import pygame


async def run_game():
    """
    Main game function.
    """
    pygame.init()

    # Initialise game state...
    size = width, height = 320, 240
    screen = pygame.display.set_mode(size)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        
        # Game logic...
        
        await asyncio.sleep(1/60)


try:
    # Check if we're in an async context (PyScript).
    asyncio.get_running_loop()
    asyncio.create_task(run_game())
except RuntimeError:
    # No async context (local Python).
    asyncio.run(run_game())
```

This pattern works in both environments. PyScript uses `create_task()`,
local Python uses `asyncio.run()`. Now you can develop locally and
publish to the web without changing code.

!!! info

    The `pygame.QUIT` event never fires in the browser version, but
    handling it is mandatory for local execution where closing the
    window generates this event.

## Precise frame timing

The `await asyncio.sleep(1/60)` approach approximates 60 FPS but isn't
precise. Frame rendering takes time, so sleeping 1/60th of a second
results in actual FPS below 60.

Better timing synchronises with the display refresh rate using
`requestAnimationFrame` in the browser and `vsync=1` locally. This
requires separating setup from the game loop:

```python
import sys
import pygame

pygame.init()

size = width, height = 320, 240
speed = pygame.Vector2(150, 150)
black = 0, 0, 0

screen = pygame.display.set_mode(size, vsync=1)
ball = pygame.image.load("intro_ball.gif")
ballrect = ball.get_rect()
clock = pygame.time.Clock()


def run_one_frame():
    """
    Execute one frame of the game.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    
    # Delta time for frame-rate independence.
    dt = clock.tick(300) / 1000
    
    ballrect.move_ip(speed * dt)
    
    # Bounce logic...
    if ballrect.left < 0 or ballrect.right > width:
        speed.x = -speed.x
    if ballrect.top < 0 or ballrect.bottom > height:
        speed.y = -speed.y
    
    screen.fill(black)
    screen.blit(ball, ballrect)
    pygame.display.flip()


# Browser: use requestAnimationFrame.
try:
    from pyscript import window, ffi
    
    def on_animation_frame(timestamp):
        """
        Called by browser for each frame.
        """
        run_one_frame()
        window.requestAnimationFrame(raf_proxy)
    
    raf_proxy = ffi.create_proxy(on_animation_frame)
    on_animation_frame(0)

except ImportError:
    # Local: use while loop with vsync.
    while True:
        run_one_frame()
```

This synchronises with display refresh (usually 60Hz, but can be higher).
Delta time (`dt`) accounts for frame rate variations between machines.
Speed is now in pixels per second, multiplied by `dt` to get movement
per frame.

The `vsync=1` parameter makes `flip()` block until the display updates
locally. In the browser, `vsync=1` does nothing - instead,
`requestAnimationFrame` controls timing.

Note that variable frame rates can cause physics issues. The ball might
get stuck in walls if frame skipping occurs. For beginners, the simpler
`asyncio.sleep` method may be easier despite being less precise.

## How PyGame-CE integration works

The `py-game` script type bootstraps Pyodide with PyGame-CE
pre-installed. Unlike regular scripts, PyGame-CE always runs on the main
thread and cannot use workers.

The `target` attribute specifies which canvas element displays the game.
If omitted, PyScript assumes a `<canvas id="canvas">` element exists.

Configuration through the `config` attribute adds packages or files like
images and sounds. This is currently the only configuration PyGame-CE
scripts support.

!!! info

    The `input()` function works in PyGame-CE but uses the browser's
    native `prompt()` dialog. Since PyGame-CE runs on the main thread,
    this is the only way to block for user input. PyScript handles this
    automatically when you call `input()`.

## Experimental status

PyGame-CE support is experimental but functional. You can load
`pygame-ce` manually through regular PyScript if needed, but the
`py-game` script type simplifies multi-game pages and ensures game logic
runs on the main thread where PyGame-CE expects it.

Future PyScript versions may include other game engines alongside
PyGame-CE. We welcome feedback, suggestions, and bug reports to improve
this feature.

## What's next

Now that you understand PyGame-CE support, explore these related topics:

**[Terminal](terminal.md)** - Use the alternative REPL-style
interface for interactive Python sessions.

**[Editor](editor.md)** - Create interactive Python coding environments in
web pages with the built-in code editor.

**[PyScript in JavaScript](from_javascript.md)** - drive PyScript from the
world JavaScript. 

**[Plugins](plugins.md)** - Understand the plugin system, lifecycle hooks,
and how to write plugins that integrate with PyScript.