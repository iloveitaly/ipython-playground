import inspect
from typing import Any
from ipython_playground import _format_signature

class DefaultClass:
    """Class with default __init__ from object or Pydantic-like."""
    pass

class CustomInitClass:
    def __init__(self, a: int, b: str = "default"):
        self.a = a
        self.b = b

class StarArgsClass:
    def __init__(self, *args, **kwargs):
        pass

class PositionalOnlyStarArgsClass:
    def __init__(self, /, *args, **kwargs):
        pass

def test_format_signature_classes():
    # Note: inspect.signature(Class.__init__) includes 'self'
    assert _format_signature(CustomInitClass) == "(self, a: int, b: str = 'default')"
    
    # These are the ones we want to omit
    assert _format_signature(StarArgsClass) == ""
    assert _format_signature(PositionalOnlyStarArgsClass) == ""

def test_format_signature_functions():
    def simple_func(x, y=1):
        pass
    
    def variadic_func(*args, **kwargs):
        pass

    # Functions don't have 'self' in signature (unless they are bound methods, but here they are plain functions)
    assert _format_signature(simple_func) == "(x, y=1)"
    assert _format_signature(variadic_func) == "(*args, **kwargs)"

def test_format_signature_builtin():
    # Builtins might raise TypeError in inspect.signature, which we handle by returning ""
    sig = _format_signature(int)
    assert sig == "" or sig.startswith("(")
