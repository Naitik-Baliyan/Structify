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
  RETRY_ATTEMPTS: 2,
  RETRY_DELAY: 500 // 500 milliseconds
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
 * Retries up to 2 times on network failures or server errors
 * @param {string} url - Full URL to fetch
 * @param {object} options - Fetch options
 * @returns {Promise<Response>}
 */
async function fetchWithRetry(url, options = {}) {
  let lastError;
  const maxAttempts = Math.min(API_CONFIG.RETRY_ATTEMPTS, 2);
  
  for (let attempt = 0; attempt < maxAttempts; attempt++) {
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
      
      // Log retry attempt for server errors (5xx)
      console.warn(`[fetchWithRetry] Attempt ${attempt + 1}/${maxAttempts} failed with status ${response.status}`);
      
    } catch (error) {
      lastError = error;
      
      // Network errors, timeouts, or 5xx errors - try again
      if (attempt < maxAttempts - 1) {
        const delayMs = API_CONFIG.RETRY_DELAY * (attempt + 1);
        console.warn(`[fetchWithRetry] Request failed: ${error.message}. Retrying in ${delayMs}ms...`);
        await new Promise(resolve => setTimeout(resolve, delayMs));
      } else {
        console.error(`[fetchWithRetry] All ${maxAttempts} attempts failed`);
      }
    }
  }
  
  throw lastError || new Error('Backend unreachable. Please ensure FastAPI server is running on port 8000.');
}

// Log configuration on load
console.log('%c[Config] Backend URL: ' + API_CONFIG.BACKEND_URL, 'color: #3b82f6; font-weight: bold;');
