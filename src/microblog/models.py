from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from .extensions import db
from .utils import generate_unique_slug, safe_commit


class User(db.Model, UserMixin):
    """
    User model for authentication and ownership of posts.
    Implements all required fields and methods for Flask-Login integration.
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    phone = db.Column(db.String(20), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship with posts (CASCADE delete)
    posts = db.relationship("Post", backref="author", cascade="all, delete-orphan", lazy=True)

    def set_password(self, password: str) -> None:
        """
        Hash the user's password using PBKDF2.
        Uses Werkzeug's generate_password_hash for secure password storage.
        """
        self.password_hash = generate_password_hash(password, method="pbkdf2:sha256")

    def check_password(self, password: str) -> bool:
        """
        Verify a user's password against the stored hash.
        Uses Werkzeug's check_password_hash for secure password verification.
        """
        return check_password_hash(self.password_hash, password)

    def save(self) -> None:
        """Persist user to database with error handling."""
        db.session.add(self)
        safe_commit()

    @staticmethod
    def get_by_id(user_id: int):
        """Get user by ID - required by Flask-Login."""
        return User.query.get(user_id)

    @staticmethod
    def get_by_email(email: str):
        """Get user by email address."""
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_by_username(username: str):
        """Get user by username."""
        return User.query.filter_by(username=username).first()

    def __repr__(self):
        return f'<User {self.username}>'


class Post(db.Model):
    """
    Primary entity model: a blog post owned by a User.
    Implements all required fields and methods for CRUD operations.
    """

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    slug = db.Column(db.String(255), unique=True, nullable=False, index=True)
    excerpt = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(100), nullable=True)
    is_published = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def save(self):
        """
        Save a post with automatic slug generation and collision handling.
        Uses python-slugify for URL-friendly slugs.
        """
        if not self.slug:
            self.slug = generate_unique_slug(Post, self.title)
        
        db.session.add(self)
        try:
            safe_commit()
        except IntegrityError:
            # Handle slug collision by generating a new unique slug
            db.session.rollback()
            self.slug = generate_unique_slug(Post, self.title)
            db.session.add(self)
            safe_commit()

    def public_url(self):
        """Generate public URL for viewing this post."""
        return f"/post/{self.slug}/"

    @staticmethod
    def get_by_slug(slug: str):
        """Get post by slug - required for detail views."""
        return Post.query.filter_by(slug=slug, is_published=True).first()

    @staticmethod
    def get_all():
        """Get all published posts ordered by creation date."""
        return Post.query.filter_by(is_published=True).order_by(Post.created_at.desc()).all()

    @staticmethod
    def get_by_user(user_id: int):
        """Get all posts by a specific user."""
        return Post.query.filter_by(user_id=user_id, is_published=True).order_by(Post.created_at.desc()).all()

    @staticmethod
    def get_by_category(category: str):
        """Get posts by category."""
        return Post.query.filter_by(category=category, is_published=True).order_by(Post.created_at.desc()).all()

    def __repr__(self):
        return f'<Post {self.title}>'
