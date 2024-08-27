# Example applications

A curated list of example applications that demonstrate various features of
PyScript can be found [on PyScript.com](https://pyscript.com/@examples).

The examples are (links take you to the code):

### Simple:

* [Hello world](https://pyscript.com/@examples/hello-world/latest)
  * uses included datetime module. No additional packages.
* [A simple clock](https://pyscript.com/@examples/simple-clock/latest)
  * Not found
* [WebGL Icosahedron](https://pyscript.com/@examples/webgl-icosahedron/latest)
  * uses very old version of [three.js](https://threejs.org/) directly imported in index.html. (not as a module in toml) 
* [Pandas dataframe fun](https://pyscript.com/@examples/pandas/latest)
  * uses [pandas](https://pandas.pydata.org/) from pypi
  * pyodide
* [Matplotlib example](https://pyscript.com/@examples/matplotlib/latest)
  * uses [matplotlib](https://matplotlib.org/)
  * not clear how numpy is being loaded as it is not referenced.
  * pyodide
* [Todo](https://pyscript.com/@examples/todo-app/latest)
  * uses pyweb. No additional packages.
  * pyodide
* [Tic Tac Toe](https://pyscript.com/@examples/tic-tac-toe/latest)
  * uses pyweb. No additional packages.
  * pyodide
* [Pyscript Jokes](https://pyscript.com/@examples/pyscript-jokes/latest)
  * uses pyweb and [pyjokes](https://pyjok.es/)
  * pyodide
* [D3 visualization](https://pyscript.com/@examples/d3-visualization/latest)
  * uses [d3](https://d3js.org/)
  * mixes javascript code with python code. imports d3 from javascript.
  * pyodide
* [Import antigravity](https://pyscript.com/@examples/antigravity/latest)
  * uses svg
  * pyodide
* [API proxy tutorial](https://pyscript.com/@examples/api-proxy-tutorial/latest)
  * uses fetch
  * pyodide
* [API proxy and secrets tutorial](https://pyscript.com/@examples/api-proxy-and-secrets-tutorial/latest)
  * uses fetch
  * pyodide

### More complex:

* [Numpy fractals](https://pyscript.com/@examples/fractals-with-numpy-and-canvas/latest)
  * uses [numpy](https://numpy.org/), [sympy](https://www.sympy.org/en/index.html) from pypi
  * pyodide
* [Simple slider panel](https://pyscript.com/@examples/simple-panel/latest)
  * uses [Panel](https://panel.holoviz.org/) and [Bokeh](https://bokeh.org/) from pypi and loads in index.html
  * does not run
  * pyodide
* [Streaming data panel](https://pyscript.com/@examples/streaming-in-panel/latest)
  * uses  [Panel](https://panel.holoviz.org/), [Bokeh](https://bokeh.org/)  [numpy](https://numpy.org/), [pandas](https://pandas.pydata.org/) from pypi
  * loads bokeh, panel, tabulator in index.html
  * pyodide
* [KMeans in a panel](https://pyscript.com/@examples/kmeans-in-panel/latest)
  * uses [Bokeh](https://bokeh.org/), [altair](https://altair-viz.github.io/), [numpy](https://numpy.org/), [pandas](https://pandas.pydata.org/), [scikit-learn](https://scikit-learn.org/stable/), [Panel](https://panel.holoviz.org/) from pypi
  * loads panel, bootstrap, vega, tabulator, bokeh in index.html
  * runs but displays errors to do with threadpools
  * pyodide
* [New York Taxi panel (WebGL)](https://pyscript.com/@examples/nyc-taxi-panel-deckgl/latest)
  * uses a mixture of pypi and direct load packages in index.html
  * [Bokeh](https://bokeh.org/), [numpy](https://numpy.org/), [pandas](https://pandas.pydata.org/), [Panel](https://panel.holoviz.org/), [deck-gl](https://deck.gl/)
  * deckGL, bokeh are loaded directly in index.html
  * pyodide
* [Folium geographical data](https://pyscript.com/@examples/folium/latest)
  * uses [folium](https://python-visualization.github.io/folium/latest/), [pandas](https://pandas.pydata.org/)  from pypi
  * pyodide
* [Bokeh data plotting](https://pyscript.com/@examples/bokeh/latest)
  * uses [pandas](https://pandas.pydata.org/), [Bokeh](https://bokeh.org/), [xyzservices](https://github.com/geopandas/xyzservices) from pypi
  * pyodide
* [Altair data plotting](https://pyscript.com/@examples/altair/latest)
  * uses [altair](https://altair-viz.github.io/), [pandas](https://pandas.pydata.org/), [vega_datasets](https://github.com/altair-viz/vega_datasets) from pypi
  * pyodide
* [Panel and hyplot](https://pyscript.com/@examples/panel-and-hvplot/latest)
  * uses [Bokeh](https://bokeh.org/), [Panel](https://panel.holoviz.org/), [markdown-it-py](https://github.com/executablebooks/markdown-it-py), [numpy](https://numpy.org/), [pandas](https://pandas.pydata.org/), [hvplot](https://hvplot.holoviz.org/), [pyodide-http](https://pyodide.org/en/stable/usage/api/python-api/http.html) a fetch library.
  * bokeh and panel are loaded in the index.html
  * pyodide

Notes:
 - Updated from 14 to 20 found at above link
 - No micropython examples - all are pyodide
 - No worker examples
 - async used in some examples - probably obsolete now
 - fetch done several ways
