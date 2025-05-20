document.getElementById('appointment-form').addEventListener('submit', async function (e) {
    e.preventDefault(); // spreči reload

    const form = e.target;
    const formData = new FormData(form);
    const errors = [];

    const urlData = document.getElementById('url-data');
    const appointmentUrl = urlData.dataset.appointmentUrl;
    const confirmationUrl = urlData.dataset.confirmationUrl;

    // jednostavna validacija
    if (formData.get('name').trim() === '') errors.push('Ime je obavezno.');
    if (!formData.get('email').includes('@')) errors.push('Email nije validan.');
    if (formData.get('phone').trim() === '') errors.push('Telefon je obavezan.');
    if (formData.get('date').trim() === '') errors.push('Datum je obavezan.');
    if (formData.get('time') === '0') errors.push('Morate izabrati vreme.');

    const errorDiv = document.getElementById('form-errors');
    errorDiv.innerHTML = '';

    if (errors.length > 0) {
        errors.forEach(err => {
            errorDiv.innerHTML += `<p>${err}</p>`;
        });
        return;
    }

    // dodaj CSRF token ako koristiš Django
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // pošalji podatke backendu
    const response = await fetch(appointmentUrl, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
        },
        body: formData
    });

    if (response.ok) {
        window.location.href = confirmationUrl;
        document.getElementById('appointment-form').reset();
    } else {
        errorDiv.innerHTML = '<p>Došlo je do greške prilikom zakazivanja.</p>';
    }
});
