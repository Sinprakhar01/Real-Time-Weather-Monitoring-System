function getWeather() {
    const city = document.getElementById('city').value;

    fetch('/weather', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({ city: city }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('City not found or API limit reached.');
        }
        return response.json();
    })
    .then(data => {
        const resultDiv = document.getElementById('result');
        const weatherData = data.weather_data;

        resultDiv.innerHTML = `
            <h2>${weatherData.city}</h2>
            <p>Temperature: ${weatherData.temperature}°C</p>
            <p>Feels Like: ${weatherData.feels_like}°C</p>
            <p>Weather Condition: ${weatherData.weather_condition}</p>
            <p>Date: ${weatherData.date}</p>
            <p style="color: red;">${data.alert ? data.alert : ''}</p>
        `;
    })
    .catch(error => {
        const resultDiv = document.getElementById('result');
        resultDiv.innerHTML = `<p style="color: red;">${error.message}</p>`;
    });
}
