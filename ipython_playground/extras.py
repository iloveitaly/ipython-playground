# ruff: noqa: F401
# isort: off

import inspect
import pkgutil
from types import ModuleType
from .utils import log
import sys


def load_modules_for_ipython():
    """Load list of common modules for use in ipython sessions and return them as a dict so they can be appended to the global namespace"""

    modules = {}
    try:
        import app.models

        modules["models"] = app.models
    except ImportError:
        log.warning("Could not import app.models")

    try:
        import app.commands

        modules["commands"] = app.commands
    except ImportError:
        log.warning("Could not import app.commands")

    try:
        import funcy_pipe as fp

        modules["fp"] = fp
    except ImportError:
        log.warning("Could not import funcy_pipe")

    try:
        import sqlalchemy as sa

        modules["sa"] = sa
    except ImportError:
        log.warning("Could not import sqlalchemy")

    return modules


def find_all_sqlmodels(module: ModuleType):
    """Import all model classes from module and submodules into current namespace."""

    try:
        from sqlmodel import SQLModel
    except ImportError:
        log.warning("Could not find SQLModel, skipping model discovery")
        return {}

    log.debug(f"Starting model import from module: {module.__name__}")
    model_classes = {}

    # Walk through all submodules
    for loader, module_name, is_pkg in pkgutil.walk_packages(module.__path__):
        full_name = f"{module.__name__}.{module_name}"
        log.debug(f"Importing submodule: {full_name}")

        # Check if module is already imported
        if full_name in sys.modules:
            submodule = sys.modules[full_name]
        else:
            log.warning(f"Module not found in sys.modules, not importing: {full_name}")
            continue

        # Get all classes from module
        for name, obj in inspect.getmembers(submodule):
            if inspect.isclass(obj) and issubclass(obj, SQLModel) and obj != SQLModel:
                log.debug(f"Found model class: {name}")
                model_classes[name] = obj

    log.debug(f"Completed model import. Found {len(model_classes)} models")
    return model_classes


def setup_database_session(database_url):
    """Set up the SQLAlchemy engine and session, return helpful globals"""
    from activemodel import SessionManager
    from sqlalchemy import create_engine
    from activemodel.session_manager import _session_context
    from activemodel.utils import compile_sql

    def sa_run(stmt):
        result = session.execute(stmt).all()
        return result

    def sa_sql(stmt):
        return compile_sql(stmt)

    engine = create_engine(database_url, echo=True)
    session = SessionManager.get_instance().get_session().__enter__()
    _session_context.set(session)

    return {"engine": engine, "session": session, "sa_sql": sa_sql, "sa_run": sa_run}


def all(*, database_url: str | None = None):
    modules = load_modules_for_ipython()

    if "models" in modules:
        modules = modules | find_all_sqlmodels(modules["models"])

    if not database_url:
        try:
            from app.configuration.database import (
                database_url as database_url_generator,
            )

            database_url = database_url_generator()
        except ImportError:
            database_url = None

    if database_url:
        modules = modules | setup_database_session(database_url)

    return modules
