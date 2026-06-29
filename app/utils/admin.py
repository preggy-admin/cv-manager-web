"""
Admin utilities — decorators and helpers for admin-only access.
"""

from functools import wraps
from flask import abort
from flask_login import current_user, login_required


def admin_required(f):
    """Decorator that enforces login + admin role.
    Returns 403 Forbidden if the authenticated user is not an admin.
    """
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function
