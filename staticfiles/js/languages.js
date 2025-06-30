document.addEventListener('DOMContentLoaded', function () {

function setLanguage(lang) {
  const csrftoken = getCookie('csrftoken'); // Funkcija za čitanje CSRF kolačića
  const nextUrl = window.location.pathname + window.location.search;

  fetch("{% url 'set_language' %}", {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'X-CSRFToken': csrftoken,
    },
    body: new URLSearchParams({
      language: lang,
      next: nextUrl
    })
  })
  .then(response => {
    if (response.ok) {
      window.location.href = nextUrl; // ili samo window.location.reload();
    } else {
      alert('Greška pri promeni jezika.');
    }
  })
  .catch(() => alert('Greška pri promeni jezika.'));
}

// Funkcija za dohvat CSRF kolačića iz browsera
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}


});