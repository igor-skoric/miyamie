from .models import Config
from django.urls import resolve, reverse
from .forms import AppointmentForm
from django.utils.translation import gettext_lazy as _

def config(request):
    # Dohvati prvog klijenta sa is_default=True
    config = Config.objects.all().first()
    form = AppointmentForm()
    return {'config': config, 'form': form}


def breadcrumbs(request):
    """Generiše breadcrumbs na osnovu trenutnog URL-a."""
    url_name = resolve(request.path_info).url_name  # Dobijamo ime rute
    kwargs = request.resolver_match.kwargs
    breadcrumbs = [(_("Početna"), "/")]

    if url_name == "showroom":
        breadcrumbs.append(("Showroom", "/showroom"))
    if url_name == "about":
        breadcrumbs.append((_("O nama"), "/about"))
    elif url_name == "contact":
        breadcrumbs.append((_("Kontakt"), "/contact"))
    elif url_name == "single_product":
            breadcrumbs.append((_("Sve haljine"), "/products/all"))
    elif url_name == "products":
        product_slug = kwargs.get("slug", "")  # Uzmi slug iz URL-a
        if product_slug == "all":
            breadcrumbs.append((_("Sve haljine"), "/products/all"))
        if product_slug == "search":
            breadcrumbs.append((_("Pretraga"), "/products/search"))
        if product_slug == "lechoix":
            breadcrumbs.append(("Lechoix", "/products/lechoix"))
        if product_slug == "long":
            breadcrumbs.append((_("Sve haljine"), "/products/all"))
            breadcrumbs.append((_("Duge haljine"), "/products/long"))
        elif product_slug == "short":
            breadcrumbs.append((_("Sve haljine"), "/products/all"))
            breadcrumbs.append((_("Kratke haljine"), "/products/short"))
        elif product_slug == "woman":
            breadcrumbs.append((_("Žene"), "/products/woman"))
        elif product_slug == "girls":
            breadcrumbs.append((_("Devojčice"), "/products/girls"))
        elif product_slug == "bestseller":
            breadcrumbs.append((_("Sve haljine"), "/products/all"))
            breadcrumbs.append((_("Najprodavanije"), "/products/bestseller"))
        elif product_slug == "for_sale":
            breadcrumbs.append((_("Sve haljine"), "/products/all"))
            breadcrumbs.append((_("Za Prodaju"), "/products/for_sale"))
        elif product_slug == "rent":
            breadcrumbs.append((_("Sve haljine"), "/products/all"))
            breadcrumbs.append((_("Za Inzjamljivanje"), "/products/rent"))

    elif url_name == "products2":
        product_slug = kwargs.get("slug", "")  # Uzmi slug iz URL-a
        breadcrumbs.append((_("Svi proizvodi"), reverse("all_products")))
        breadcrumbs.append((product_slug.replace("-", " ").title(), request.path))  # Prikazivanje lepog naziva
    elif url_name == "services":
        product_slug = kwargs.get("slug", "")  # Uzmi slug iz URL-a
        breadcrumbs.append((_("Sve usluge"), reverse("services")))
        breadcrumbs.append((product_slug.replace("-", " ").title(), request.path))  # Prikazivanje lepog naziva

    return {"breadcrumbs": breadcrumbs}