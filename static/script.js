// Minimal BioVerse Frontend
class BioVerseFrontend {
    constructor() {
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.createSpaceDust();
    }
    
    bindEvents() {
        document.getElementById('generateBtn').addEventListener('click', () => this.createAlien());
        document.getElementById('resetBtn').addEventListener('click', () => this.reset());
        document.getElementById('saveBtn')?.addEventListener('click', () => this.saveAlien());
        document.getElementById('planetInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.createAlien();
        });
    }
    
    async createAlien() {
        const planetName = document.getElementById('planetInput').value.trim();
        if (!planetName) {
            this.showError('Please enter a planet name');
            return;
        }
        
        this.showLoading(true);
        
        try {
            const response = await fetch('/api/create-alien', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ planetName: planetName })
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Failed to create alien after retries');
            }
            
            const data = await response.json();
            this.displayResults(data.planet, data.alien, data.image);
        } catch (error) {
            console.error('Error:', error);
            this.showError('Failed to create alien after all retry attempts. Please try again.');
        } finally {
            this.showLoading(false);
        }
    }
    
    displayResults(planetData, alienData, imageUrl) {
        // Store current data for saving
        this.currentPlanet = planetData;
        this.currentAlien = alienData;
        this.currentImage = imageUrl;
        
        // Ultra creative entrance animation
        const results = document.getElementById('results');
        results.style.display = 'flex';
        results.style.flexDirection = 'column';
        results.style.alignItems = 'center';
        results.style.opacity = '0';
        results.style.transform = 'translateY(100px) scale(0.8) rotateX(45deg)';
        
        setTimeout(() => {
            results.style.transition = 'all 1.2s cubic-bezier(0.175, 0.885, 0.32, 1.275)';
            results.style.opacity = '1';
            results.style.transform = 'translateY(0) scale(1) rotateX(0deg)';
        }, 200);
        
        // Planet info with ultra creative styling
        document.getElementById('planetName').textContent = planetData.name;
        document.getElementById('planetDescription').textContent = planetData.description;
        document.getElementById('planetTraits').innerHTML = `
            <div class="trait-item">
                <span class="trait-label">🌍 Gravity</span>
                <span class="trait-value">${planetData.gravity}g</span>
            </div>
            <div class="trait-item">
                <span class="trait-label">🌌 Atmosphere</span>
                <span class="trait-value">${planetData.atmosphere}</span>
            </div>
            <div class="trait-item">
                <span class="trait-label">🌡️ Temperature</span>
                <span class="trait-value">${planetData.temperature}°C</span>
            </div>
            <div class="trait-item">
                <span class="trait-label">⚡ Radiation</span>
                <span class="trait-value">${planetData.radiation}</span>
            </div>
            <div class="trait-item">
                <span class="trait-label">💧 Water</span>
                <span class="trait-value">${planetData.water}</span>
            </div>
            <div class="trait-item">
                <span class="trait-label">⏰ Day Length</span>
                <span class="trait-value">${planetData.dayLength}h</span>
            </div>
            <div class="trait-item">
                <span class="trait-label">📅 Year Length</span>
                <span class="trait-value">${planetData.yearLength}d</span>
            </div>
        `;
        
        // Alien info with ultra creative styling
        document.getElementById('alienImage').src = imageUrl;
        document.getElementById('alienName').textContent = alienData.name;
        document.getElementById('alienDescription').textContent = alienData.description;
        document.getElementById('alienTraits').innerHTML = `
            <h4>🧬 Physical Traits</h4>
            ${alienData.physicalTraits.map((t, i) =>
                `<div style="animation-delay: ${i * 0.15}s">✨ ${t}</div>`
            ).join('')}
            <h4>⚡ Special Abilities</h4>
            ${alienData.abilities.map((a, i) =>
                `<div style="animation-delay: ${(i + alienData.physicalTraits.length) * 0.15}s">🚀 ${a}</div>`
            ).join('')}
            <h4>🔬 Scientific Classification</h4>
            <div style="animation-delay: ${(alienData.physicalTraits.length + alienData.abilities.length) * 0.15}s">
                <em>🧪 ${alienData.scientificName}</em>
            </div>
        `;
        
        // Show save button
        const saveBtn = document.getElementById('saveBtn');
        if (saveBtn) {
            saveBtn.style.display = 'block';
        }
        
        // Ultra creative animations
        this.ultraAnimateElements();
    }
    
    ultraAnimateElements() {
        const elements = document.querySelectorAll('.trait-item, .alien-traits > div');
        elements.forEach((el, index) => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(30px) scale(0.9)';
            el.style.filter = 'blur(5px)';
            
            setTimeout(() => {
                el.style.transition = 'all 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275)';
                el.style.opacity = '1';
                el.style.transform = 'translateY(0) scale(1)';
                el.style.filter = 'blur(0px)';
            }, index * 150);
        });
        
        // Add particle effects
        this.addParticleEffects();
    }
    
    addParticleEffects() {
        const results = document.getElementById('results');
        for (let i = 0; i < 20; i++) {
            const particle = document.createElement('div');
            particle.style.cssText = `
                position: absolute;
                width: 2px;
                height: 2px;
                background: rgba(0, 255, 255, 0.8);
                border-radius: 50%;
                pointer-events: none;
                animation: particleFloat ${3 + Math.random() * 4}s linear infinite;
                left: ${Math.random() * 100}%;
                top: ${Math.random() * 100}%;
                animation-delay: ${Math.random() * 2}s;
            `;
            results.appendChild(particle);
        }
        
        // Add CSS for particle animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes particleFloat {
                0% {
                    transform: translateY(0) translateX(0) scale(0);
                    opacity: 0;
                }
                10% {
                    opacity: 1;
                    transform: scale(1);
                }
                90% {
                    opacity: 1;
                }
                100% {
                    transform: translateY(-100px) translateX(${Math.random() * 100 - 50}px) scale(0);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);
    }
    
    animateElements() {
        const elements = document.querySelectorAll('.trait-item, .alien-traits > div');
        elements.forEach((el, index) => {
            el.style.opacity = '0';
            el.style.transform = 'translateX(-30px)';
            setTimeout(() => {
                el.style.transition = 'all 0.6s ease';
                el.style.opacity = '1';
                el.style.transform = 'translateX(0)';
            }, index * 100);
        });
    }
    
    showLoading(show) {
        document.getElementById('loading').style.display = show ? 'block' : 'none';
        document.getElementById('generateBtn').disabled = show;
    }
    
    showError(message) {
        alert(message);
    }
    
    reset() {
        document.getElementById('results').style.display = 'none';
        document.getElementById('planetInput').value = '';
        document.getElementById('planetInput').focus();
    }
    
    async saveAlien() {
        const saveBtn = document.getElementById('saveBtn');
        const originalText = saveBtn.innerHTML;
        
        saveBtn.innerHTML = '<span class="btn-saving">Saving...</span>';
        saveBtn.disabled = true;
        
        try {
            const response = await fetch('/api/save-alien', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    planet: this.currentPlanet,
                    alien: this.currentAlien,
                    image: this.currentImage
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                alert('Alien saved successfully!');
                document.getElementById('saveBtn').style.display = 'none';
            } else {
                throw new Error(result.error || 'Failed to save alien');
            }
        } catch (error) {
            console.error('Error saving alien:', error);
            alert('Failed to save alien. Please try again.');
        } finally {
            saveBtn.innerHTML = originalText;
            saveBtn.disabled = false;
        }
    }
    
    createSpaceDust() {
        const container = document.createElement('div');
        container.className = 'space-dust';
        for (let i = 0; i < 30; i++) {
            const particle = document.createElement('div');
            particle.className = 'dust-particle';
            particle.style.cssText = `
                position: absolute;
                width: 2px;
                height: 2px;
                background: rgba(255, 255, 255, 0.8);
                border-radius: 50%;
                left: ${Math.random() * 100}%;
                top: ${Math.random() * 100}%;
                animation: float ${Math.random() * 10 + 15}s infinite linear;
            `;
            container.appendChild(particle);
        }
        document.querySelector('.galaxy-background').appendChild(container);
    }
}

// Contact Form Handler
class ContactForm {
    constructor() {
        this.init();
    }
    
    init() {
        const contactForm = document.getElementById('contactForm');
        if (contactForm) {
            contactForm.addEventListener('submit', (e) => this.handleSubmit(e));
        }
    }
    
    async handleSubmit(e) {
        e.preventDefault();
        
        const form = e.target;
        const submitBtn = form.querySelector('.submit-btn');
        const btnText = submitBtn.querySelector('.btn-text');
        const btnLoading = submitBtn.querySelector('.btn-loading');
        
        // Show loading state
        btnText.style.display = 'none';
        btnLoading.style.display = 'inline-block';
        submitBtn.disabled = true;
        
        // Get form data
        const formData = new FormData(form);
        const data = Object.fromEntries(formData);
        
        try {
            const response = await fetch('/api/contact', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.showSuccess(result.message);
                form.reset();
            } else {
                this.showError(result.error || 'Failed to send message');
            }
        } catch (error) {
            console.error('Error:', error);
            this.showError('Failed to send message. Please try again.');
        } finally {
            // Reset button state
            btnText.style.display = 'inline-block';
            btnLoading.style.display = 'none';
            submitBtn.disabled = false;
        }
    }
    
    showSuccess(message) {
        const alert = this.createAlert(message, 'success');
        document.querySelector('.contact-container').appendChild(alert);
        setTimeout(() => alert.remove(), 5000);
    }
    
    showError(message) {
        const alert = this.createAlert(message, 'error');
        document.querySelector('.contact-container').appendChild(alert);
        setTimeout(() => alert.remove(), 5000);
    }
    
    createAlert(message, type) {
        const alert = document.createElement('div');
        alert.className = `alert alert-${type}`;
        alert.style.cssText = `
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 10px;
            text-align: center;
            font-weight: 600;
            background: ${type === 'success' ? 'rgba(0, 255, 0, 0.1)' : 'rgba(255, 107, 107, 0.1)'};
            border: 1px solid ${type === 'success' ? '#00ff00' : '#ff6b6b'};
            color: ${type === 'success' ? '#00ff00' : '#ff6b6b'};
        `;
        alert.textContent = message;
        return alert;
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    new BioVerseFrontend();
    new ContactForm();
});