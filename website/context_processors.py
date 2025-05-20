from .models import Config
from django.urls import resolve, reverse
from .forms import AppointmentForm


def config(request):
    # Dohvati prvog klijenta sa is_default=True
    config = Config.objects.all().first()
    form = AppointmentForm()
    return {'config': config, 'form': form}


def breadcrumbs(request):
    """Generiše breadcrumbs na osnovu trenutnog URL-a."""
    url_name = resolve(request.path_info).url_name  # Dobijamo ime rute
    kwargs = request.resolver_match.kwargs
    breadcrumbs = [("Početna", "/")]

    if url_name == "about":
        breadcrumbs.append(("O nama", "/about"))
    elif url_name == "contact":
        breadcrumbs.append(("Kontakt", "/contact"))
    elif url_name == "products":
        product_slug = kwargs.get("slug", "")  # Uzmi slug iz URL-a
        if product_slug == "long":
            breadcrumbs.append(("Duge haljine", "/products/long"))
        elif product_slug == "short":
            breadcrumbs.append(("Kratke haljine", "/products/short"))
        elif product_slug == "woman":
            breadcrumbs.append(("Zene", "/products/woman"))
        elif product_slug == "girls":
            breadcrumbs.append(("Devojcice", "/products/girls"))
        elif product_slug == "bestseller":
            breadcrumbs.append(("Najprodavanije", "/products/bestseller"))

    elif url_name == "products2":
        product_slug = kwargs.get("slug", "")  # Uzmi slug iz URL-a
        breadcrumbs.append(("Svi proizvodi", reverse("all_products")))
        breadcrumbs.append((product_slug.replace("-", " ").title(), request.path))  # Prikazivanje lepog naziva
    elif url_name == "services":
        product_slug = kwargs.get("slug", "")  # Uzmi slug iz URL-a
        breadcrumbs.append(("Sve usluge", reverse("services")))
        breadcrumbs.append((product_slug.replace("-", " ").title(), request.path))  # Prikazivanje lepog naziva

    return {"breadcrumbs": breadcrumbs}