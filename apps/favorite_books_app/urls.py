from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.registration),
    url(r'^authenticate$', views.auth_user),
    url(r'^books$', views.user_logged),
    url(r'^add_book$', views.add_book),
    url(r'^books/(?P<book_id>\d+)$', views.display_info),
    url(r'^books/edit_description/(?P<book_id>\d+)$', views.edit_description),
    url(r'^add_to_favorites/(?P<book_id>\d+)$', views.add_to_favorites),
    url(r'^delete/(?P<book_id>\d+)$', views.delete_book),
    url(r'^clear_session$', views.clear_session),
]