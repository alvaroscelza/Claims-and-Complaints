from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .forms import suggestionsForm


def send_suggestion(request):
    if request.method == 'POST':
        form = suggestionsForm(request.POST)
        if form.is_valid():
            suggestions = form.save()

            subject = 'Nueva Sugerencia'
            message = f'Se ha recibido una nueva sugerencia:\n\n{str(suggestions)}'
            from_email = 'tu_email@example.com'
            recipient_list = ['quejassyreclamos@gmail.com']
            send_mail(subject, message, from_email, recipient_list)

            return redirect('success')

    else:
        form = suggestionsForm()

    return render(request, 'template.html', {'form': form})
