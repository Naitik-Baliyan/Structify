/**
 * =============================================================
 * STRUCTIFY AUTHENTICATION SYSTEM
 * =============================================================
 * Handles login/signup validation, localStorage mock database,
 * and smooth user interactions with professional error handling.
 * 
 * Features:
 * - Email & password validation
 * - localStorage-based user storage
 * - Smooth animations for errors
 * - Tab switching between login/signup
 * - XSS prevention with HTML escaping
 * =============================================================
 */

// ===== INITIALIZATION =====
/**
 * Run setup code when DOM is ready
 */
document.addEventListener('DOMContentLoaded', () => {
  initializeAuthUI();
  setupFormListeners();
  initializeStorageCheck();
});

// ===== STORAGE & DATABASE CONSTANTS =====
/**
 * Storage key for users in localStorage
 */
const USERS_STORAGE_KEY = 'structify_users';
const CURRENT_USER_KEY = 'structify_current_user';

// ===== EMAIL & PASSWORD VALIDATION =====
/**
 * Validate email format using regex
 * @param {string} email - Email address to validate
 * @returns {boolean} - True if valid email format
 */
function isValidEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email.trim());
}

/**
 * Validate password strength
 * @param {string} password - Password to validate
 * @returns {object} - { isValid: boolean, message: string }
 */
function validatePassword(password) {
  if (!password) {
    return { isValid: false, message: 'Password is required' };
  }
  
  if (password.length < 6) {
    return { isValid: false, message: 'Password must be at least 6 characters' };
  }
  
  // Optional: enforce stronger passwords (uncomment if needed)
  // const hasUpperCase = /[A-Z]/.test(password);
  // const hasLowerCase = /[a-z]/.test(password);
  // const hasNumbers = /\d/.test(password);
  // if (!hasUpperCase || !hasLowerCase || !hasNumbers) {
  //   return { isValid: false, message: 'Password must contain uppercase, lowercase, and numbers' };
  // }
  
  return { isValid: true, message: '' };
}

// ===== LOCALSTORAGE MANAGEMENT =====
/**
 * Get all users from localStorage
 * @returns {Array} - Array of user objects
 */
function getAllUsers() {
  const users = localStorage.getItem(USERS_STORAGE_KEY);
  return users ? JSON.parse(users) : [];
}

/**
 * Save users array to localStorage
 * @param {Array} users - Array of user objects to save
 */
function saveUsers(users) {
  localStorage.setItem(USERS_STORAGE_KEY, JSON.stringify(users));
}

/**
 * Find user by email
 * @param {string} email - Email to search for
 * @returns {object|null} - User object or null if not found
 */
function findUserByEmail(email) {
  const users = getAllUsers();
  return users.find(u => u.email.toLowerCase() === email.toLowerCase()) || null;
}

/**
 * Create new user account in localStorage
 * @param {object} userData - { name, email, password }
 * @returns {boolean} - True if user created successfully
 */
function createUser(userData) {
  const users = getAllUsers();
  
  // Check if email already exists
  if (findUserByEmail(userData.email)) {
    return false;
  }
  
  // Create new user object with timestamp
  const newUser = {
    id: Date.now(), // Simple ID using timestamp
    name: userData.name.trim(),
    email: userData.email.toLowerCase(),
    password: userData.password, // In production, this would be hashed
    createdAt: new Date().toISOString()
  };
  
  users.push(newUser);
  saveUsers(users);
  return true;
}

/**
 * Verify login credentials
 * @param {string} email - Email address
 * @param {string} password - Password
 * @returns {object|null} - User object if valid, null if not
 */
function verifyCredentials(email, password) {
  const user = findUserByEmail(email);
  
  if (!user) {
    return null; // Email not found
  }
  
  if (user.password !== password) {
    return null; // Password incorrect
  }
  
  return user; // Success
}

/**
 * Set current logged-in user
 * @param {object} user - User object to store
 */
function setCurrentUser(user) {
  const userToStore = {
    id: user.id,
    name: user.name,
    email: user.email,
    // Don't store password in current user
  };
  localStorage.setItem(CURRENT_USER_KEY, JSON.stringify(userToStore));
}

/**
 * Get current logged-in user
 * @returns {object|null} - Current user or null
 */
function getCurrentUser() {
  const user = localStorage.getItem(CURRENT_USER_KEY);
  return user ? JSON.parse(user) : null;
}

// ===== UI ERROR & SUCCESS MESSAGES =====
/**
 * Display error message in the form
 * @param {string} fieldId - ID of form field or 'general' for form-wide error
 * @param {string} message - Error message to display
 */
function showError(fieldId, message) {
  // Remove any existing error message
  removeError(fieldId);
  
  if (fieldId === 'general') {
    // Show general form error at top
    const activeForm = document.querySelector('form[style*="display: flex"], form:not([style*="display: none"])');
    if (!activeForm) return;
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'form-error general-error';
    errorDiv.setAttribute('role', 'alert');
    errorDiv.setAttribute('aria-live', 'polite');
    errorDiv.innerHTML = `
      <span class="error-icon">⚠️</span>
      <span class="error-text">${escapeHtml(message)}</span>
    `;
    
    activeForm.insertBefore(errorDiv, activeForm.firstChild);
  } else {
    // Show field-specific error
    const field = document.getElementById(fieldId);
    if (!field) return;
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'field-error';
    errorDiv.setAttribute('role', 'alert');
    errorDiv.setAttribute('aria-live', 'polite');
    errorDiv.textContent = message;
    
    field.parentElement.appendChild(errorDiv);
    field.setAttribute('aria-invalid', 'true');
    field.classList.add('input-error');
  }
}

/**
 * Remove error message from field
 * @param {string} fieldId - ID of field or 'general'
 */
function removeError(fieldId) {
  if (fieldId === 'general') {
    const error = document.querySelector('.general-error');
    if (error) error.remove();
  } else {
    const field = document.getElementById(fieldId);
    if (field) {
      const error = field.parentElement.querySelector('.field-error');
      if (error) error.remove();
      field.removeAttribute('aria-invalid');
      field.classList.remove('input-error');
    }
  }
}

/**
 * Show success message with animation
 * @param {string} message - Success message
 */
function showSuccess(message) {
  const notification = document.createElement('div');
  notification.className = 'success-notification';
  notification.setAttribute('role', 'status');
  notification.setAttribute('aria-live', 'polite');
  notification.innerHTML = `
    <span class="success-icon">✓</span>
    <span class="success-text">${escapeHtml(message)}</span>
  `;
  
  document.body.appendChild(notification);
  
  // Trigger animation
  setTimeout(() => {
    notification.classList.add('show');
  }, 10);
  
  // Remove after delay
  setTimeout(() => {
    notification.classList.remove('show');
    setTimeout(() => notification.remove(), 300);
  }, 2000);
}

/**
 * Show loading state on button
 * @param {HTMLElement} button - Button element
 * @param {boolean} isLoading - True to show loading, false to reset
 */
function setButtonLoading(button, isLoading) {
  if (isLoading) {
    button.disabled = true;
    button.classList.add('loading');
    button.innerHTML = '<span class="spinner"></span> Processing...';
  } else {
    button.disabled = false;
    button.classList.remove('loading');
    // Restore original text - needs to be done differently
    // For now, just reset based on the button's ID
    if (button.id === 'login-btn') {
      button.innerHTML = 'Login to Structify';
    } else if (button.id === 'signup-btn') {
      button.innerHTML = 'Create Account';
    }
  }
}

// ===== FORM VALIDATION & SUBMISSION =====
/**
 * Handle login form submission
 * @param {Event} event - Form submit event
 */
function handleLogin(event) {
  event.preventDefault();
  
  // Get form values
  const email = document.getElementById('login-email').value.trim();
  const password = document.getElementById('login-password').value;
  
  // Clear previous errors
  removeError('login-email');
  removeError('login-password');
  removeError('general');
  
  // Validate email
  if (!email) {
    showError('login-email', 'Email is required');
    return;
  }
  
  if (!isValidEmail(email)) {
    showError('login-email', 'Please enter a valid email address');
    return;
  }
  
  // Validate password
  if (!password) {
    showError('login-password', 'Password is required');
    return;
  }
  
  // Show loading state
  const loginBtn = event.target.querySelector('button[type="submit"]');
  setButtonLoading(loginBtn, true);
  
  // Simulate network delay for realism
  setTimeout(() => {
    // Verify credentials
    const user = verifyCredentials(email, password);
    
    if (!user) {
      setButtonLoading(loginBtn, false);
      showError('general', 'Invalid email or password. Try signing up if you\'re new.');
      return;
    }
    
    // Success - store user and redirect
    setCurrentUser(user);
    showSuccess(`Welcome back, ${user.name}!`);
    
    // Redirect after brief delay
    setTimeout(() => {
      window.location.href = 'chat.html';
    }, 800);
  }, 1200); // Simulate 1.2s network request
}

/**
 * Handle signup form submission
 * @param {Event} event - Form submit event
 */
function handleSignup(event) {
  event.preventDefault();
  
  // Get form values
  const name = document.getElementById('signup-name').value.trim();
  const email = document.getElementById('signup-email').value.trim();
  const password = document.getElementById('signup-password').value;
  const terms = document.getElementById('terms').checked;
  
  // Clear previous errors
  removeError('signup-name');
  removeError('signup-email');
  removeError('signup-password');
  removeError('general');
  
  // Validate name
  if (!name) {
    showError('signup-name', 'Full name is required');
    return;
  }
  
  if (name.length < 2) {
    showError('signup-name', 'Name must be at least 2 characters');
    return;
  }
  
  // Validate email
  if (!email) {
    showError('signup-email', 'Email is required');
    return;
  }
  
  if (!isValidEmail(email)) {
    showError('signup-email', 'Please enter a valid email address');
    return;
  }
  
  // Check if email already exists
  if (findUserByEmail(email)) {
    showError('signup-email', 'This email is already registered. Try logging in.');
    return;
  }
  
  // Validate password
  const passwordValidation = validatePassword(password);
  if (!passwordValidation.isValid) {
    showError('signup-password', passwordValidation.message);
    return;
  }
  
  // Check terms acceptance
  if (!terms) {
    showError('general', 'You must accept the Terms of Service and Privacy Policy');
    return;
  }
  
  // Show loading state
  const signupBtn = event.target.querySelector('button[type="submit"]');
  setButtonLoading(signupBtn, true);
  
  // Simulate network delay for realism
  setTimeout(() => {
    // Create new user
    const userCreated = createUser({ name, email, password });
    
    if (!userCreated) {
      setButtonLoading(signupBtn, false);
      showError('signup-email', 'This email is already registered');
      return;
    }
    
    // Success - get the created user and log them in
    const newUser = findUserByEmail(email);
    setCurrentUser(newUser);
    showSuccess(`Welcome to Structify, ${name}! 🎉`);
    
    // Redirect after brief delay
    setTimeout(() => {
      window.location.href = 'chat.html';
    }, 800);
  }, 1200); // Simulate 1.2s network request
}

// ===== TAB SWITCHING =====
/**
 * Switch between login and signup tabs
 * @param {string} tab - 'login' or 'signup'
 */
function switchTab(tab) {
  const loginPanel = document.getElementById('login-panel');
  const signupPanel = document.getElementById('signup-panel');
  const loginTab = document.getElementById('login-tab');
  const signupTab = document.getElementById('signup-tab');
  
  // Clear all errors when switching tabs
  removeError('login-email');
  removeError('login-password');
  removeError('signup-name');
  removeError('signup-email');
  removeError('signup-password');
  removeError('general');
  
  if (tab === 'login') {
    loginPanel.style.display = 'flex';
    signupPanel.style.display = 'none';
    loginTab.classList.add('active');
    signupTab.classList.remove('active');
    loginTab.setAttribute('aria-selected', 'true');
    signupTab.setAttribute('aria-selected', 'false');
  } else {
    loginPanel.style.display = 'none';
    signupPanel.style.display = 'flex';
    loginTab.classList.remove('active');
    signupTab.classList.add('active');
    loginTab.setAttribute('aria-selected', 'false');
    signupTab.setAttribute('aria-selected', 'true');
  }
}

// ===== UI INITIALIZATION =====
/**
 * Initialize auth UI elements and add event listeners
 */
function initializeAuthUI() {
  // Get button elements and add unique IDs for reference
  const loginBtn = document.querySelector('#login-panel button[type="submit"]');
  const signupBtn = document.querySelector('#signup-panel button[type="submit"]');
  
  if (loginBtn) loginBtn.id = 'login-btn';
  if (signupBtn) signupBtn.id = 'signup-btn';
  
  // Setup tab click listeners
  const loginTab = document.getElementById('login-tab');
  const signupTab = document.getElementById('signup-tab');
  
  if (loginTab) {
    loginTab.addEventListener('click', () => switchTab('login'));
  }
  
  if (signupTab) {
    signupTab.addEventListener('click', () => switchTab('signup'));
  }
  
  // Add input focus animations callback (CSS handles the visual part)
  const inputs = document.querySelectorAll('.form-group input');
  inputs.forEach(input => {
    input.addEventListener('focus', () => {
      input.parentElement.classList.add('focused');
    });
    
    input.addEventListener('blur', () => {
      input.parentElement.classList.remove('focused');
    });
    
    // Clear error on input change
    input.addEventListener('input', () => {
      const fieldId = input.id;
      if (document.getElementById(fieldId).hasAttribute('aria-invalid')) {
        removeError(fieldId);
      }
    });
  });
}

/**
 * Setup form listeners
 */
function setupFormListeners() {
  const loginPanel = document.getElementById('login-panel');
  const signupPanel = document.getElementById('signup-panel');
  
  // Setup login form submission
  if (loginPanel) {
    loginPanel.addEventListener('submit', handleLogin);
    
    // Allow Enter key to submit
    const loginInputs = loginPanel.querySelectorAll('input');
    loginInputs.forEach(input => {
      input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
          loginPanel.dispatchEvent(new Event('submit'));
        }
      });
    });
  }
  
  // Setup signup form submission
  if (signupPanel) {
    signupPanel.addEventListener('submit', handleSignup);
    
    // Allow Enter key to submit
    const signupInputs = signupPanel.querySelectorAll('input:not([type="checkbox"])');
    signupInputs.forEach(input => {
      input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
          signupPanel.dispatchEvent(new Event('submit'));
        }
      });
    });
  }
}

/**
 * Check if user is already logged in on page load
 */
function initializeStorageCheck() {
  const currentUser = getCurrentUser();
  
  // If user is already logged in, you could redirect them
  // Uncomment to add this behavior:
  // if (currentUser) {
  //   window.location.href = 'chat.html';
  // }
}

// ===== UTILITY FUNCTIONS =====
/**
 * Escape HTML special characters to prevent XSS
 * @param {string} text - Text to escape
 * @returns {string} - Escaped HTML
 */
function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

// ===== DEMO MODE SETUP =====
/**
 * Initialize with demo user for testing
 * Uncomment to enable demo mode
 */
function initializeDemoUser() {
  // Check if any users exist
  if (getAllUsers().length === 0) {
    // Create demo user
    createUser({
      name: 'Demo User',
      email: 'demo@structify.com',
      password: 'demo123'
    });
    console.log('Demo user created. Email: demo@structify.com, Password: demo123');
  }
}

// Uncomment to enable demo user on first load:
// initializeDemoUser();

// ===== CONSOLE LOG =====
console.log('%c✅ Structify Auth System Loaded', 'color: #3b82f6; font-size: 14px; font-weight: bold;');
if (getAllUsers().length > 0) {
  console.log(`Currently have ${getAllUsers().length} user(s) in localStorage`);
}
