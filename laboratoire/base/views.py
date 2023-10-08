
# Create your views here.
from django.shortcuts import get_object_or_404,render
from .models import Analyse,Chercheur,Slider,Appareil
from .utils import render_to_pdf
from django.core.mail import send_mail
from django.http import JsonResponse

def send_email(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        number = request.POST.get('number')
        message = request.POST.get('message')

        # Configure your email settings in Django settings.py
        send_mail(
            'Subject here',  # Subject of the email
            f'Name: {name}\nEmail: {email}\nNumber: {number}\nMessage: {message}',  # Message body
            'zbouzegzeg@gmail.com',  # From email address
            ['zbouzegzeg@gmail.com'],  # List of recipient email addresses
            fail_silently=False,
        )

        return JsonResponse({'message': 'Email sent successfully'}, status=200)

    return JsonResponse({'message': 'Invalid request'}, status=400)

def index(request):
    chercheurs = Chercheur.objects.filter(laboratoire__isnull=False)
    sliders=Slider.objects.all()
    appareils=Appareil.objects.all()
    print(appareils)
    return render(request,'index.html',{"chercheurs":chercheurs,"sliders":sliders,"appareils":appareils})
def generate_pdf_analyse(request,analyse_id):
    template_path = 'analyse.html'
    output="Demande Analyse N "+str(analyse_id)+".pdf"
    context = get_object_or_404(Analyse, pk=analyse_id)
    return render_to_pdf(template_path,output,context)
