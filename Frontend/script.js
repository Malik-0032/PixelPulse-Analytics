const API_BASE_URL = 'https://your-render-backend.onrender.com';

async function generatePixel() {
    const campaignName = document.getElementById('campaignName').value.trim();
    
    if (!campaignName) {
        alert('Please enter a campaign name');
        return;
    }

    const pixelUrl = `${API_BASE_URL}/pixel/${encodeURIComponent(campaignName)}.png`;
    const pixelHtml = `<img src="${pixelUrl}" alt="" style="width:1px;height:1px;">`;
    
    document.getElementById('pixelCode').textContent = pixelHtml;
    document.getElementById('pixelResult').style.display = 'block';
}

// Add smooth scroll animation
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Add animation on scroll
const observerOptions = {
    threshold: 0.1
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('fade-in');
        }
    });
}, observerOptions);

document.querySelectorAll('.feature-card').forEach(card => {
    observer.observe(card);
});