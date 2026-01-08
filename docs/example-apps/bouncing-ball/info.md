# Bouncing Ball

A simple PyGame-CE demonstration running in the browser with PyScript.
Based on the
[PyGame-CE quickstart tutorial](https://pyga.me/docs/tutorials/en/intro-to-pygame.html).

## What it shows

- Running PyGame-CE in the browser with the `py-game` script type.
- Using `await asyncio.sleep()` for frame timing in the browser.
- Loading game assets through PyScript configuration.
- Basic game loop with collision detection.

## How it works

The game initialises a pygame display, loads a ball image, and runs an
infinite game loop. Each frame, it updates the ball position, checks for
wall collisions (reversing speed on impact), renders the scene, and
yields control to the browser with `await asyncio.sleep(1/60)`.

The `await` at the top level works because PyScript provides an async
context. This wouldn't run in standard Python without wrapping in an
async function.

## Required files

You'll need to download `intro_ball.webp` from the PyGame-CE repository:
https://raw.githubusercontent.com/pygame-community/pygame-ce/80fe4cb9f89aef96f586f68d269687572e7843f6/docs/reST/tutorials/assets/intro_ball.gif

Place it in the same directory as the other files.

## Running locally

Serve the files with any web server:

```sh
python -m http.server 8000
```

Then visit `http://localhost:8000/` in your browser.