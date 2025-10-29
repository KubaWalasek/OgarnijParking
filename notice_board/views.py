from django.shortcuts import render
from django.views import View

from notice_board.forms import AnnouncementForm
from notice_board.models import Announcement


class addAnnouncement(View):
    def get(self, request):
        form = AnnouncementForm()
        return render(request, 'add_announcement.html', {'form': form})

    def post(self, request):
            form = AnnouncementForm(request.POST)
            if form.is_valid():
                announcement = form.save(commit=False)
                announcement.author = request.user
                announcement.save()
                form.save()
                return render(request, 'add_announcement.html', {'form': form})
            return render(request, 'add_announcement.html', {'form': form})


class AnnouncementListView(View):
    def get(self, request):
        announcements = Announcement.objects.all()
        return render(request, 'announcement_list.html', {'announcements': announcements})

class AnnouncementDetailView(View):
    def get(self, request, pk):
        announcement = Announcement.objects.get(pk=pk)
        return render(request, 'announcement_detail.html', {
            'announcement': announcement,
            'pk': pk
        })