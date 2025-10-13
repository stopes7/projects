from django.urls import path
from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("search/", views.SearchResultsView.as_view(), name="search_results"),
    path("add-location/", views.AddLocationView.as_view(), name="add_location"),
    path("delete-location/<int:pk>/", views.DeleteLocationView.as_view(), name="delete_location"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
]
