from django.conf.urls.static import static
from django.urls import path

from scrumboard import views
from scrumboard.api import CardViewSet, ListViewSet
from rest_framework.routers import DefaultRouter
from django.conf import settings

"""
DefaultRouter class allows automatic routing of
ALL URLS for all operations on object from DB
ViewSet is mapped with Router below code.
Finally, urlpatterns gets populated
"""

router = DefaultRouter()  # instead of urlpatterns list
router.register(r'lists', ListViewSet)
router.register(r'cards', CardViewSet)

# calling a bad URL show a lot of URLS created automatically
urlpatterns = [
    path('register/', views.registerView, name="register"),
    path('login/', views.loginView, name="login"),
    path('logout/', views.logoutView, name="logout"),
    path('', views.home, name="home"),
    path('chat/', views.usersView, name="chat"),
    path("chat/<int:user_id>", views.userChat, name="userChat"),
    path("message/<int:user_id>", views.message, name="message")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += router.urls
print(urlpatterns)
