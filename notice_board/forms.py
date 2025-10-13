from django import forms
from .models import Announcement


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = (
            'title',
            'content',
            'category'
        )
        widgets = {'title': forms.TextInput(attrs={'placeholder': ' np. Warszawa, ul. Mazowiecka 25 na dwie noce.'}),
                   'content': forms.Textarea(attrs={'placeholder': 'Dodaj opis miejsca parkingowego.'})}