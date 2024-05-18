import pandas as pd
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render
from django.conf import settings
from .forms import UploadFileForm
from django.http import HttpResponse

def handle_uploaded_file(f):
    data = pd.read_excel(f) if f.name.endswith('.xlsx') else pd.read_csv(f)
    summary = data.describe().to_string()
    return summary

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            summary = handle_uploaded_file(request.FILES['file'])
            try:
                send_mail(
                    subject=f'Python Assignment - {request.user.username}',
                    message=summary,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=['tech@themedius.ai'],
                )
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            except Exception as e:
                return HttpResponse(f'An error occurred: {str(e)}')
            return render(request, 'success.html')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})
