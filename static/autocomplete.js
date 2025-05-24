// static/autocomplete.js
document.addEventListener('DOMContentLoaded', function () {
    const input = document.getElementById('city-input');
    const suggestions = document.getElementById('suggestions');

    input.addEventListener('input', async function () {
        const query = this.value.trim();
        if (query.length < 2) return;

        try {
            const res = await fetch(`/api/suggest?query=${encodeURIComponent(query)}`);
            const data = await res.json();

            // Очистка предыдущих подсказок
            suggestions.innerHTML = '';

            // Добавление новых подсказок
            data.forEach(city => {
                const option = document.createElement('option');
                option.value = city;
                suggestions.appendChild(option);
            });
        } catch (err) {
            console.error("Ошибка получения подсказок:", err);
        }
    });

    // Обработка клика по форме
    document.getElementById('search-form').addEventListener('submit', function(e) {
        const city = input.value.trim();
        if (city) {
            window.location.href = '/weather/' + encodeURIComponent(city);
            e.preventDefault();
        }
    });
});