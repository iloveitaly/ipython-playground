import inspect
import logging
import os
from pathlib import Path
from typing import get_type_hints

from rich.console import Console
from rich.text import Text

from ipython_playground.create import create_playground_file

logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "INFO").upper(),
)

logger = logging.getLogger(__name__)


def inspect_environment():
    """Display relevant custom functions and variables with minimal formatting"""

    console = Console()
    width = console.width
    current_module = inspect.currentframe().f_globals
    ipython_path = Path.home() / ".ipython"
    builtin_modules = {
        "os",
        "sys",
        "json",
        "tempfile",
        "subprocess",
        "importlib",
        "pkgutil",
    }
    ipy_modules = {"IPython", "ipykernel"}
    exclude_vars = {"In", "Out", "PIPE", "get_ipython", "exit", "quit", "c"}

    def truncate_text(text: str, max_width: int) -> str:
        if len(text) > max_width:
            return text[: max_width - 3] + "..."
        return text

    def get_module_info(module) -> str:
        module_path = getattr(module, "__path__", [""])[0]
        version = getattr(module, "__version__", "unknown version")
        return f"{module.__name__} ({version}) from {module_path}"

    # Functions Section
    console.print("\n[bold blue]Custom Functions[/bold blue]")
    console.print("─" * width)

    for name, obj in current_module.items():
        if (
            inspect.isfunction(obj)
            and not name.startswith("_")
            and obj.__module__ == "__main__"
        ):
            # Get the source file of the function
            try:
                source_file = Path(inspect.getfile(obj))
                # Skip if function is from .ipython directory
                if ipython_path in source_file.parents:
                    continue
            except (TypeError, ValueError):
                continue

            sig = str(inspect.signature(obj))
            return_type = get_type_hints(obj).get("return", None)
            if return_type:
                sig += f" -> {return_type.__name__}"
            text = Text()
            text.append(f"{name:<30}", style="cyan bold")
            text.append(truncate_text(sig, width - 30), style="green")
            console.print(text)

    # Classes Section
    console.print("\n[bold blue]Classes[/bold blue]")
    console.print("─" * width)

    for name, obj in current_module.items():
        if inspect.isclass(obj) and not name.startswith("_"):
            try:
                sig = str(inspect.signature(obj.__init__))
            except (TypeError, ValueError):
                sig = "()"
            text = Text()
            text.append(f"{name:<30}", style="cyan bold")
            text.append(truncate_text(sig, width - 30), style="green")
            console.print(text)

    # Modules Section
    console.print("\n[bold blue]Imported Modules[/bold blue]")
    console.print("─" * width)

    for name, obj in current_module.items():
        if (
            inspect.ismodule(obj)
            and not name.startswith("_")
            and name not in builtin_modules
            and name not in exclude_vars
        ):
            text = Text()
            text.append(f"{name:<30}", style="cyan bold")
            text.append(truncate_text(get_module_info(obj), width - 30), style="yellow")
            console.print(text)

    # Variables Section
    console.print("\n[bold blue]Variables[/bold blue]")
    console.print("─" * width)

    for name, obj in current_module.items():
        if (
            not inspect.isfunction(obj)
            and not inspect.ismodule(obj)
            and not inspect.isclass(obj)
            and not name.startswith("_")
            and name not in builtin_modules
            and name not in exclude_vars
        ):
            type_info = type(obj).__name__
            if hasattr(obj, "__annotations__"):
                annotations = getattr(obj, "__annotations__", {})
                if annotations:
                    type_info += f" [{', '.join(str(v) for v in annotations.values())}]"
            text = Text()
            text.append(f"{name:<30}", style="cyan bold")
            text.append(truncate_text(type_info, width - 30), style="green")
            console.print(text)


def main():
    create_playground_file()
