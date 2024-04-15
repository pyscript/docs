# Terminal

In conventional (non-browser based) Python, it is common to run scripts from
the terminal, or to interact directly with the Python interpreter via the
[REPL](https://en.wikipedia.org/wiki/Read%E2%80%93eval%E2%80%93print_loop).
It's to the terminal that `print` writes characters (via `stdout`), and it's
from the terminal that the `input` reads characters (via `stdin`).

It usually looks something like this:

<img src="../../assets/images/py-terminal.gif" style="border: 1px solid black; border-radius: 0.2rem; box-shadow: var(--md-shadow-z1);"/>

Because of the historic importance of the use of a terminal, PyScript makes one
available in the browser (based upon [XTerm.js](https://xtermjs.org/)).
As [mentioned earlier](first-steps.md), PyScript's built-in terminal is
activated with the `terminal` flag when using the `<script>`, `<py-script>` or
`<mpy-script>` tags.

!!! success 

    As of the 2024.4.1 release, MicroPython works with the terminal.

This is, perhaps, the simplest use case that allows data to be emitted to a
read-only terminal:

```html
<script type="py" terminal>print("hello world")</script>
```

The end result will look like this (the rectangular box indicates the current
position of the cursor):

<img src="../../assets/images/pyterm1.png" style="border: 1px solid black; border-radius: 0.2rem; box-shadow: var(--md-shadow-z1);"/>

Should you need an interactive terminal, for example because you use the
`input` statement that requires the user to type things into the terminal, you
**must ensure your code is run on a worker**:

```html
<script type="py" terminal worker>
name = input("What is your name? ")
print(f"Hello, {name}")
</script>
```
<img src="../../assets/images/pyterm2.gif" style="border: 1px solid black; border-radius: 0.2rem; box-shadow: var(--md-shadow-z1);"/>

To use the interactive Python REPL in the terminal, use Python's
[code](https://docs.python.org/3/library/code.html) module like this:

```python
import code

code.interact()
```

The end result should look something like this:

<img src="../../assets/images/pyterm3.gif" style="border: 1px solid black; border-radius: 0.2rem; box-shadow: var(--md-shadow-z1);"/>

Finally, it is possible to dynamically pass Python code into the terminal. The
trick is to get a reference to the terminal created by PyScript. Thankfully,
this is very easy.

Consider this fragment:

```html
<script id="my_script" type="mpy" terminal worker>
```

Get a reference to the element, and just call the `process` method on
that object:

```JS
const myterm = document.querySelector("#my_script");
await myterm.process('print("Hello world!")');
```
