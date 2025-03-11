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

## How it works

When a `<script type="py-game"></script>` element is found on the page a
Pyodide instance is bootstrapped with the `pygame-ce` package already included.
Differently from other scripts, `py-game` cannot currently work through a
worker and it uses an optional target attribute to define the `<canvas>`
element id that will be used to render the game. If no target attribute is
defined, the script assumes there is a `<canvas id="canvas">` element already
on the page.

A config attribute can be specified to add extra packages but right now that's
all it can do.

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
