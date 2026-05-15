// ==================== DISPLAY ANALYSIS RESULTS ====================

function displayResults(data) {
    const { prediction, recommendations, image_url } = data;

    const resultsSection = document.getElementById('resultsSection');
    resultsSection.style.display = 'block';
    resultsSection.classList.add('animate-in');

    // Soil Type with animation
    const soilTypeEl = document.getElementById('resultSoilType');
    soilTypeEl.textContent = prediction.soil_type;
    soilTypeEl.style.animation = 'slideDown 0.5s ease';

    // Confidence with smooth animation
    const confidencePercent = prediction.confidence_percent;
    const confidenceFill = document.getElementById('confidenceFill');
    confidenceFill.style.transition = 'width 1s cubic-bezier(0.4, 0, 0.2, 1)';
    confidenceFill.style.width = `${confidencePercent}%`;
    
    const confidenceText = document.getElementById('confidenceText');
    confidenceText.textContent = `${confidencePercent}% confidence`;
    confidenceText.style.animation = 'fadeIn 0.5s ease 0.3s both';

    // Image with fade in
    const resultImage = document.getElementById('resultImage');
    resultImage.style.opacity = '0';
    resultImage.src = image_url;
    resultImage.onload = () => {
        resultImage.style.transition = 'opacity 0.5s ease';
        resultImage.style.opacity = '1';
    };

    // Properties with staggered animation
    const propertiesList = document.getElementById('propertiesList');
    propertiesList.innerHTML = '';
    const props = prediction.properties;
    let delayIndex = 0;
    for (const [key, value] of Object.entries(props)) {
        const label = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
        const propItem = document.createElement('div');
        propItem.className = 'property-item';
        propItem.innerHTML = `
            <span class="property-label">${label}</span>
            <span class="property-value">${value}</span>
        `;
        propItem.style.animation = `slideUp 0.5s ease ${delayIndex * 0.1}s both`;
        propertiesList.appendChild(propItem);
        delayIndex++;
    }

    // Status Badge
    document.getElementById('soilStatus').textContent = recommendations.status;

    // Fertilizer Cards with animations
    const fertilizerList = document.getElementById('fertilizerList');
    fertilizerList.innerHTML = '';
    if (recommendations.general_fertilizers) {
        recommendations.general_fertilizers.forEach((fert, index) => {
            const card = document.createElement('div');
            card.className = 'fertilizer-card';
            card.innerHTML = `
                <h4>${fert.name}</h4>
                <p><strong>Purpose:</strong> ${fert.purpose}</p>
                <p><strong>Application:</strong> ${fert.application}</p>
                <p><strong>Frequency:</strong> ${fert.frequency}</p>
            `;
            card.style.animation = `scaleIn 0.5s ease ${index * 0.1}s both`;
            fertilizerList.appendChild(card);
        });
    }

    // Crop Specific
    const cropCard = document.getElementById('cropSpecificCard');
    const cropList = document.getElementById('cropSpecificList');
    if (recommendations.crop_specific_fertilizers && recommendations.crop_specific_fertilizers.length > 0) {
        cropCard.style.display = 'block';
        cropCard.style.animation = 'slideDown 0.5s ease';
        cropList.innerHTML = `<h4>For ${recommendations.selected_crop}</h4>`;
        recommendations.crop_specific_fertilizers.forEach((fert, index) => {
            const card = document.createElement('div');
            card.className = 'fertilizer-card';
            card.innerHTML = `
                <h4>${fert.name}</h4>
                <p><strong>Dose:</strong> ${fert.dose}</p>
                <p><strong>Timing:</strong> ${fert.timing}</p>
            `;
            card.style.animation = `scaleIn 0.5s ease ${index * 0.1}s both`;
            cropList.appendChild(card);
        });
    } else {
        cropCard.style.display = 'none';
    }

    // Organic Alternatives with animation
    const organicList = document.getElementById('organicList');
    organicList.innerHTML = '';
    if (recommendations.organic_alternatives) {
        recommendations.organic_alternatives.forEach((item, index) => {
            const li = document.createElement('li');
            li.textContent = item;
            li.style.animation = `slideDown 0.4s ease ${index * 0.08}s both`;
            organicList.appendChild(li);
        });
    }

    // Improvement Tips with animations
    const tipsList = document.getElementById('tipsList');
    tipsList.innerHTML = '';
    if (recommendations.improvement_tips) {
        recommendations.improvement_tips.forEach((tip, index) => {
            const tipCard = document.createElement('div');
            tipCard.className = 'tip-card';
            tipCard.textContent = tip;
            tipCard.style.animation = `slideDown 0.4s ease ${index * 0.08}s both`;
            tipsList.appendChild(tipCard);
        });
    }

    // Charts
    setTimeout(() => {
        drawPredictionsChart(prediction.all_predictions);
        drawCompositionChart(prediction.soil_type);
    }, 300);

    // Smooth scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });
    showToast('Analysis complete!', 'success', 2000);
}

    // Improvement Tips
    const tipsList = document.getElementById('tipsList');
    tipsList.innerHTML = '';
    if (recommendations.improvement_tips) {
        recommendations.improvement_tips.forEach(tip => {
            tipsList.innerHTML += `<div class="tip-card">${tip}</div>`;
        });
    }

    // Charts
    drawPredictionsChart(prediction.all_predictions);
    drawCompositionChart(prediction.soil_type);

    // Smooth scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

function drawPredictionsChart(predictions) {
    const ctx = document.getElementById('predictionsChart').getContext('2d');

    // Destroy existing chart if any
    if (window.predictionsChartInstance) {
        window.predictionsChartInstance.destroy();
    }

    const labels = Object.keys(predictions).map(
        s => s.charAt(0).toUpperCase() + s.slice(1)
    );
    const values = Object.values(predictions);

    const colors = [
        'rgba(46, 125, 50, 0.8)',
        'rgba(255, 143, 0, 0.8)',
        'rgba(139, 69, 19, 0.8)',
        'rgba(28, 28, 28, 0.8)',
        'rgba(244, 208, 63, 0.8)',
        'rgba(133, 146, 158, 0.8)'
    ];

    window.predictionsChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Confidence %',
                data: values,
                backgroundColor: colors,
                borderColor: colors.map(c => c.replace('0.8', '1')),
                borderWidth: 2,
                borderRadius: 8,
                borderSkipped: false
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    borderRadius: 8,
                    titleFont: { size: 14, weight: 'bold' },
                    bodyFont: { size: 13 }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)',
                        drawBorder: false
                    },
                    ticks: {
                        callback: value => value + '%',
                        color: '#666'
                    }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: '#666' }
                }
            },
            animation: {
                duration: 1000,
                easing: 'easeInOutQuart'
            }
        }
    });
}

function drawCompositionChart(soilType) {
    const ctx = document.getElementById('compositionChart').getContext('2d');

    if (window.compositionChartInstance) {
        window.compositionChartInstance.destroy();
    }

    const compositions = {
        loamy: { Sand: 40, Silt: 40, Clay: 20 },
        sandy: { Sand: 70, Silt: 15, Clay: 15 },
        clay: { Sand: 20, Silt: 20, Clay: 60 },
        silty: { Sand: 20, Silt: 60, Clay: 20 },
        peaty: { 'Organic Matter': 70, Mineral: 30 },
        chalky: { 'Calcium Carbonate': 40, Sand: 30, Clay: 30 }
    };

    const data = compositions[soilType] || compositions.loamy;

    const colors = [
        'rgba(244, 208, 63, 0.9)',
        'rgba(133, 146, 158, 0.9)',
        'rgba(211, 84, 0, 0.9)',
        'rgba(139, 69, 19, 0.9)'
    ];

    window.compositionChartInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: Object.keys(data),
            datasets: [{
                data: Object.values(data),
                backgroundColor: colors.slice(0, Object.keys(data).length),
                borderColor: '#fff',
                borderWidth: 3,
                hoverOffset: 10
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        font: { size: 13, weight: '500' },
                        color: '#666',
                        padding: 15,
                        boxWidth: 12
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    borderRadius: 8,
                    titleFont: { size: 14, weight: 'bold' },
                    bodyFont: { size: 13 }
                }
            },
            animation: {
                duration: 1000,
                easing: 'easeInOutQuart'
            }
        }
    });
}