# Features

<dl>
    <dt><em>All the web</em></dt>
    <dd>
    <p>Pyscript gives you <a href="../dom">full access to the DOM</a> and all
    the <a href="https://developer.mozilla.org/en-US/docs/Web/API">web
    APIs implemented by your browser</a>.</p>

    <p>Thanks to the <a href="../dom#ffi">foreign
    function interface</a> (FFI), Python just works with all the browser has to
    offer, including any third party JavaScript libraries that may be included
    in the page.</p>

    <p>The FFI is bi-directional ~ it also enables JavaScript to access the
    power of Python.</p></dd>

    <dt><em>All of Python</em></dt>
    <dd>
    <p>PyScript brings you two Python interpreters:</p>
    <ol>
        <li><a href="../architecture#pyodide">Pyodide</a> - the original standard
        CPython interpreter you know and love, but compiled to WebAssembly.
        </li>
        <li><a href="../architecture#micropython">MicroPython</a> - a lean and
        efficient reimplementation of Python3 that includes a comprehensive
        subset of the standard library, compiled to WebAssembly.</li>
    </ol>
    <p>Because it is just regular CPython, Pyodide puts Python's deep and
    <a href="https://pypi.org/">diverse ecosystem</a> of libraries, frameworks
    and modules at your disposal. No matter the area of computing endeavour,
    there's probably a Python library to help. Got a favourite library in
    Python? Now you can use it in the browser and share your work with just 
    a URL.</p>
    <p>MicroPython, because of its small size (170k) and speed, is especially
    suited to running on more constrained browsers, such as those on mobile
    or tablet devices. It includes a powerful sub-set of the Python standard
    library and efficiently exposes the expressiveness of Python to the
    browser.</p>
    <p>Both Python interpreters supported by PyScript implement the
    <a href="../dom#ffi">same FFI</a> to bridge the gap between the worlds of Python
    and the browser.</p>
    </dd>

    <dt><em>AI and Data science built in</em></dt>
    <dd>Python is famous for its extraordinary usefulness in artificial
    intelligence and data science. The Pyodide interpreter comes with many of
    the libraries you need for this sort of work already baked in.</dd>

    <dt><em>Mobile friendly MicroPython</em></dt>
    <dd>
    <p>Thanks to MicroPython in PyScript, there is a compelling story for
    Python on mobile.</p>

    <p>MicroPython is small and fast enough that your app will start quickly
    on first load, and almost instantly (due to the cache) on subsequent
    runs.</p></dd>

    <dt><em>Parallel execution</em></dt>
    <dd>Thanks to a browser technology called
    <a href="https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API">web workers</a>
    expensive and blocking computation can run somewhere other than the main
    application thread controlling the user interface. When such work is done
    on the main thread, the browser appears frozen; web workers ensure
    expensive blocking computation <a href="../workers">happens elsewhere</a>.
    Think of workers as independent subprocesses in your web page.</dd>

    <dt><em>Rich and powerful plugins</em></dt>
    <dd>
    <p>PyScript has a small, efficient yet powerful core called
    <a href="https://github.com/pyscript/polyscript">PolyScript</a>. Most of
    the functionality of PyScript is actually implemented through PolyScript's
    <a href="../plugins">plugin system</a>.</p>

    <p>This approach ensures a clear separation of concerns: PolyScript
    can focus on being small, efficient and powerful, whereas the PyScript
    related plugins allow us to build upon the solid foundations of
    PolyScript.</p>

    <p>Because there is a plugin system, folks
    <em>independent of the PyScript core team</em> have a way to create and
    contribute to a rich ecosystem of plugins whose functionality reflects the
    unique and diverse needs of PyScript's users.</p>
    </dd>
</dl>


