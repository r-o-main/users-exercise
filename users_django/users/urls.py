from django.urls import include, path
from rest_framework import routers
from . import views


# The DefaultRouter class includes a default API root view, returning a response
# containing hyperlinks to all the list views.
router = routers.DefaultRouter()
router.trailing_slash = '/?'
router.register(r'users', views.UserViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('api/v1/', include((router.urls, 'users'), namespace='v1')),
]
