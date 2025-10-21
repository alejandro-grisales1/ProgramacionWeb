from slugify import slugify
from sqlalchemy.exc import IntegrityError
from .extensions import db

def generate_unique_slug(model, value_field: str, slug_field: str = "slug") -> str:
    """Generate a unique slug for `model` using `value_field` attribute value."""
    base = slugify(value_field)[:200]
    slug = base
    counter = 1
    while True:
        exists = model.query.filter(getattr(model, slug_field) == slug).first()
        if not exists:
            return slug
        slug = f"{base}-{counter}"
        counter += 1

def safe_commit():
    """Commit the current DB session and handle IntegrityError gracefully."""
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise
