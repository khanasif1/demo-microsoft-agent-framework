/**
 * JavaScript for Microsoft Agent Framework Demo
 */

async function submitQuery() {
    const queryInput = document.getElementById('queryInput');
    const submitBtn = document.getElementById('submitBtn');
    const btnText = document.getElementById('btnText');
    const btnLoader = document.getElementById('btnLoader');
    const resultsSection = document.getElementById('resultsSection');
    const resultsContainer = document.getElementById('resultsContainer');
    
    const query = queryInput.value.trim();
    
    if (!query) {
        alert('Please enter a query');
        return;
    }
    
    // Get selected agents
    const checkboxes = document.querySelectorAll('.agent-checkboxes input[type="checkbox"]:checked');
    const selectedAgents = Array.from(checkboxes).map(cb => cb.value);
    
    if (selectedAgents.length === 0) {
        alert('Please select at least one agent');
        return;
    }
    
    // Disable button and show loader
    submitBtn.disabled = true;
    btnText.style.display = 'none';
    btnLoader.style.display = 'inline-block';
    
    try {
        const response = await fetch('/api/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                query: query,
                agents: selectedAgents
            })
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            displayResults(data.results);
        } else {
            displayError(data.error || 'An error occurred');
        }
    } catch (error) {
        displayError('Failed to communicate with server: ' + error.message);
    } finally {
        // Re-enable button
        submitBtn.disabled = false;
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
    }
}

function displayResults(results) {
    const resultsSection = document.getElementById('resultsSection');
    const resultsContainer = document.getElementById('resultsContainer');
    
    resultsContainer.innerHTML = '';
    
    // Process each agent's results
    for (const [agentKey, agentResult] of Object.entries(results)) {
        const agentDiv = document.createElement('div');
        agentDiv.className = 'agent-result';
        
        const agentName = agentResult.agent || agentKey;
        const status = agentResult.status || 'unknown';
        const statusClass = status === 'success' ? 'status-success' : 'status-error';
        
        let content = `
            <h3>
                ${getAgentIcon(agentKey)} ${agentName}
                <span class="status-badge ${statusClass}">${status}</span>
            </h3>
        `;
        
        if (status === 'error') {
            content += `<div class="error-message">${agentResult.message || 'Unknown error'}</div>`;
        } else if (agentResult.data && agentResult.data.length > 0) {
            content += formatAgentData(agentKey, agentResult.data);
        } else {
            content += '<p>No data available</p>';
        }
        
        agentDiv.innerHTML = content;
        resultsContainer.appendChild(agentDiv);
    }
    
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

function formatAgentData(agentKey, data) {
    if (agentKey === 'bbc_news' || agentKey === 'techcrunch') {
        return formatNewsData(data);
    } else if (agentKey === 'crypto') {
        return formatCryptoData(data);
    } else if (agentKey === 'stocks') {
        return formatStockData(data);
    }
    return '<p>Data format not recognized</p>';
}

function formatNewsData(articles) {
    let html = '<ul class="data-list">';
    articles.forEach(article => {
        html += `
            <li class="data-item">
                <strong>${escapeHtml(article.title)}</strong>
                ${article.url ? `<a href="${escapeHtml(article.url)}" target="_blank">Read more →</a>` : ''}
            </li>
        `;
    });
    html += '</ul>';
    return html;
}

function formatCryptoData(cryptos) {
    let html = '<ul class="data-list">';
    cryptos.forEach(crypto => {
        let changeClass = 'positive';
        const changeStr = crypto.change_24h || 'N/A';
        if (changeStr !== 'N/A') {
            const changeNum = parseFloat(changeStr);
            if (changeNum < 0) {
                changeClass = 'negative';
            }
        }
        html += `
            <li class="data-item">
                <div class="crypto-item">
                    <span><strong>${escapeHtml(crypto.name)} (${escapeHtml(crypto.symbol)})</strong></span>
                    <span>${escapeHtml(crypto.price)}</span>
                    <span class="${changeClass}">${escapeHtml(changeStr)}</span>
                    <span style="font-size: 0.9em; color: #666;">MCap: ${escapeHtml(crypto.market_cap || 'N/A')}</span>
                </div>
            </li>
        `;
    });
    html += '</ul>';
    return html;
}

function formatStockData(stocks) {
    let html = '<ul class="data-list">';
    stocks.forEach(stock => {
        let changeClass = 'positive';
        const changeStr = stock.change || 'N/A';
        if (changeStr !== 'N/A') {
            const changeNum = parseFloat(changeStr);
            if (changeNum < 0) {
                changeClass = 'negative';
            }
        }
        html += `
            <li class="data-item">
                <div class="stock-item">
                    <span><strong>${escapeHtml(stock.symbol)}</strong> - ${escapeHtml(stock.name)}</span>
                    <span>${escapeHtml(stock.price)}</span>
                    <span class="${changeClass}">${escapeHtml(changeStr)}</span>
                </div>
                ${stock.note ? `<div style="font-size: 0.9em; color: #666; margin-top: 5px;">${escapeHtml(stock.note)}</div>` : ''}
            </li>
        `;
    });
    html += '</ul>';
    return html;
}

function getAgentIcon(agentKey) {
    const icons = {
        'bbc_news': '📰',
        'techcrunch': '💻',
        'crypto': '₿',
        'stocks': '📈'
    };
    return icons[agentKey] || '🤖';
}

function displayError(message) {
    const resultsSection = document.getElementById('resultsSection');
    const resultsContainer = document.getElementById('resultsContainer');
    
    resultsContainer.innerHTML = `
        <div class="error-message">
            <strong>Error:</strong> ${escapeHtml(message)}
        </div>
    `;
    
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

function escapeHtml(text) {
    if (typeof text !== 'string') return text;
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Allow submitting with Enter key (Ctrl+Enter in textarea)
document.addEventListener('DOMContentLoaded', function() {
    const queryInput = document.getElementById('queryInput');
    queryInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && e.ctrlKey) {
            submitQuery();
        }
    });
});
