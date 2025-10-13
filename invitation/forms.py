from django import forms
from invitation.models import Invitation


class InvitationForm(forms.ModelForm):
    class Meta:
        model = Invitation
        fields = [ 'email', 'description', 'latitude', 'longitude']
        widgets = {'description': forms.Textarea(attrs={'rows': 4}),
                   'latitude': forms.HiddenInput(),
                   'longitude': forms.HiddenInput(),
                   }
