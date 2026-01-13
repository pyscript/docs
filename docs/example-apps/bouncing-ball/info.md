# Bouncing Ball

[Run the app](index.html) | 
[View the code on GitHub](https://github.com/pyscript/docs/tree/main/docs/example-apps/bouncing-ball)

A simple PyGame-CE demonstration running in the browser with PyScript.
Based on the
[PyGame-CE quickstart tutorial](https://pyga.me/docs/tutorials/en/intro-to-pygame.html).

## What it demonstrates

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