# PyGame Support

!!! Danger 

    **Support for PyGame-CE is experimental** and its behaviour is likely to
    change as we get feedback and bug reports from the community.

    Please bear this in mind as you try PyGame-CE with PyScript, and all
    feedback, bug reports and constructive critique is welcome via discord
    or GitHub.


[PyGameCE](https://pyga.me/) is a Python library for building powerful games
(so says their website). They also say, to get started you just need to
`pip install pygame-ce`.

Thanks to work in the upstream [Pyodide project](https://pyodide.org/)
PyGame-CE is available in PyScript and to get started all you need to do is:
`<script type="py-game" src="my_game.py"></script>` Now you don't even need to
`pip install` the library! It comes with PyScript by default, and you can share
your games via a URL!

!!! Info

    Please refer to
    [PyGame-CE's extensive documentation](https://pyga.me/docs/) for how to
    create a game. Some things may not work because we're running in a
    browser context, but play around and let us know how you get on.

## Getting Started

Here are some notes on using PyGame-CE specifically in a browser context with
pyscript versus running locally per
[PyGame-CE's documentation](https://pyga.me/docs/).

1. You can use [pyscript.com](https://pyscript.com) as mentioned in
   [Beginning PyScript](../beginning-pyscript.md) for an easy starting
   environment.
2. Pyscript's PyGame-CE is under development, so make sure to use the latest
   version by checking the `index.html` and latest version on this website. If
   using [pyscript.com](https://pyscript.com), the latest version is not always
   used in a new project.
3. The game loop needs to allow the browser to run to update the canvas used as
   the game's screen. In the simplest projects, the quickest way to do that is
   to replace `clock.tick(fps)` with `await asyncio.sleep(1/fps)`, but there
   are better ways (discussed later).
4. If you have multiple Python source files or media such as images or sounds,
   you need to use the [config attribute](configuration.md) to load the
   files into the PyScript environment. The below example shows how to do this.
5. The integrated version of Python and PyGame-CE may not be the latest. In the 
   browser's console when PyGame-CE starts you can see the versions, and for 
   example if 2.4.1 is included, you can't use a function marked in the 
   documentation as "since 2.5".

### Example

This is the example quickstart taken from the [Python Pygame 
Introduction](https://pyga.me/docs/tutorials/en/intro-to-pygame.html) on the 
PyGame-CE website, modified only to add `await asyncio.sleep(1/60)` (and the 
required `import asyncio`) to limit the game to roughly 60 fps.

Note: since the `await` is not in an `async` function, it cannot run using
Python on your local machine, but a solution is
[discussed later](#running-locally).


```python title="quickstart.py"
import asyncio
import sys, pygame

pygame.init()

size = width, height = 320, 240
speed = [2, 2]
black = 0, 0, 0

screen = pygame.display.set_mode(size)
ball = pygame.image.load("intro_ball.gif")
ballrect = ball.get_rect()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

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

To run this game with PyScript, use the following HTML file, ensuring a call
to the Python program and a `<canvas id="canvas">` element where the graphics
will be placed. Make sure to update the pyscript release to the latest version.

```html title="index.html"
<!DOCTYPE html>
<html lang="en">

<head>
  <title>PyScript Pygame-CE Quickstart</title>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1.0">
  <link rel="stylesheet" href="https://pyscript.net/releases/2025.8.1/core.css">
  <script type="module" src="https://pyscript.net/releases/2025.8.1/core.js"></script>
</head>
<body>
<canvas id="canvas" style="image-rendering: pixelated"></canvas>
<script type="py-game" src="quickstart.py" config='pyscript.toml'></script>
</body>
</html>
```

!!! Info

    The `style="image-rendering: pixelated` on the canvas preserves the
    pixelated look on high-DPI screens or when zoomed-in. Remove it to have a
    "smoothed" look.
    
Lastly, you need to define the `pyscript.toml` file to expose any files that
your game loads -- in this case, `intro_ball.gif`
[(download from pygame GitHub)](https://github.com/pygame-community/pygame-ce/blob/80fe4cb9f89aef96f586f68d269687572e7843f6/docs/reST/tutorials/assets/intro_ball.gif?raw=true).

```toml title="pyscript.toml"
[files]
"intro_ball.gif" = ""
```

Now you only need to serve the 3 files to a browser. If using 
[pyscript.com](https://pyscript.com) you only need to ensure the content of the 
files, click save then run and view the preview tab. Or, if you are on a machine 
with Python installed you can do it from a command line running in the same 
directory as the project:

```
python -m http.server -b 127.0.0.1 8000
```

This will start a website accessible only to your machine (`-b 127.0.0.1` limits 
access only to "localhost" -- your own machine). After running this, you can 
visit [http://localhost:8000/](http://localhost:8000/) to run the game in your
browser.

Congratulations! Now you know the basics of updating games to run in PyScript.
You can continue to develop your game in the typical PyGame-CE way.

## Running Locally

Placing an `await` call in the main program script as in the example is not 
technically valid Python as it should be in an `async` function. In the
environment executed by PyScript, the code runs in an `async` context so this
works; however, you will notice you cannot run the `quickstart.py` on your
local machine with Python. To fix that, you need to add just a little more
code:

Place the entire game in a function called `run_game` so that function can be 
declared as `async`, allowing it to use `await` in any environment. Import the 
`asyncio` package and add the `try ... except` code at the end. Now when running 
in the browser, `asyncio.create_task` is used, but when running locally 
`asyncio.run` is used. Now you can develop and run locally but also support 
publish to the web via PyScript.

```python
import asyncio
import sys, pygame

async def run_game():
    pygame.init()

    # Game init ...

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            
        # Game logic ...
        
        await asyncio.sleep(1/60)

try:
    asyncio.get_running_loop() # succeeds if in async context
    asyncio.create_task(run_game())
except RuntimeError:
    asyncio.run(run_game()) # start async context as we're not in one
```

!!! Info

    In the web version, the `sys.exit()` was never used because the `QUIT`
    event is not generated, but in the local version, responding to the event
    is mandatory.
    
## Advanced Timing

While the `await asyncio.sleep(1/60)` is a quick way to approximate 60 FPS,
like all sleep-based timing methods in games this is not precise. Generating
the frame itself takes time, so sleeping 1/60th of a second means total frame
time is longer and actual FPS will be less than 60.

A better way is to do this is to run your game at the same frame rate as the 
display (usually 60, but can be 75, 100, 144, or higher on some displays). When 
running in the browser, the proper way to do this is with the JavaScript API 
called `requestAnimationFrame`. Using the FFI (foreign function interface) 
capabilities of PyScript, we can request the browser's JavaScript runtime to 
call the game. The main issue of this method is it requires work to separate the 
game setup from the game's execution, which may require more advanced Python 
code such as `global` or `class`. However, one benefit is that the `asyncio` 
usages are gone.


When running locally, you get the same effect from the `vsync=1` parameter on 
`pygame.display.set_mode` as `pygame.display.flip()` will pause until the screen 
has displayed the frame. In the web version, the `vsync=1` will do nothing, 
`flip` will not block, leaving the browser itself to control the timing using 
`requestAnimationFrame` by calling `run_one_frame` (via `on_animation_frame`) 
each time the display updates.

Additionally, since frame lengths will be different on each machine, we need to
account for this by creating and using a `dt` (delta time) variable by using a
`pygame.time.Clock`. We update the speed to be in pixels per second and multiply
by `dt` (in seconds) to get the number of pixels to move.

The code will look like this:

```python
import sys, pygame

pygame.init()

size = width, height = 320, 240
speed = pygame.Vector2(150, 150) # use Vector2 so we can multiply with dt
black = 0, 0, 0

screen = pygame.display.set_mode(size, vsync=1) # Added vsync=1
ball = pygame.image.load("intro_ball.gif")
ballrect = ball.get_rect()
clock = pygame.time.Clock() # New clock defined

def run_one_frame():
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        
    # in this 300 is for maximum frame rate only, in case vsync is not working
    dt = clock.tick(300) / 1000

    ballrect.move_ip(speed * dt) # use move_ip to avoid the need for "global"
    # Remaining game code unchanged ...
    
    pygame.display.flip()

    
# PyScript-specific code to use requestAnimationFrame in browser
try:
    from pyscript import window
    from pyscript import ffi
    # Running in PyScript
    def on_animation_frame(dt):
        # For consistency, we use dt from pygame's clock even in browser
        run_one_frame()
        window.requestAnimationFrame(raf_proxy)
    raf_proxy = ffi.create_proxy(on_animation_frame)
    on_animation_frame(0)
    
except ImportError:
    # Local Execution
    while True:
        run_one_frame()
```

A benefit of `vsync` / `requestAnimationFrame` method is that if the game is 
running too slowly, frames will naturally be skipped. A drawback is that in the 
case of skipped frames and different displays, `dt` will be different. This can
cause problems depending on your game's physics code; the potential solutions 
are not unique to the PyScript situation and can be found elsewhere online as an 
exercise for the reader. For example, the above example on some machines the 
ball will get "stuck" in the sides. In case of issues the `asyncio.sleep` method 
without `dt` is easier to deal with for the beginning developer.

## How it works

When a `<script type="py-game"></script>` element is found on the page a
Pyodide instance is bootstrapped with the `pygame-ce` package already included.
Differently from other scripts, `py-game` cannot currently work through a
worker and it uses an optional target attribute to define the `<canvas>`
element id that will be used to render the game. If no target attribute is
defined, the script assumes there is a `<canvas id="canvas">` element already
on the page.

A config attribute can be specified to add extra packages or bring in additional
files such as images and sounds but right now that's all it can do.

!!! Info

    Sometimes you need to gather text based user input when starting a game.
    The usual way to do this is via the builtin `input` function.

    Because PyGame-CE **only runs on the main thread**, the only way to block
    your code while it waits for user `input` is to use a
    [JavaScript prompt](https://developer.mozilla.org/en-US/docs/Web/API/Window/prompt)
    instead of input typed in via a terminal. PyScript handles this
    automatically for you if you use the `input` function.

This is an experiment, but:

* It is possible to use regular PyScript to load the pygame-ce package and use
  all the other features. But there be dragons! This helper simply allows
  multiple games on a page and forces game logic to run on the main thread to
  reduce confusion around attributes and features when the `pygame-ce` package
  is meant to be used. Put simply, we make it relatively safe and easy to use.
* The fact `pygame-ce` is the default "game engine" does not mean in the future
  PyScript won't have other engines also available.
* Once again, as this is an experiment, we welcome any kind of feedback,
  suggestions, hints on how to improve or reports of what's missing.

Other than that, please go make and share wonderful games. We can't wait to see
what you come up with.
