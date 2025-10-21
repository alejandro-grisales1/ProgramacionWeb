from flask import Flask, render_template, redirect, url_for, request, flash, abort, jsonify
from urllib.parse import urlparse
from .config import Config, is_safe_url
from .extensions import db, login_manager
from .models import User, Post
from .forms import SignupForm, LoginForm, PostForm, EditPostForm
from flask_login import login_user, logout_user, current_user, login_required

def create_app(config_class=Config):
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "login"

    @login_manager.user_loader
    def load_user(user_id: str):
        return User.get_by_id(int(user_id))

    @app.route("/")
    def index():
        posts = Post.get_all()
        return render_template("index.html", posts=posts)

    @app.route("/post/<slug>/")
    def post_detail(slug: str):
        post = Post.get_by_slug(slug)
        if not post:
            abort(404)
        return render_template("post_view.html", post=post)

    @app.route("/signup/", methods=["GET", "POST"])
    def signup():
        """User registration with email uniqueness validation."""
        if current_user.is_authenticated:
            return redirect(url_for("index"))
        
        form = SignupForm()
        if form.validate_on_submit():
            # Check if email already exists
            if User.get_by_email(form.email.data):
                form.email.errors.append("Email already registered")
            # Check if username already exists
            elif User.get_by_username(form.username.data):
                form.username.errors.append("Username already taken")
            else:
                user = User(username=form.username.data, email=form.email.data)
                user.set_password(form.password.data)
                user.save()
                login_user(user)
                flash("¡Cuenta creada e iniciada sesión exitosamente!", "success")
                return redirect(url_for("index"))
        
        return render_template("admin/signup_form.html", form=form)

    @app.route("/login", methods=["GET", "POST"])
    def login():
        """User login with secure redirect handling."""
        if current_user.is_authenticated:
            return redirect(url_for("index"))
        
        form = LoginForm()
        if form.validate_on_submit():
            user = User.get_by_email(form.email.data)
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                flash("¡Sesión iniciada exitosamente!", "success")
                
                # Handle secure redirect with next parameter
                next_page = request.args.get("next")
                if next_page and is_safe_url(next_page, request.host_url):
                    return redirect(next_page)
                return redirect(url_for("index"))
            else:
                form.password.errors.append("Invalid email or password")
        
        return render_template("login_form.html", form=form)

    @app.route("/logout")
    def logout():
        """User logout with flash message."""
        logout_user()
        flash("Has cerrado sesión exitosamente.", "info")
        return redirect(url_for("index"))

    @app.route("/admin/post/", methods=["GET", "POST"])
    @login_required
    def create_post():
        """Create new post - protected route requiring authentication."""
        form = PostForm()
        if form.validate_on_submit():
            post = Post(
                user_id=current_user.id,
                title=form.title.data,
                content=form.content.data,
                excerpt=form.excerpt.data,
                category=form.category.data if form.category.data else None,
                slug=""
            )
            post.save()
            flash("¡Post creado exitosamente!", "success")
            return redirect(url_for("post_detail", slug=post.slug))
        
        return render_template("admin/post_form.html", form=form)

    @app.route("/admin/post/<int:post_id>/edit/", methods=["GET", "POST"])
    @login_required
    def edit_post(post_id):
        """Edit existing post - only by post author."""
        post = Post.query.get_or_404(post_id)
        
        # Check if user owns the post
        if post.user_id != current_user.id and not current_user.is_admin:
            abort(403)
        
        form = EditPostForm(obj=post)
        if form.validate_on_submit():
            post.title = form.title.data
            post.content = form.content.data
            post.excerpt = form.excerpt.data
            post.category = form.category.data if form.category.data else None
            post.is_published = form.is_published.data
            post.save()
            flash("¡Post actualizado exitosamente!", "success")
            return redirect(url_for("post_detail", slug=post.slug))
        
        return render_template("admin/edit_post_form.html", form=form, post=post)

    @app.route("/admin/post/<int:post_id>/delete/", methods=["POST"])
    @login_required
    def delete_post(post_id):
        """Delete post - only by post author or admin."""
        post = Post.query.get_or_404(post_id)
        
        # Check if user owns the post or is admin
        if post.user_id != current_user.id and not current_user.is_admin:
            abort(403)
        
        db.session.delete(post)
        db.session.commit()
        flash("¡Post eliminado exitosamente!", "success")
        return redirect(url_for("index"))

    @app.route("/user/<username>/")
    def user_posts(username):
        """Display posts by a specific user."""
        user = User.get_by_username(username)
        if not user:
            abort(404)
        
        posts = Post.get_by_user(user.id)
        return render_template("user_posts.html", user=user, posts=posts)

    @app.route("/category/<category>/")
    def category_posts(category):
        """Display posts by category."""
        posts = Post.get_by_category(category)
        return render_template("category_posts.html", category=category, posts=posts)

    @app.errorhandler(404)
    def page_not_found(e):
        """Handle 404 errors."""
        return render_template("404.html"), 404

    @app.errorhandler(403)
    def forbidden(e):
        """Handle 403 Forbidden errors."""
        return render_template("403.html"), 403

    @app.errorhandler(500)
    def internal_error(e):
        """Handle 500 Internal Server errors."""
        db.session.rollback()
        return render_template("500.html"), 500

    return app

if __name__ == "__main__":
    app = create_app()
    # For development only: create tables if they don't exist (use migrations in production)
    with app.app_context():
        db.create_all()
    app.run(debug=True)
