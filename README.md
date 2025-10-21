# Microblog - Comprehensive Flask Blog Application

A modern, full-featured blog application built with Flask and PostgreSQL, implementing all required technical specifications for a complete web application with user authentication, CRUD operations, and modern UI/UX.

## Project Description

Microblog is a comprehensive blog platform that allows users to create, share, and manage blog posts. The application solves the problem of content sharing and community building by providing a secure, user-friendly platform where individuals can express their thoughts, share experiences, and connect with others through written content.

### Domain Choice: Blog/Content Management System

I chose to implement a blog platform because it perfectly demonstrates all the required technical features:

- **User Management**: Each user can create and manage their own posts
- **Content Creation**: Rich text posts with categories and excerpts
- **Social Features**: Users can view posts by author and category
- **Security**: Proper authentication and authorization
- **SEO-Friendly**: URL slugs for better search engine optimization

## Features Implemented

### Core Functionality

- **User Authentication**: Secure registration and login with password hashing
- **Post Management**: Create, read, update, and delete blog posts
- **Content Organization**: Categories, excerpts, and publication status
- **User Profiles**: Individual user pages with post history
- **Category Filtering**: Browse posts by category
- **Responsive Design**: Modern, mobile-friendly interface
- **Security**: CSRF protection, secure redirects, input validation

### Advanced Features

- **Slug Generation**: SEO-friendly URLs using python-slugify
- **Email Validation**: Comprehensive email validation using email-validator
- **Flash Messages**: User feedback with styled notifications
- **Error Handling**: Custom 404, 403, and 500 error pages
- **Admin Features**: Admin users have additional privileges
- **Remember Me**: Persistent login sessions

## Tech Stack

### Backend Technologies

- **Python**: 3.12+ (Modern Python features and performance)
- **Flask**: 3.1.2+ (Web framework)
- **Flask-WTF**: 1.2.2+ (Form handling and CSRF protection)
- **Flask-Login**: 0.6.3+ (User session management)
- **Flask-SQLAlchemy**: 3.1.1+ (Database ORM)
- **PostgreSQL**: Database engine
- **psycopg**: 3.2.11+ (PostgreSQL adapter)

### Frontend Technologies

- **Jinja2**: Template engine
- **CSS3**: Modern styling with CSS Grid and Flexbox
- **Font Awesome**: Icon library
- **Responsive Design**: Mobile-first approach

### Development Tools

- **python-slugify**: 8.0.4+ (URL-friendly slug generation)
- **email-validator**: 2.3.0+ (Email validation)
- **Werkzeug**: Password hashing and security utilities

## Installation Instructions

### Prerequisites

- Python 3.12 or higher
- PostgreSQL 12 or higher
- Git (for version control)

### 1. Clone the Repository

```bash
git clone <repository-url>
cd microblog
```

### 2. Set Up Virtual Environment

```bash
# Using venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Or using Rye
rye sync
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Database Configuration

#### Create PostgreSQL Database

```sql
-- Connect to PostgreSQL as superuser
CREATE DATABASE microblog;
CREATE USER microblog_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE microblog TO microblog_user;
```

#### Set Environment Variables

```bash
export DATABASE_URL='postgresql+psycopg://microblog_user:your_secure_password@localhost:5432/microblog'
export SECRET_KEY='your-super-secret-key-here-make-it-long-and-random'
export ALLOWED_HOSTS='localhost,127.0.0.1'
```

### 5. Initialize Database

```bash
python -m src.microblog.run
# The application will automatically create all required tables
```

### 6. Run the Application

```bash
python -m src.microblog.run
```

The application will be available at `http://localhost:5000`

## Available Routes

### Public Routes (No Authentication Required)

- **`/`** - Homepage with recent posts
- **`/post/<slug>/`** - Individual post detail view
- **`/login`** - User login form
- **`/signup/`** - User registration form
- **`/logout`** - User logout (redirects to home)
- **`/user/<username>/`** - User profile with their posts
- **`/category/<category>/`** - Posts filtered by category

### Protected Routes (Authentication Required)

- **`/admin/post/`** - Create new post
- **`/admin/post/<id>/edit/`** - Edit existing post
- **`/admin/post/<id>/delete/`** - Delete post (POST method)

### Error Pages

- **`/404`** - Page not found
- **`/403`** - Access forbidden
- **`/500`** - Internal server error

## Data Models

### User Model

```python
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    phone = db.Column(db.String(20), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

**Required Methods:**

- `set_password(password)` - Hash and store password
- `check_password(password)` - Verify password
- `save()` - Persist to database
- `get_by_id(id)` - Static method to get user by ID
- `get_by_email(email)` - Static method to get user by email

### Post Model

```python
class Post(db.Model):
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
```

**Required Methods:**

- `save()` - Persist with automatic slug generation
- `public_url()` - Generate public URL
- `get_by_slug(slug)` - Static method to get post by slug
- `get_all()` - Static method to get all published posts

## Forms Implementation

### SignupForm

- Username validation (3-80 characters)
- Email validation with email-validator library
- Password validation (6-128 characters)
- CSRF protection

### LoginForm

- Email and password validation
- Remember me functionality
- Secure redirect handling

### PostForm

- Title validation (3-255 characters)
- Content validation (minimum 10 characters)
- Optional excerpt (maximum 500 characters)
- Category selection
- CSRF protection

## Security Features

### Authentication & Authorization

- **Password Hashing**: Using Werkzeug's PBKDF2 with SHA256
- **Session Management**: Flask-Login integration
- **Protected Routes**: @login_required decorator
- **User Ownership**: Users can only edit/delete their own posts

### Security Measures

- **CSRF Protection**: Enabled via Flask-WTF
- **Secure Redirects**: URL validation using urlparse
- **Input Validation**: Comprehensive form validation
- **SQL Injection Prevention**: SQLAlchemy ORM protection
- **XSS Prevention**: Template auto-escaping

## Project Structure

```
microblog/
├── pyproject.toml              # Project configuration and dependencies
├── README.md                   # This documentation
├── requirements.txt           # Python dependencies
└── src/
    └── microblog/            # Main application package
        ├── run.py            # Application factory and routes
        ├── models.py         # Database models (User, Post)
        ├── forms.py          # WTForms definitions
        ├── config.py         # Configuration settings
        ├── extensions.py     # Flask extensions initialization
        ├── utils.py          # Utility functions
        ├── static/
        │   └── css/
        │       └── styles.css # Modern CSS styling
        └── templates/
            ├── base_template.html    # Base template with navigation
            ├── index.html           # Homepage template
            ├── post_view.html       # Post detail template
            ├── login_form.html      # Login form template
            ├── 404.html            # Not found error page
            ├── 403.html            # Forbidden error page
            ├── 500.html            # Server error page
            ├── user_posts.html     # User profile template
            ├── category_posts.html # Category listing template
            └── admin/
                ├── signup_form.html    # Registration form
                ├── post_form.html      # Post creation form
                └── edit_post_form.html # Post editing form
```

## Development Features

### Code Quality

- **Type Hints**: Comprehensive type annotations
- **Docstrings**: Detailed function and class documentation
- **Error Handling**: Graceful error handling with custom pages
- **Code Organization**: Modular structure with separation of concerns

### User Experience

- **Responsive Design**: Works on all device sizes
- **Modern UI**: Clean, professional interface
- **Intuitive Navigation**: Easy-to-use navigation system
- **Flash Messages**: Clear user feedback
- **Loading States**: Smooth user interactions

## Deployment Considerations

### Production Setup

1. **Environment Variables**: Set secure SECRET_KEY and DATABASE_URL
2. **Database Migrations**: Use Alembic for production database changes
3. **Static Files**: Configure proper static file serving
4. **HTTPS**: Enable SSL/TLS encryption
5. **Security Headers**: Implement security headers

### Performance Optimization

- **Database Indexing**: Optimized queries with proper indexes
- **Caching**: Consider Redis for session storage
- **CDN**: Use CDN for static assets
- **Database Connection Pooling**: Configure connection pooling

## Testing

### Manual Testing Checklist

- [ ] User registration and login
- [ ] Post creation, editing, and deletion
- [ ] Category filtering
- [ ] User profile pages
- [ ] Error page handling
- [ ] Mobile responsiveness
- [ ] Form validation
- [ ] Security features

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions or issues, please open an issue in the repository or contact the development team.

---

**Built with ❤️ using Flask, PostgreSQL, and modern web technologies.**
