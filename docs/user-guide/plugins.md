# Plugins

PyScript, like many other software plaforms, offers a Plugin API that can be used to extend its
own functionality without the need to modify its own core. By using this API, users can add new
features and distribute them as plugins.

At the moment, PyScript supports plugins written in Javascript. These plugins can use PyScript
Plugins API to define entry points and hooks so that the plugin can be collected and hook into
the PyScript lifecycle events, with the ablity to modify and integrate the features of PyScript
core itself.

Here's an example of how a PyScript plugin looks like:

```js

```