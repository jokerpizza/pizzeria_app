
"""Find SessionLocal defined in your project."""
import importlib

def _find():
    candidates = [
        "backend.app.database",
        "app.database",
        "backend.database",
        "database",
        "app.db",
        "backend.app.db",
        "backend.app.models",
        "app.models",
        "backend.app.sales.models_sales",
    ]
    for name in candidates:
        try:
            mod = importlib.import_module(name)
        except ModuleNotFoundError:
            continue
        if hasattr(mod, "SessionLocal"):
            return getattr(mod, "SessionLocal")
    raise ImportError("SessionLocal not found; update sales/db_session.py candidates.")

SessionLocal = _find()
