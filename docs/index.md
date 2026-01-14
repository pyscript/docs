
<div><img alt="PyScript Logo" src="assets/images/pyscript.svg"></div>

<h1 style="text-align: center; font-weight: bold;">PyScript is an <u>open source</u> platform for Python in the browser.</h1>

**Step 1:** Add these two lines to the `<head>` of your HTML document:

```html
<link rel="stylesheet" href="https://pyscript.net/releases/2025.11.2/core.css" />
<script type="module" src="https://pyscript.net/releases/2025.11.2/core.js"></script>
```

**Step 2:** Start PyScript with a `<script>` tag:

```html
<script type="py" config="./conf.json" src="./main.py"></script>
```

**Step 3:** Write Python (use the `pyscript` namespace):

```python
from pyscript import when, display


@when("click", "#my-button")
def handler():
    display("Button clicked!")
```

That's just the start of it!

What's next?

<dl>
  <dt><strong>I'm a beginner...</strong></dt>
  <dd>Welcome! PyScript is designed to be friendly for beginner coders. Start
  with our <a href="./beginning-pyscript">beginning PyScript guide</a>
  to create your first apps. Graduate to the
  <a href="./user-guide">user guide</a> to grow your understanding.</dd>
  <dt><strong>I'm already technical...</strong></dt>
  <dd>The beginner docs describe a
  <a href="./beginning-pyscript#editing-your-app">simple coding environment</a>.
  Consult the
  <a href="./user-guide">user guide</a> for comprehensive learning
  resources. The
  <a href="./example-apps/overview/">example applications</a> demonstrate many of
  the features of PyScript. The <a href="./api/init/">API docs</a> and <a href="./faq">FAQ</a>
  contain the technical details.</dd>
  <dt><strong>I want support...</strong></dt>
  <dd>
    <p>Join the conversation on our
    <a href="https://discord.gg/HxvBtukrg2" target="_blank">discord server</a>,
    for realtime chat with core maintainers and fellow users of PyScript.
    Check out <a href="https://www.youtube.com/@PyScriptTV" target="_blank">our YouTube
    channel</a>, full of community calls and show-and-tells.</p>
  </ul></dd>
  <dt><strong>I want to contribute...</strong></dt>
  <dd>
    <p>Welcome, friend!
    PyScript is an <a href="./license/">open source project</a>, we expect
    participants to act in the spirit of our
    <a href="./conduct/">code of conduct</a> and we have many 
    ways in which <a href="./contributing/"><u>you</u> can contribute</a>.
    Our <a href="./developers/">developer guide</a> explains how to set
    up a working development environment for PyScript.</p>
  </dd>
</dl>
