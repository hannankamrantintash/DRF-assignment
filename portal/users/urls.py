from rest_framework import routers
from django.conf.urls import url, include
from users.views import UserView, PostView

router = routers.DefaultRouter()
router.register(r'profile', UserView, base_name='users')
router.register(r'post', PostView, base_name='post')

urlpatterns = [
    url(r'^api/', include(router.urls)),
]
