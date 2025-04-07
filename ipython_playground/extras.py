# ruff: noqa: F401
# isort: off


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

    return modules


# TODO wrap in function, add to globals
# treat the entire ipython session as a with block :)
engine = create_engine(database_url(), echo=True)
session = SessionManager.get_instance().get_session().__enter__()
_session_context.set(session)

# Import modules for ipython
imported_modules = load_modules_for_ipython()
globals().update(imported_modules)


import funcy_pipe as fp
import sqlalchemy as sa

from activemodel.utils import find_all_sqlmodels

# from activemodel import SessionManager
