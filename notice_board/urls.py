from django.urls import path
from notice_board.views import addAnnouncement, AnnouncementListView, AnnouncementDetailView

urlpatterns = [
    path('add_announcement/', addAnnouncement.as_view(), name='add_announcement'),
    path('announcement_list/', AnnouncementListView.as_view(), name='announcement_list'),
    path('announcement_detail/<int:pk>/', AnnouncementDetailView.as_view(), name='announcement_detail'),
]