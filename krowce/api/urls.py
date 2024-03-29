from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'teams', views.TeamViewSet)
router.register(r'sessions', views.SessionViewSet)
router.register(r'items', views.ItemViewSet)
router.register(r'scores', views.ScoreViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.login),
    path('signup/', views.signup),
    path('join-session/', views.join_session),
    path('finish-combo/', views.add_item_sentence_and_score),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

urlpatterns += router.urls
