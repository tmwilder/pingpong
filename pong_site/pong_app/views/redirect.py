#Django
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

#Our app
from django.conf import settings

@login_required
def redirectToUserProfile(request):
    user_id = User.objects.get(username__exact=request.user.username).id
    return HttpResponseRedirect("/{0}/user_profile/{1}".format(settings.BASE_URL, user_id))


def redirectToHome(request):
    return HttpResponseRedirect("/{0}/".format(settings.BASE_URL))
