from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Import models so they are registered on the Base metadata
# Models are kept in app.models package
try:
    from app import models  # noqa: F401
except Exception:
    # During some tooling or test runs models may not be importable; ignore failures here
    models = None
