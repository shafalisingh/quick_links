const API_URL = window.location.origin;

// Shorten URL
async function shortenUrl() {
    const longUrl = document.getElementById('longUrl').value;
    const errorDiv = document.getElementById('error');
    const resultDiv = document.getElementById('result');
    
    // Clear previous states
    errorDiv.classList.add('hidden');
    resultDiv.classList.add('hidden');
    
    // Validate URL
    if (!longUrl) {
        showError('Please enter a URL');
        return;
    }
    
    if (!isValidUrl(longUrl)) {
        showError('Please enter a valid URL (must start with http:// or https://)');
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/shorten`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ long_url: longUrl })
        });
        
        if (!response.ok) {
            throw new Error('Failed to shorten URL');
        }
        
        const data = await response.json();
        
        // Show result
        document.getElementById('shortUrl').value = data.short_url;
        document.getElementById('analyticsLink').href = `#analytics/${data.short_code}`;
        document.getElementById('analyticsLink').onclick = () => {
            loadAnalyticsByCode(data.short_code);
            return false;
        };
        resultDiv.classList.remove('hidden');
        
    } catch (error) {
        showError('Error shortening URL. Please try again.');
        console.error(error);
    }
}

// Copy URL to clipboard
function copyUrl() {
    const shortUrl = document.getElementById('shortUrl');
    shortUrl.select();
    document.execCommand('copy');
    
    // Show feedback
    const btn = event.target;
    const originalText = btn.textContent;
    btn.textContent = '✓ Copied!';
    btn.style.background = '#4CAF50';
    
    setTimeout(() => {
        btn.textContent = originalText;
        btn.style.background = '';
    }, 2000);
}

// Load analytics
async function loadAnalytics() {
    const code = document.getElementById('analyticsCode').value;
    
    if (!code) {
        showError('Please enter a short code');
        return;
    }
    
    await loadAnalyticsByCode(code);
}

async function loadAnalyticsByCode(code) {
    try {
        const response = await fetch(`${API_URL}/analytics/${code}`);
        
        if (!response.ok) {
            throw new Error('Analytics not found');
        }
        
        const data = await response.json();
        displayAnalytics(data);
        
    } catch (error) {
        showError('Could not load analytics. Check the short code and try again.');
        console.error(error);
    }
}

// Display analytics
function displayAnalytics(data) {
    const content = `
        <div class="analytics-card">
            <h2>Analytics for /${data.short_code}</h2>
            
            <div class="stat-grid">
                <div class="stat-box">
                    <h3>Total Clicks</h3>
                    <div class="stat-value">${data.total_clicks}</div>
                </div>
                <div class="stat-box">
                    <h3>Created</h3>
                    <div class="stat-value">${formatDate(data.created_at)}</div>
                </div>
            </div>
            
            <div style="margin-top: 2rem; padding: 1rem; background: white; border-radius: 10px;">
                <strong>Original URL:</strong><br>
                <a href="${data.long_url}" target="_blank" style="color: #667eea; word-break: break-all;">
                    ${data.long_url}
                </a>
            </div>
            
            ${data.recent_clicks && data.recent_clicks.length > 0 ? `
                <div class="clicks-list">
                    <h3>Recent Clicks</h3>
                    ${data.recent_clicks.map(click => `
                        <div class="click-item">
                            <span class="click-time">${formatDateTime(click.clicked_at)}</span>
                        </div>
                    `).join('')}
                </div>
            ` : '<p style="margin-top: 2rem; text-align: center; color: #666;">No clicks yet</p>'}
        </div>
    `;
    
    document.getElementById('analyticsContent').innerHTML = content;
    showSection('analyticsSection');
}

// Navigation functions
function showShortener() {
    showSection('shortenerSection');
}

function showAnalyticsSearch() {
    showSection('analyticsSearchSection');
}

function showSection(sectionId) {
    document.querySelectorAll('.section').forEach(section => {
        section.classList.add('hidden');
    });
    document.getElementById(sectionId).classList.remove('hidden');
}

// Reset form
function resetForm() {
    document.getElementById('longUrl').value = '';
    document.getElementById('result').classList.add('hidden');
    document.getElementById('error').classList.add('hidden');
}

// Utility functions
function showError(message) {
    const errorDiv = document.getElementById('error');
    errorDiv.textContent = message;
    errorDiv.classList.remove('hidden');
}

function isValidUrl(string) {
    try {
        const url = new URL(string);
        return url.protocol === 'http:' || url.protocol === 'https:';
    } catch (_) {
        return false;
    }
}

function formatDate(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays === 0) return 'Today';
    if (diffDays === 1) return 'Yesterday';
    if (diffDays < 7) return `${diffDays}d ago`;
    if (diffDays < 30) return `${Math.floor(diffDays / 7)}w ago`;
    return `${Math.floor(diffDays / 30)}mo ago`;
}

function formatDateTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}