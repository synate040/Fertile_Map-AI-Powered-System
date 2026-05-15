// ==================== MAIN APP LOGIC ====================

// Smooth scroll behavior for all navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Form input focus animations
document.querySelectorAll('input, textarea, select').forEach(input => {
    input.addEventListener('focus', function() {
        this.classList.add('focused');
    });
    
    input.addEventListener('blur', function() {
        this.classList.remove('focused');
    });
});

document.addEventListener('DOMContentLoaded', () => {
    checkAuth();
    initializeAnimations();

    // Check if viewing a past analysis
    const params = new URLSearchParams(window.location.search);
    if (params.get('view') === 'true') {
        const analysisData = JSON.parse(sessionStorage.getItem('viewAnalysis') || 'null');
        if (analysisData) {
            // Format data for displayResults function
            const formattedData = {
                prediction: {
                    soil_type: analysisData.soil_type,
                    confidence: analysisData.confidence,
                    confidence_percent: (analysisData.confidence * 100).toFixed(2),
                    properties: analysisData.properties,
                    all_predictions: {} // Not available from history
                },
                recommendations: analysisData.recommendations,
                image_url: analysisData.image_url
            };

            // Hide upload section and show results
            const uploadSection = document.getElementById('uploadSection');
            if (uploadSection) uploadSection.style.display = 'none';

            if (typeof displayResults === 'function') {
                displayResults(formattedData);
            }

            sessionStorage.removeItem('viewAnalysis');
        }
    }
});

// ==================== ANIMATION INITIALIZATION ====================
function initializeAnimations() {
    // Observe elements for intersection animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe cards and sections
    document.querySelectorAll('.card, .section, .stat-card, .chart-card').forEach(el => {
        observer.observe(el);
    });
}

// ==================== UTILITY FUNCTIONS ====================

// Debounce function for search and input handlers
function debounce(func, delay) {
    let timeoutId;
    return function(...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func.apply(this, args), delay);
    };
}

// Toast notification system
function showToast(message, type = 'info', duration = 3000) {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        background: var(--${type === 'error' ? 'danger' : type === 'success' ? 'success' : 'info'});
        color: white;
        border-radius: 8px;
        box-shadow: var(--shadow-lg);
        z-index: 9999;
        animation: slideDown 0.3s ease;
        font-weight: 600;
    `;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideUp 0.3s ease forwards';
        setTimeout(() => toast.remove(), 300);
    }, duration);
}

// Loading indicator
function showLoading(text = 'Loading...') {
    const loader = document.createElement('div');
    loader.className = 'global-loader';
    loader.innerHTML = `
        <div class="loader-content">
            <div class="spinner"></div>
            <p>${text}</p>
        </div>
    `;
    loader.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10000;
        backdrop-filter: blur(4px);
    `;
    document.body.appendChild(loader);
    return loader;
}

function hideLoading() {
    const loader = document.querySelector('.global-loader');
    if (loader) loader.remove();
}