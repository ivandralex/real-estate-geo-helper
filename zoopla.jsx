javascript:(function(){
    const {latitude, longitude} = JSON.parse(document.querySelector('script[type="application/ld+json"]').textContent)['@graph'][3].geo;
    fetch(`https://europe-west2-news-analyzer-2022.cloudfunctions.net/apartment-distance?address=68-80%20hanbury%20street%20london%20e1%205jl&coordinates=${latitude},${longitude}`)
    .then(async res => {
        const {distance_info: { bicycling, transit, walking } } = JSON.parse(await res.text());
        const el = document.getElementById('listing-summary-details-heading');
        const newSpan = document.createElement("h3");
        newSpan.textContent = `Time to office: ${transit} by transport / ${bicycling} by bicycle`;
        el.appendChild(newSpan)
    });

    fetch(`https://europe-west2-news-analyzer-2022.cloudfunctions.net/apartment-distance?address=1201%2C%20Morello%20House%2C%2012%20Leamouth%20Road%2C%20London%2C%20E14%200US&coordinates=${latitude},${longitude}`)
    .then(async res => {
        const {distance_info: { bicycling, transit, walking } } = JSON.parse(await res.text());
        const el = document.getElementById('listing-summary-details-heading');
        const newSpan = document.createElement("h3");
        newSpan.textContent = `Time to rebyata: ${transit} by transport / ${walking} of walking`;
        el.appendChild(newSpan)
    });
})()
