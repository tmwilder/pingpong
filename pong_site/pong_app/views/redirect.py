#Django imports.
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


@login_required
def redirectToUserProfile(request):
    return HttpResponseRedirect("/user_profile/{0}".format(User.objects.get(username__exact=request.user.username).id))


def redirectToHome(request):
    return HttpResponseRedirect("/")
