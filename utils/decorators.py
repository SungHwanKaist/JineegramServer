from functools import wraps
from urllib.parse import urlparse

from django.contrib.auth.decorators import login_required as django_login_required
from django.contrib.auth.views import redirect_to_login
from django.core.handlers.wsgi import WSGIRequest


def login_required(view_func):
    @wraps(view_func)
    def decorator(*args, **kwargs):
        if args:
            request = args[0]
           
            if isinstance(request, WSGIRequest) and request.method == 'POST':
                user = getattr(request, 'user')
                if user and user.is_authenticated:
                    return view_func(*args, **kwargs)
                path = urlparse(request.META['HTTP_REFERER']).path
                return redirect_to_login(path)
        return django_login_required(view_func)(*args, **kwargs)
    return decorator