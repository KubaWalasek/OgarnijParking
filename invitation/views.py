from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.views import View
from django.utils.html import strip_tags
from invitation.forms import InvitationForm

class CreateInvitationView(View):
    def get(self, request):
        form = InvitationForm()
        return render(request, 'invitation_form.html', {'form': form})

    def post(self, request):
        form = InvitationForm(request.POST)

        if not form.is_valid():
            return render(request, 'invitation_form.html', {'form': form})

        invitation = form.save(commit=False)
        invitation.author = request.user
        invitation.save()

        lat = form.cleaned_data['latitude']
        lng = form.cleaned_data['longitude']
        email_to = form.cleaned_data['email']
        description = form.cleaned_data['description']

        map_url = f'https://www.openstreetmap.org/?mlat={lat}&mlon={lng}#map=16/{lat}/{lng}'


        context = {
            'author_email': request.user.email,
            'map_url': map_url,
            'description': description,
        }

        html_body = render_to_string('invitation_template_email.html', context)
        text_body = strip_tags(html_body)

        msg = EmailMultiAlternatives(
            subject='Zaproszenie do miejsca',
            body=text_body,
            to=[email_to],
        )
        msg.attach_alternative(html_body, 'text/html')
        msg.send()

        return redirect('home')