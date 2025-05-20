document.addEventListener('DOMContentLoaded', function () {
    const dateInput = document.querySelector('input[type="date"]');
    const timeSelect = document.querySelector('select');
    const fieldWrapperTime = document.querySelector('#field-wrapper-time');

    dateInput.addEventListener('change', function () {
        fetch(`/get-available-times/?date=${this.value}`)
            .then(response => response.json())
            .then(data => {
                fieldWrapperTime.classList.remove('hidden');
                timeSelect.innerHTML = '';

                if (data.available_times.length === 0) {
                    timeSelect.innerHTML = '<option disabled selected>Nema slobodnih termina</option>';
                } else {
                    timeSelect.innerHTML = '<option value="" disabled selected>Izaberite vreme</option>';
                    data.available_times.forEach(time => {
                        const opt = document.createElement('option');
                        opt.value = time[0];
                        opt.textContent = time[1];
                        timeSelect.appendChild(opt);
                    });
                }
            });
    });
});
