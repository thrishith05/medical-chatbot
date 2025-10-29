// Configuration
const API_URL = 'http://localhost:8001';

// DOM Elements
const queryInput = document.getElementById('queryInput');
const sendButton = document.getElementById('sendButton');
const chatMessages = document.getElementById('chatMessages');
const statusIndicator = document.querySelector('.status-indicator');
const statusDot = document.querySelector('.status-dot');
const apiUrlInput = document.getElementById('apiUrl');

// Get API URL from input
function getApiUrl() {
    return apiUrlInput.value || API_URL;
}

// Update status indicator
function updateStatus(status, text) {
    statusDot.className = 'status-dot';
    if (status === 'loading') {
        statusDot.classList.add('loading');
        statusIndicator.querySelector('span').textContent = text || 'Processing...';
    } else if (status === 'error') {
        statusDot.classList.add('error');
        statusIndicator.querySelector('span').textContent = text || 'Error';
    } else {
        statusIndicator.querySelector('span').textContent = text || 'Ready';
    }
}

// Add message to chat
function addMessage(content, isUser = false, contexts = []) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user' : 'assistant'}`;
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = isUser ? '👤' : '🤖';
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    
    const messageText = document.createElement('div');
    messageText.className = 'message-text';
    messageText.textContent = content;
    
    messageContent.appendChild(messageText);
    
    // Don't show sources - user requested single source without displaying contexts
    // Contexts are hidden from UI
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(messageContent);
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Add loading indicator
function addLoadingIndicator() {
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'message assistant';
    loadingDiv.id = 'loadingIndicator';
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = '🤖';
    
    const loadingContent = document.createElement('div');
    loadingContent.className = 'message-content';
    
    const loadingDots = document.createElement('div');
    loadingDots.className = 'loading-dots';
    for (let i = 0; i < 3; i++) {
        const dot = document.createElement('span');
        loadingDots.appendChild(dot);
    }
    
    loadingContent.appendChild(loadingDots);
    loadingDiv.appendChild(avatar);
    loadingDiv.appendChild(loadingContent);
    
    chatMessages.appendChild(loadingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Remove loading indicator
function removeLoadingIndicator() {
    const loadingIndicator = document.getElementById('loadingIndicator');
    if (loadingIndicator) {
        loadingIndicator.remove();
    }
}

// Send query to API
async function sendQuery() {
    const query = queryInput.value.trim();
    
    if (!query) {
        alert('Please enter a question');
        return;
    }
    
    // Disable button
    sendButton.disabled = true;
    updateStatus('loading', 'Sending query...');
    
    // Add user message
    addMessage(query, true);
    
    // Clear input
    queryInput.value = '';
    
    // Add loading indicator
    addLoadingIndicator();
    
    try {
        const topK = document.getElementById('topK').value;
        const apiUrl = getApiUrl();
        
        const response = await fetch(`${apiUrl}/query`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: query,
                top_k: parseInt(topK)
            })
        });
        
        // Remove loading indicator
        removeLoadingIndicator();
        
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Add assistant message with contexts
        addMessage(data.answer, false, data.contexts);
        
        updateStatus('ready', 'Ready');
    } catch (error) {
        console.error('Error:', error);
        removeLoadingIndicator();
        
        addMessage(
            `Sorry, I encountered an error. Please check:\n\n` +
            `1. API is running on: ${getApiUrl()}\n` +
            `2. Network connection\n` +
            `3. Error: ${error.message}`,
            false
        );
        
        updateStatus('error', 'Connection error');
    } finally {
        sendButton.disabled = false;
    }
}

// Handle Enter key (with Shift for new line)
queryInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendQuery();
    }
});

// Check API health on load
async function checkApiHealth() {
    try {
        const apiUrl = getApiUrl();
        const response = await fetch(`${apiUrl}/health`);
        
        if (response.ok) {
            updateStatus('ready', 'API Connected');
        } else {
            updateStatus('error', 'API Error');
        }
    } catch (error) {
        updateStatus('error', 'API Offline');
    }
}

// Auto-resize textarea
queryInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = (this.scrollHeight) + 'px';
});

// Check health periodically
setInterval(checkApiHealth, 30000);
checkApiHealth();

