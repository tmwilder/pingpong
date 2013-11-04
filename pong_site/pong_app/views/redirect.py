#Django
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


@login_required
def redirectToUserProfile(request):
    user_id = User.objects.get(username__exact=request.user.username).id
    kwargs = {'user_id': user_id}
    return HttpResponseRedirect(reverse('pong_app.views.profiles.user_profile', kwargs=kwargs))


def redirectToHome(request):
    if request.user.is_authenticated():
        return redirectToUserProfile(request)
    else:
        return HttpResponseRedirect(reverse('django.contrib.auth.views.login'))
