from django.http import HttpResponseRedirect
from functools import wraps
from django.utils.decorators import available_attrs
from django.contrib.auth.models import User


def user_passes_test_request(test_func):
    """Explanation of how this works...

    user_passes_test_request takes a testing function as input, and returns a function.
    When you use it to decorate:

    @user_passes_test_request(my_test)
    def my_view(request, etc)

    the inner decorator [having already evaluated the test_func] is what is being used to decorate!
    This decorator then takes the view function, uses wraps to ensure the namespace is correct.

    Within the wrapped function, if the test passes, the view is executed as is,
    otherwise, it redirects to the "unauthorized" page.

    """

    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request):
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseRedirect("/unauthorized")
        return _wrapped_view
    return decorator


def verify_user_id_in_url(request):
    return int(User.objects.get(username__exact=request.user.username).id) == int(request.path.split('/')[-1])
