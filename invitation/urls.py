from django.urls import path

from invitation import views

app_name = "invitation"

urlpatterns = [
    path("", views.InvitationView.as_view()),
    #path("<str:pk>", views.InvitationIdView.as_view())
]
