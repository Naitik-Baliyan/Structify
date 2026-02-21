/**
 * =============================================================
 * STRUCTIFY BACKEND CONFIGURATION
 * =============================================================
 * Central configuration for backend API connectivity
 * Update BACKEND_URL to change the server location
 * =============================================================
 */

// Backend API Configuration
const API_CONFIG = {
  BACKEND_URL: 'http://127.0.0.1:8001',
  TIMEOUT: 10000, // 10 seconds
  RETRY_ATTEMPTS: 3,
  RETRY_DELAY: 1000 // 1 second
};

/**
 * Check if backend is reachable
 * @returns {Promise<boolean>} - True if backend is running
 */
async function checkBackendHealth() {
  try {
    const response = await fetch(`${API_CONFIG.BACKEND_URL}/`, {
      method: 'GET',
      timeout: 5000
    });
    return response.ok;
  } catch (error) {
    console.warn('Backend health check failed:', error.message);
    return false;
  }
}

/**
 * Fetch with retry logic and timeout
 * @param {string} url - Full URL to fetch
 * @param {object} options - Fetch options
 * @returns {Promise<Response>}
 */
async function fetchWithRetry(url, options = {}) {
  let lastError;
  
  for (let attempt = 0; attempt < API_CONFIG.RETRY_ATTEMPTS; attempt++) {
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), API_CONFIG.TIMEOUT);
      
      const response = await fetch(url, {
        ...options,
        signal: controller.signal
      });
      
      clearTimeout(timeoutId);
      
      if (response.ok) {
        return response;
      }
      
      lastError = new Error(`HTTP ${response.status}: ${response.statusText}`);
      
      // Don't retry on client errors (4xx)
      if (response.status >= 400 && response.status < 500) {
        throw lastError;
      }
      
    } catch (error) {
      lastError = error;
      
      // Don't retry if it's the last attempt
      if (attempt < API_CONFIG.RETRY_ATTEMPTS - 1) {
        await new Promise(resolve => setTimeout(resolve, API_CONFIG.RETRY_DELAY));
        console.log(`Retrying request... (attempt ${attempt + 2}/${API_CONFIG.RETRY_ATTEMPTS})`);
      }
    }
  }
  
  throw lastError || new Error('Failed to fetch after retries');
}

// Log configuration on load
console.log('%c[Config] Backend URL: ' + API_CONFIG.BACKEND_URL, 'color: #3b82f6; font-weight: bold;');
