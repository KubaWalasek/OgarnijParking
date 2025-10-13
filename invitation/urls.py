from django.urls import path
from invitation.views import  CreateInvitationView

urlpatterns = [
    path('create_invitation/', CreateInvitationView.as_view(), name='create_invitation'),
]



