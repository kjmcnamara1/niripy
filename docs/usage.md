# Usage

Quick start and examples.

## Install

Install from [PyPI](https://pypi.org/project/niripy/):

=== "UV"

    <!-- termynal -->
    ```sh
    $ uv add niripy
    Using CPython 3.13.11
    Creating virtual environment at: .venv
    Resolved 7 packages in 271ms
    Installed 6 packages in 15ms
    + annotated-types==0.7.0
    + niripy==0.2.7
    + pydantic==2.12.5
    + pydantic-core==2.41.5
    + typing-extensions==4.15.0
    + typing-inspection==0.4.2
    ```

=== "Poetry"

    <!-- termynal -->
    ```sh
    $ poetry add niripy
    Creating virtualenv test-poetry in /home/kjm/Code/test_poetry/.venv
    Using version ^0.2.7 for niripy

    Updating dependencies
    Resolving dependencies... (1.1s)

    Package operations: 6 installs, 0 updates, 0 removals

    - Installing typing-extensions (4.15.0)
    - Installing annotated-types (0.7.0)
    - Installing pydantic-core (2.41.5)
    - Installing typing-inspection (0.4.2)
    - Installing pydantic (2.12.5)
    - Installing niripy (0.2.7)

    Writing lock file
    ```

=== "Pip"

    <!-- termynal {prompt_literal_start: ["$ ", "(.venv) $ "] } -->
    ```sh
    $ python -m venv .venv
    $ source .venv/bin/activate
    (.venv) $ pip install niripy
    Collecting niripy
    Using cached niripy-0.2.7-py3-none-any.whl.metadata (2.8 kB)
    Collecting pydantic>=2.12.4 (from niripy)
    Using cached pydantic-2.12.5-py3-none-any.whl.metadata (90 kB)
    Collecting annotated-types>=0.6.0 (from pydantic>=2.12.4->niripy)
    Using cached annotated_types-0.7.0-py3-none-any.whl.metadata (15 kB)
    Collecting pydantic-core==2.41.5 (from pydantic>=2.12.4->niripy)
    Using cached pydantic_core-2.41.5-cp314-cp314-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (7.3 kB)
    Collecting typing-extensions>=4.14.1 (from pydantic>=2.12.4->niripy)
    Using cached typing_extensions-4.15.0-py3-none-any.whl.metadata (3.3 kB)
    Collecting typing-inspection>=0.4.2 (from pydantic>=2.12.4->niripy)
    Using cached typing_inspection-0.4.2-py3-none-any.whl.metadata (2.6 kB)
    Using cached niripy-0.2.7-py3-none-any.whl (15 kB)
    Using cached pydantic-2.12.5-py3-none-any.whl (463 kB)
    Using cached pydantic_core-2.41.5-cp314-cp314-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (2.1 MB)
    Using cached annotated_types-0.7.0-py3-none-any.whl (13 kB)
    Using cached typing_extensions-4.15.0-py3-none-any.whl (44 kB)
    Using cached typing_inspection-0.4.2-py3-none-any.whl (14 kB)
    Installing collected packages: typing-extensions, annotated-types, typing-inspection, pydantic-core, pydantic, niripy
    Successfully installed annotated-types-0.7.0 niripy-0.2.7 pydantic-2.12.5 pydantic-core-2.41.5 typing-extensions-4.15.0 typing-inspection-0.4.2

    [notice] A new release of pip is available: 25.3 -> 26.0.1
    [notice] To update, run: pip install --upgrade pip
    ```

Or the [AUR](https://aur.archlinux.org/packages/python-niripy):

=== "Yay"

    <!-- termynal -->
    ```sh
    $ yay -S python-niripy
    ```

=== "Paru"

    <!-- termynal -->
    ```sh
    $ paru -S python-niripy
    ```

Or use Nix with the provided flake:

<!-- termynal -->

```sh
$ nix develop github:kjmcnamara1/niripy
---> 100%
Niripy development environment loaded
```

## Examples

[Instance][niripy.Instance] is the main class for interacting with Niri. It
attaches to the Niri socket and provides methods for querying and controlling
Niri.

The models returned (e.g. [Windows][niripy.models.Window],
[Outputs][niripy.models.Output], [Workspaces][niripy.models.Workspace]) are all
pydantic models!

```py linenums="1" title="example.py"
from niripy.instances import Instance

niri = Instance()

print(niri.version)

for window in niri.get_windows():
    print(window.title)
    print(window.model_dump_json(indent=2))
```
