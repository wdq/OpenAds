from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from advertisements.models import Provider


def superuser_or_provider(function):
    def authenticate_and_continue(*args, **kwargs):
        request = args[0]
        if request.user.is_superuser:
            return function(*args, **kwargs)
        if hasattr(request.user, 'provider'):
            return function(*args, **kwargs)
        return HttpResponseRedirect(reverse('accounts:logout'))
    return authenticate_and_continue


def provider_access(function):
    def wrapper(*args, **kwargs):
        request = args[0]
        if request.user.is_superuser:
            return function(*args, **kwargs)
        if hasattr(request.user, 'provider'):
            provider = Provider.objects.get(pk=kwargs["provider_pk"])
            if provider == request.user.provider:
                return function(*args, **kwargs)
            else:
                raise Http404
        return HttpResponseRedirect(reverse('accounts:logout'))
    return wrapper
