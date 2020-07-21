from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator


def csrf_protect_class(cls):
    for method in ('post', 'put', 'delete'):
        if hasattr(cls, method):
            cls = method_decorator(csrf_protect, method)(cls)
    return cls
