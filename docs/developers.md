# Developer Guide

This page explains the technical and practical requirements and processes
needed to contribute to PyScript.

!!! info

    In the following instructions, we assume familiarity with `git`,
    [GitHub](https://github.com/pyscript/pyscript), the command line and other
    common development concepts, tools and practices.

    For those who come from a non-Pythonic technical background (for example,
    you're a JavaScript developer), we will explain Python-isms as we go along
    so you're contributing with confidence.

    If you're unsure, or encounter problems, please ask for help on our
    [discord server](https://discord.gg/HxvBtukrg2).

## Welcome 

We are a diverse, inclusive coding community and welcome contributions from
_anyone_ irrespective of their background. If you're thinking, "but they don't
mean me", _then we especially mean YOU_. Our diversity means _you will meet
folks in our community who are different to yourself_. Therefore, thoughtful
contributions made in good faith, and engagement with respect, care and
compassion wins every time.

* If you're from a background which isn't well-represented in most geeky
  groups, get involved - _we want to help you make a difference_.
* If you're from a background which **is** well-represented in most geeky
  groups, get involved - _we want your help making a difference_.
* If you're worried about not being technical enough, get involved - _your
  fresh perspective will be invaluable_.
* If you need help with anything, get involved - _we welcome questions asked
  in good faith, and will move mountains to help_.
* If you're unsure where to start, get involved - _we have [many ways to
  contribute](/contributing)_.

All contributors are expected to follow our [code of conduct](/conduct/).

## Setup 

**You must have recent versions of [Python](https://python.org/),
[node.js](https://nodejs.org/en) and [npm](https://www.npmjs.com/) already
installed on your system.**

The following steps create a working development environment for PyScript. It
is through this environment that you contribute to PyScript.

!!! danger

    The following commands work on Unix like operating systems (like MacOS or
    Linux). **If you are a Microsoft Windows user please use the
    [Windows Subsystem for Linux](https://learn.microsoft.com/en-us/windows/wsl/about)
    with the following instructions.**

### Create a virtual environment

* A Python [virtual environment](https://docs.python.org/3/library/venv.html) 
  is a computing "sandbox" that safely isolates your work. PyScript's
  development makes use of various Python based tools, so both
  [Python](https://python.org) and a virtual environment is needed. There are
  many tools to help manage these environments, but the standard way to create
  a virtual environment is to use this command in your terminal:

    ```sh
    python3 -m venv my_pyscript_dev_venv
    ```

    !!! warning

        Replace `my_pyscript_dev_venv` with a meaningful name for the
        virtual environment, that works for you.

* A `my_pyscript_dev_venv` directory containing the virtual environment's
  "stuff" is created as a subdirectory of your current directory. Next,
  activate the virtual environment to ensure your development activities happen
  within the context of the sandbox:

    ```sh
    source my_pyscript_dev_venv/bin/activate
    ```

* The prompt in your terminal will change to include the name of your virtual
  environment indicating the sandbox is active. To deactivate the virtual
  environment just type the following into your terminal:

    ```sh
    deactivate
    ```

!!! info

    The rest of the instructions on this page assume you are working in **an
    activated virtual environment** for developing PyScript.

### Prepare your repository

* Create a [fork](https://docs.github.com/en/get-started/quickstart/fork-a-repo)
  of the
  [PyScript github repository](https://github.com/pyscript/pyscript/fork) to
  your own GitHub account.
* [Clone](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)
  your newly forked version of the PyScript repository onto your
  local development machine. For example, use this command in your terminal:

    ```sh
    git clone https://github.com/<YOUR USERNAME>/pyscript
    ```

    !!! warning

        In the URL for the forked PyScript repository, remember to replace
        `<YOUR USERNAME>` with your actual GitHub username.

    !!! tip

        To help explain steps, we will use `git` commands to be typed into your
        terminal / command line.

        The equivalent of these commands could be achieved through other means
        (such as [GitHub's desktop client](https://desktop.github.com/)). How
        these alternatives work is beyond the scope of this document.

* Change into the root directory of your newly cloned `pyscript` repository:

      ```sh
      cd pyscript
      ```

* Add the original PyScript repository as your `upstream` to allow you to keep
  your own fork up-to-date with the latest changes:

      ```sh
      git remote add upstream https://github.com/pyscript/pyscript.git
      ```

* If the above fails, try this alternative:

      ```sh
      git remote remove upstream
      git remote add upstream git@github.com:pyscript/pyscript.git
      ```

* Pull in the latest changes from the main `upstream` PyScript repository:

      ```sh
      git pull upstream main
      ```

* Pyscript uses a `Makefile` to automate the most common development tasks. In
  your terminal, type `make` to see what it can do. You should see something
  like this:

    ```sh
    There is no default Makefile target right now. Try:

    make setup - check your environment and install the dependencies.
    make clean - clean up auto-generated assets.
    make build - build PyScript.
    make precommit-check - run the precommit checks (run eslint).
    make test-integration - run all integration tests sequentially.
    make fmt - format the code.
    make fmt-check - check the code formatting.
    ```

### Install dependencies

* To install the required software dependencies for working on PyScript, in
  your terminal type:

    ```sh
    make setup
    ```

* Updates from `npm` and then `pip` will scroll past telling you about
  their progress installing the required packages.

    !!! warning

        The `setup` process checks the versions of Python, node
        and npm. If you encounter a failure at this point, it's probably
        because one of these pre-requisits is out of date on your system.
        Please update!

## Check code

* To ensure consistency of code layout we use tools to both reformat and check
  the code.

* To ensure your code is formatted correctly:

    ```sh
    make fmt
    ```

* To check your code is formatted correctly:

    ```sh
    make fmt-check
    ```

* Finally, as part of the automated workflow for contributing
  [pull requests](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request)
  pre-commit checks the source code. If this fails revise your PR. To run
  pre-commit checks locally (before creating the PR):

    ```sh
    make precommit-check
    ```

    This may also revise your code formatting. Re-run `make precommit-check` to
    ensure this is the case.

## Build PyScript

* To turn the JavaScript source code found in the `pyscript.core` directory
  into a bundled up module ready for the browser, type:

    ```sh
    make build
    ```

    The resulting assets will be in the `pyscript.core/dist` directory.

## Run the tests

* The integration tests for PyScript are started with:

    ```sh
    make test-integration
    ```

## Documentation

* Documentation for PyScript (i.e. what you're reading right now), is found
  in a separate repository:
  [https://github.com/pyscript/docs](https://github.com/pyscript/docs)

* The documentation's `README` file contains instructions for setting up a
  development environment and contributing.

## Contributing

* We have [suggestions for how to contribute to PyScript](/contributing). Take
  a read and dive in.

* Please make sure you discuss potential contributions *before* you put in
  work. We don#t want folks to waste their time or re-invent the wheel.

* Technical discussions happen [on our discord server](https://discord.gg/HxvBtukrg2)
  and in the
  [discussions section](https://github.com/pyscript/pyscript/discussions) of
  our GitHub repository.

* Every Tusday is a community video call, the details of which are posted onto
  the discord server. Face to face technical discussions happen here.

* Every two weeks, on a Thursday, is a PyScript FUN call, the details of which
  are also posted to discord. Project show-and-tells, cool hacks, new features
  and a generally humorous and creative time is had by all.
