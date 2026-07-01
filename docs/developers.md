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
  contribute](contributing.md)_.

All contributors are expected to follow our [code of conduct](conduct.md).

## Setup
The following steps create a working development environment for PyScript. It
is through this environment that you contribute to PyScript. You can choose
between two options for setting up your environment.

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

### Option 2: Create a conda environment
**This option will install Python and NodeJS for you, so you don't need to have them
pre-installed on your system.**

* If you prefer using [conda](https://docs.conda.io/en/latest/) for environment management,
you can create a conda environment that includes both Python and NodeJS:
* 
    ```sh
    conda create --name pyscript python nodejs
    conda activate pyscript
    ```
  
!!! warning

    Replace `pyscript` with a meaningful name for the conda environment, that works for you.

* This creates a new environment with both Python and NodeJS installed. The prompt in your
terminal will change to include the name of your conda environment indicating the sandbox is active.
* To deactivate the conda environment just type the following into your terminal:

    ```sh
    conda deactivate
    ```

* If you don't have conda installed, you can download and install
[Miniconda, Miniforge](https://docs.conda.io/projects/conda), or
[Anaconda](https://www.anaconda.com/download).

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
    make test
    ```
    
    (This essentially runs the `npm run test:integration` command in the right
    place. This is defined in PyScript's `package.json` file.)

    Tests are found in the `core/tests` directory. These are organised into
    three locations:

    1. `python` - the Python based test suite to exercise Python code
       **within** PyScript.
    2. `javascript` - JavaScript tests to exercise PyScript itself, in the
       browser.
    3. `manual` - containing tests to run manually in a browser, due to the
       complex nature of the tests.

    We use [Playwright](https://playwright.dev/) to automate the running of the
    Python and JavaScript test suites. We use
    [uPyTest](https://github.com/ntoll/upytest) as a test framework for the
    Python test suite. uPyTest is a "PyTest inspired" framework for running
    tests in the browser on both MicroPython and Pyodide.

    The automated (Playwright) tests are specified in the
    `tests/integration.spec.js` file.

## Documentation

* Documentation for PyScript (i.e. what you're reading right now), is found
  in a separate repository:
  [https://github.com/pyscript/docs](https://github.com/pyscript/docs)

* The project's homepage ([pyscript.net](https://pyscript.net/)) contains links
  and signposts for help and documentation. This is also found in a separate
  repository:
  [https://github.com/pyscript/pyscript.net](https://github.com/pyscript/pyscript.net)

## Release PyScript

This is the procedure for cutting a new release of PyScript. To follow it you
need the correct permissions on GitHub (you're a PyScript core maintainer /
admin).

The steps below must be done in order. Each phase depends on the GitHub release
created in the first phase already existing, so don't skip ahead.

Throughout, the version number for a release uses
[calver](https://calver.org/) in the form `YYYY.M.N` (year, month, and the
release number within that month). For example, the first release in June 2026
is `2026.6.1`. Wherever you see `2026.6.1` in the examples below, substitute the
actual calver of the release you are cutting.

### 1. Cut the GitHub release

* Navigate to the [GitHub page for PyScript releases](https://github.com/pyscript/pyscript/releases).
* Click the "Draft a new release" button, which will [take you here](https://github.com/pyscript/pyscript/releases/new),
  where you can fill in the details of the new release of PyScript.
    - Create a new tag. This should be the calver for the new release.
    - Set the target to `main`.
    - Set the release title to the calver for the new release (the same value
      as the new tag).
    - Write the release notes as a Markdown bulleted list of the changes, along
      with references to the related pull requests and the GitHub usernames of
      those who contributed.
    - Set the release label to "Latest".
* Once you're happy with the draft release, click the "Publish release" button.
  At this point the [prepare-release.yml](https://github.com/pyscript/pyscript/blob/main/.github/workflows/prepare-release.yml)
  and then the [publish-release.yml](https://github.com/pyscript/pyscript/blob/main/.github/workflows/publish-release.yml)
  GitHub actions will run, to generate the assets needed for the release.
  You'll be able to [observe this process here](https://github.com/pyscript/pyscript/actions).

**Verify:** there should be two outcomes.

1. A new latest release listed on GitHub, containing the description and
   related assets. For example: [https://github.com/pyscript/pyscript/releases/tag/2026.6.1](https://github.com/pyscript/pyscript/releases/tag/2026.6.1).
2. A page describing the release at `pyscript.net/releases/<CALVER>`. For
   example: [https://pyscript.net/releases/2026.7.1/](https://pyscript.net/releases/2026.7.1/).

You're not done yet. Now the release exists in GitHub, further changes to
related repositories need to be made.

### 2. Update the docs

Each release of PyScript has its own version of the docs. The generation of the
docs is handled automatically by GitHub actions. Inside the
[documentation repository](https://github.com/pyscript/docs), the process is:

* Create a new branch whose name is that of the new calver release (but use `-`
  instead of `.` between the numbers, e.g. `2026-6-1`).
* Update the [`version.json`](https://github.com/pyscript/docs/blob/main/version.json)
  file to the new calver.
* Run `node version-update.js`. This will automatically update all the
  references to the old calver to the new calver. It also downloads the new
  version's Python API and auto-builds the API docs.
* If you have outstanding PRs for updates to the documentation, merge or resolve
  them into this branch at this moment in time via `git fetch origin docs-pr-branch-name` followed by `git merge origin/docs-pr-branch-name`
* Once you're happy with the state of the documentation for this new version,
  create a PR for your branch in GitHub.
* Once the PR is approved and merged, a GitHub action based on
  [`update_docs.yml`](https://github.com/pyscript/docs/blob/main/.github/workflows/update_docs.yml)
  will run to generate the new version of the documentation in the `gh-pages`
  branch.

**Verify:** once the `gh-pages` branch is updated, GitHub's own automatic
deployment action will kick in, making the new version of the documentation
live. You'll be able to [observe this process here](https://github.com/pyscript/docs/actions).
Check the updated docs at
[docs.pyscript.net](https://docs.pyscript.net) (and remember to clear your
browser cache).

### 3. Update the homepage

Update two files in the
[homepage repository](https://github.com/pyscript/pyscript.net) to use the
latest calver:

1. In [`index.html`](https://github.com/pyscript/pyscript.net/blob/main/index.html),
   update ALL references to the old calver with the new version's calver. This
   includes the `<link>` and `<script>` tags in the `<head>` of the document,
   along with the content of the `<span class="subhead">` tag in the `<header>`
   tag in the `<body>` of the document.
2. Update the [`version.json`](https://github.com/pyscript/pyscript.net/blob/main/version.json)
   file to a JSON string containing the new calver.

Bundle these changes into a single PRi (named in the same way as the PR for
PyScript's docs), to be reviewed and approved by someone
else.
[This pull request](https://github.com/pyscript/pyscript.net/pull/104/changes)
is a good historical example of the changes described above.

**Verify**: Once your PR is reviewed and merged GitHub automatically deploys
the changes.
[Observe this process here](https://github.com/pyscript/pyscript.net/actions).
Once deployed, check your changes at [pyscript.net](https://pyscript.net)
(you may need to clear your browser cache).

### 4. Update the README

Update the opening HTML example in
[PyScript's README](https://github.com/pyscript/pyscript/blob/main/README.md)
to reference the new latest version.

### 5. Announce the release

**Verify first:** visit the new release's page on pyscript.net (for example,
[https://pyscript.net/releases/2026.7.1/](https://pyscript.net/releases/2026.7.1/))
and ensure the "Home", "Docs", "Code" and "Changes" links all point to the
pages and assets you've just updated.

Now all the pieces are in place, visit the
[`#announcements`](https://discord.com/channels/972017612454232116/1028271951082442832)
channel on the PyScript Discord server, and post a message along the lines of:

> @here we have a new release of PyScript! All the details can be found here:
> https://pyscript.net/releases/2026.7.1/ As always, feedback welcome. 🎉

Remember to substitute the actual new calver, not the `2026.6.1` used in these
examples.

## Contributing

* We have [suggestions for how to contribute to PyScript](contributing.md). Take
  a read and dive in.

* Please make sure you discuss potential contributions *before* you put in
  work. We don#t want folks to waste their time or re-invent the wheel.

* Technical discussions happen [on our discord server](https://discord.gg/HxvBtukrg2)
  and in the
  [discussions section](https://github.com/pyscript/pyscript/discussions) of
  our GitHub repository.

* Every two weeks on a Tuesday is a [technical community video call](https://discord.com/events/972017612454232116/1227274094366556279),
  the details of which are posted onto
  the discord server. Face to face technical discussions happen here.

* On the first Thursday of every month is a
  [PyScript FUN call](https://discord.com/events/972017612454232116/1227275336115556402),
  the details of which
  are also posted to discord. Project show-and-tells, cool hacks, new features
  and a generally humorous and creative time is had by all.
