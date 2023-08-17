from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('search', views.search, name='search'),
    path('new-page', views.new_page, name='new page'),
    path('wiki/<str:entry>', views.entry, name='title'),
    path('edit-page/<str:entry>', views.edit_page, name='edit page')
]
