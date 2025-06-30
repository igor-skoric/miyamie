from django.shortcuts import render, get_object_or_404, redirect
from .models import Dress, Category, Appointment
from .forms import AppointmentForm
from django.http import JsonResponse
from datetime import time
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from email.utils import formataddr
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.db.models import Q
import os
import re

import logging
logger = logging.getLogger("django")


def home(request):
    long_dresses = Dress.objects.filter(category__name='LONG').exclude(home_page=0).order_by('home_page')[:4]
    short_dresses = Dress.objects.filter(category__name='SHORT').exclude(home_page=0).order_by('home_page')[:4]
    bestseller_dresses = Dress.objects.filter(tag='bestseller').exclude(home_page=0).order_by('home_page')[:4]

    context = {'short_dresses': short_dresses, 'long_dresses': long_dresses, 'bestseller_dresses': bestseller_dresses}
    return render(request, 'website/pages/index.html', context)




def showroom(request):
    image_folder = os.path.join(settings.BASE_DIR, 'static', 'img', 'showroomcompresed')

    def extract_number(filename):
        match = re.search(r'(\d+)', filename)
        return int(match.group(1)) if match else 0

    image_files = sorted(
        [f for f in os.listdir(image_folder) if f.lower().endswith('.webp')],
        key=extract_number
    )

    image_paths = [f'img/showroomcompresed/{f}' for f in image_files]
    context = {'image_paths': image_paths}
    return render(request, 'website/pages/showroom.html', context)



def contact(request):

    if request.POST:
        question(request.POST)
        title = 'Uspešno ste poslali poruku.'
        message = ''
        context = {'message': message, 'title': title}
        return render(request, 'website/pages/confirmation.html', context)
    else:
        context = {}
        return render(request, 'website/pages/contact.html', context)


def about(request):
    context = {}
    return render(request, 'website/pages/about.html', context)


def confirmation(request):
    title = 'Vaš termin je uspešno zakazan.'
    message = 'Uskoro ćete dobiti email sa svim detaljima, uključujući tačno vreme i lokaciju. Molimo vas da proverite svoj inbox (i spam folder ako ne vidite poruku u roku od nekoliko minuta).'
    context = {'message': message, 'title': title}
    return render(request, 'website/pages/confirmation.html', context)


def single_product(request, pk):
    product = Dress.objects.get(pk=pk)
    category_id = product.category.id
    related_products = Dress.objects.filter(category=category_id).exclude(pk=product.pk)
    context = {'product': product, 'related_products': related_products}
    return render(request, 'website/pages/single_product.html', context)


def products(request, slug):
    query = request.GET.get('search', '').strip()

    if slug not in ['all', 'lechoix', 'search', 'for_sale', 'rent']:
        category = get_object_or_404(Category, slug=slug)

    if slug == 'all':
        dresses = Dress.objects.filter(category__brand__slug='miyamia')
    elif slug == 'lechoix':
        dresses = Dress.objects.filter(category__brand__slug='lechoix')
    elif slug == 'bestseller':
        dresses = Dress.objects.filter(tag='bestseller')
    elif slug == 'search':
        dresses = Dress.objects.filter(
            Q(name__icontains=query)
        )
    elif slug == 'for_sale':
        dresses = Dress.objects.filter(tag='for_sale')
    elif slug == 'rent':
        dresses = Dress.objects.filter(tag='rent')
    else:
        dresses = Dress.objects.filter(category=category)



    return render(request, 'website/pages/products.html', {
        'dresses': dresses
    })


AVAILABLE_TIMES = [
    (time(10, 0), "10:00 - 12:00"),
    (time(12, 0), "12:00 - 14:00"),
    (time(14, 0), "14:00 - 16:00"),
    (time(16, 0), "16:00 - 18:00"),
    (time(18, 0), "18:00 - 20:00"),
    (time(20, 0), "20:00 - 22:00"),
]


def appointment_form(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        context = {
            'name': request.POST.get('name'),
            'phone': request.POST.get('phone'),
            'email': request.POST.get('email'),
            'date': request.POST.get('date'),
            "time": request.POST.get('time')
        }

        if form.is_valid():
            try:
                form.save()
                send_reservation_email(context)
                return JsonResponse({'success': True, 'message': 'Uspešno zakazano!'})
            except Exception as e:
                return JsonResponse({'success': False, 'message': 'Greška prilikom čuvanja podataka.'}, status=500)
        else:
            return JsonResponse({'success': False, 'message': 'Neispravni podaci.', 'errors': form.errors}, status=400)

    return JsonResponse({'success': False, 'message': 'Samo POST zahtevi su dozvoljeni.'}, status=405)


def get_available_times(request):
    """AJAX endpoint: vrati slobodne termine za izabrani dan"""
    selected_date = request.GET.get('date')

    if not selected_date:
        return JsonResponse({'error': 'No date provided'}, status=400)

    taken_times = Appointment.objects.filter(date=selected_date).values_list('time', flat=True)

    available = [
        (t, label)  # konvertuj time u string
        for t, label in AVAILABLE_TIMES
        if t not in taken_times
    ]

    return JsonResponse({'available_times': available})


def send_reservation_email(data):
    # Izvlačenje podataka iz `data`

    try:
        context = {
            'name': data.get('name'),
            'phone': data.get('phone'),
            'email': data.get('email'),
            'date': data.get("date"),
            "time": data.get('time'),
        }

        # Generisanje sadržaja emaila
        subject = "Vaši detalji porudžbine"
        # from_email = settings.EMAIL_HOST_USER

        from_email = formataddr(("Miya Mie", settings.EMAIL_HOST_USER))  # Ime i email adresa
        to_email = data.get('email')  # Pretpostavka da je kontakt email korisnika
        text_content = "Hvala Vam za vašu rezervaciju!"  # Tekstualni fallback
        html_content = render_to_string('website/pages/email.html', context)

        # Kreiranje emaila
        email = EmailMultiAlternatives(subject, text_content, from_email, [to_email, settings.EMAIL_HOST_USER])
        email.attach_alternative(html_content, "text/html")
        email.send()

    except Exception as e:
        logger.error(f"ERROR send_reservation_email: {e}")


def question(request):
    try:
        name = request.get('name')
        email = request.get('email')
        phone = request.get('phone')
        message = request.get('message')

        subject = (f"Question from {email} - {name} - {phone}")
        from_email = settings.EMAIL_HOST_USER

        email = EmailMultiAlternatives(subject, message, from_email, [from_email])
        email.send()
    except Exception as e:
        logger.error(f"ERROR question: {e}")