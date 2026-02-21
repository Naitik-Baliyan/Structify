/**
 * =============================================================
 * STRUCTIFY AUTHENTICATION SYSTEM - IMPROVED VERSION
 * =============================================================
 * Handles login/signup validation, localStorage mock database,
 * and smooth user interactions with professional error handling.
 * 
 * Features:
 * - Email & password validation with defensive checks
 * - localStorage-based user storage with write verification
 * - Smooth animations for errors and success
 * - Tab switching between login/signup
 * - XSS prevention with HTML escaping
 * - Reliable event listeners with fallback mechanisms
 * - Production-ready signup flow
 * =============================================================
 */

// ===== INITIALIZATION =====
/**
 * Run setup code when DOM is ready
 */
document.addEventListener('DOMContentLoaded', () => {
  console.log('%c[Auth] Initializing...', 'color: #3b82f6; font-weight: bold;');
  initializeAuthUI();
  setupFormListeners();
  setupDirectButtonListeners();
  initializeStorageCheck();
  console.log('%c[Auth] Initialization complete', 'color: #10b981; font-weight: bold;');
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
 * Save users array to localStorage with verification
 * @param {Array} users - Array of user objects to save
 * @returns {boolean} - True if save was successful
 */
function saveUsers(users) {
  try {
    const jsonString = JSON.stringify(users);
    localStorage.setItem(USERS_STORAGE_KEY, jsonString);
    
    // Verify the write was successful
    const verification = localStorage.getItem(USERS_STORAGE_KEY);
    if (!verification) {
      console.error('localStorage write verification failed');
      return false;
    }
    
    return true;
  } catch (error) {
    console.error('localStorage save error:', error);
    return false;
  }
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
 * @returns {object} - { success: boolean, message: string, user: object|null }
 */
function createUser(userData) {
  try {
    // Validate input exists
    if (!userData || !userData.name || !userData.email || !userData.password) {
      return { success: false, message: 'Missing user data', user: null };
    }

    const users = getAllUsers();
    
    // Check if email already exists
    if (findUserByEmail(userData.email)) {
      return { success: false, message: 'Email already registered', user: null };
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
    
    // Save to localStorage and verify
    const saveSuccess = saveUsers(users);
    if (!saveSuccess) {
      return { success: false, message: 'Failed to save user data', user: null };
    }
    
    return { success: true, message: 'User created successfully', user: newUser };
  } catch (error) {
    console.error('createUser error:', error);
    return { success: false, message: 'Error creating user account', user: null };
  }
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
 * Set current logged-in user with verification
 * @param {object} user - User object to store
 * @returns {boolean} - True if successfully stored
 */
function setCurrentUser(user) {
  try {
    const userToStore = {
      id: user.id,
      name: user.name,
      email: user.email,
      // Don't store password in current user
    };
    localStorage.setItem(CURRENT_USER_KEY, JSON.stringify(userToStore));
    
    // Verify the write was successful
    const verification = localStorage.getItem(CURRENT_USER_KEY);
    if (!verification) {
      console.error('Current user storage verification failed');
      return false;
    }
    
    return true;
  } catch (error) {
    console.error('setCurrentUser error:', error);
    return false;
  }
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
 * Show loading state on button with spinner animation
 * @param {HTMLElement} button - Button element
 * @param {boolean} isLoading - True to show loading, false to reset
 */
function setButtonLoading(button, isLoading) {
  if (!button) return;
  
  try {
    if (isLoading) {
      // Store original text if not already stored
      if (!button.dataset.originalText) {
        button.dataset.originalText = button.textContent.trim();
      }
      
      button.disabled = true;
      button.classList.add('loading');
      button.innerHTML = '<span class="spinner"></span> Processing...';
    } else {
      button.disabled = false;
      button.classList.remove('loading');
      
      // Restore original text from data attribute
      const originalText = button.dataset.originalText || 'Create Account';
      button.textContent = originalText;
    }
  } catch (error) {
    console.error('setButtonLoading error:', error);
  }
}

// ===== FORM VALIDATION & SUBMISSION =====
/**
 * Handle login form submission
 * @param {Event} event - Form submit event
 */
function handleLogin(event) {
  console.log('%c[Auth] handleLogin called', 'color: #8b5cf6;');
  
  event.preventDefault();
  
  // Get form values
  const email = document.getElementById('login-email').value.trim();
  const password = document.getElementById('login-password').value;
  
  console.log('%c[Auth] Login form values:', 'color: #8b5cf6;', { email });
  
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
    
    console.log('%c[Auth] Login successful, redirecting...', 'color: #10b981;');
    
    // Redirect after brief delay
    setTimeout(() => {
      window.location.href = 'chat.html';
    }, 800);
  }, 1200); // Simulate 1.2s network request
}

/**
 * Handle signup form submission with strong defensive checks
 * @param {Event} event - Form submit event
 */
function handleSignup(event) {
  console.log('%c[Auth] handleSignup called', 'color: #8b5cf6;');
  
  // Defensive check: ensure event exists
  if (!event) return;
  
  event.preventDefault();
  event.stopPropagation();
  
  try {
    // Get form values with defensive checks
    const nameInput = document.getElementById('signup-name');
    const emailInput = document.getElementById('signup-email');
    const passwordInput = document.getElementById('signup-password');
    const termsCheckbox = document.getElementById('terms');
    
    if (!nameInput || !emailInput || !passwordInput || !termsCheckbox) {
      console.error('Form inputs not found');
      showError('general', 'Form validation error. Please refresh and try again.');
      return;
    }
    
    const name = nameInput.value.trim();
    const email = emailInput.value.trim();
    const password = passwordInput.value;
    const terms = termsCheckbox.checked;
    
    console.log('%c[Auth] Signup form values:', 'color: #8b5cf6;', { name, email, termsChecked: terms });
    
    // Validate empty fields first
    if (!name || !email || !password) {
      if (!name) showError('signup-name', 'Full name is required');
      if (!email) showError('signup-email', 'Email is required');
      if (!password) showError('signup-password', 'Password is required');
      return;
    }
    
    // Clear previous errors
    removeError('signup-name');
    removeError('signup-email');
    removeError('signup-password');
    removeError('general');
    
    // Validate name
    if (name.length < 2) {
      showError('signup-name', 'Name must be at least 2 characters');
      return;
    }
    
    // Validate email
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
    
    console.log('%c[Auth] All validations passed, proceeding with signup', 'color: #10b981;');
    
    // All validations passed - proceed with signup
    performSignup(name, email, password);
    
  } catch (error) {
    console.error('handleSignup error:', error);
    showError('general', 'An error occurred. Please try again.');
  }
}

/**
 * Execute signup process with loading state and smooth redirect
 * @param {string} name - User's full name
 * @param {string} email - User's email
 * @param {string} password - User's password
 */
function performSignup(name, email, password) {
  console.log('%c[Auth] performSignup started', 'color: #8b5cf6;');
  
  try {
    // Get the signup button
    const signupBtn = document.getElementById('signup-btn');
    if (!signupBtn) {
      console.error('Signup button not found');
      showError('general', 'Form error. Please refresh and try again.');
      return;
    }
    
    // Save original button text
    const originalText = 'Create Account';
    
    // Show loading state
    setButtonLoading(signupBtn, true);
    
    // Simulate network delay for realistic UX
    setTimeout(() => {
      try {
        console.log('%c[Auth] Creating user...', 'color: #f59e0b;');
        
        // Create new user
        const result = createUser({ name, email, password });
        
        if (!result.success) {
          console.error('User creation failed:', result.message);
          setButtonLoading(signupBtn, false);
          showError('general', result.message || 'Failed to create account. Please try again.');
          return;
        }
        
        console.log('%c[Auth] User created successfully', 'color: #10b981;');
        
        // Get the created user
        const newUser = findUserByEmail(email);
        if (!newUser) {
          console.error('User verification failed');
          setButtonLoading(signupBtn, false);
          showError('general', 'User creation verification failed. Please try again.');
          return;
        }
        
        console.log('%c[Auth] Storing current user...', 'color: #f59e0b;');
        
        // Attempt to store current user
        const storageSuccess = setCurrentUser(newUser);
        if (!storageSuccess) {
          console.error('Session storage failed');
          setButtonLoading(signupBtn, false);
          showError('general', 'Failed to store session. Please try again.');
          return;
        }
        
        console.log('%c[Auth] Session stored successfully', 'color: #10b981;');
        
        // All checks passed - show success animation
        showSuccess(`Welcome to Structify, ${name}! 🎉`);
        
        // Disable form while redirecting
        const signupForm = document.getElementById('signup-panel');
        if (signupForm) {
          signupForm.style.opacity = '0.7';
          const inputs = signupForm.querySelectorAll('input, button');
          inputs.forEach(input => input.disabled = true);
        }
        
        // Smooth redirect after animation
        setTimeout(() => {
          // Final verification before redirect
          const currentUser = getCurrentUser();
          if (currentUser && currentUser.email === email) {
            console.log('%c[Auth] Redirecting to chat.html', 'color: #10b981; font-weight: bold;');
            window.location.href = 'chat.html';
          } else {
            console.error('Session verification failed before redirect');
            setButtonLoading(signupBtn, false);
            showError('general', 'Session verification failed. Please try again.');
          }
        }, 800);
        
      } catch (error) {
        console.error('performSignup timeout error:', error);
        setButtonLoading(signupBtn, false);
        showError('general', 'An error occurred during signup. Please try again.');
      }
    }, 1200); // Simulate 1.2s network request
  } catch (error) {
    console.error('performSignup outer error:', error);
    showError('general', 'An unexpected error occurred. Please try again.');
  }
}

// ===== TAB SWITCHING =====
/**
 * Switch between login and signup tabs
 * @param {string} tab - 'login' or 'signup'
 */
function switchTab(tab) {
  console.log('%c[Auth] Switching to tab:', 'color: #06b6d4;', tab);
  
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
    console.log('%c[Auth] Showing login panel', 'color: #06b6d4;');
    loginPanel.style.display = 'flex';
    signupPanel.style.display = 'none';
    loginTab.classList.add('active');
    signupTab.classList.remove('active');
    loginTab.setAttribute('aria-selected', 'true');
    signupTab.setAttribute('aria-selected', 'false');
  } else {
    console.log('%c[Auth] Showing signup panel', 'color: #06b6d4;');
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
 * Setup form listeners with error handling
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
  } else {
    console.warn('Login panel not found');
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
  } else {
    console.warn('Signup panel not found');
  }
}

/**
 * Setup direct button event listeners as fallback mechanism
 * Ensures signup button works reliably even if form submission has issues
 */
function setupDirectButtonListeners() {
  const signupBtn = document.getElementById('signup-btn');
  const loginBtn = document.getElementById('login-btn');
  
  // Direct signup button listener (fallback)
  if (signupBtn) {
    console.log('%c[Auth] Signup button found, attaching click listener', 'color: #10b981;');
    signupBtn.addEventListener('click', (e) => {
      console.log('%c[Auth] Signup button clicked!', 'color: #f59e0b; font-weight: bold;');
      e.preventDefault();
      e.stopPropagation();
      
      const signupForm = document.getElementById('signup-panel');
      if (signupForm) {
        console.log('%c[Auth] Dispatching form submit event', 'color: #f59e0b;');
        // Trigger form submission
        const submitEvent = new Event('submit', { bubbles: true, cancelable: true });
        signupForm.dispatchEvent(submitEvent);
      }
    });
  } else {
    console.warn('%c[Auth] Signup button NOT found!', 'color: #ef4444; font-weight: bold;');
  }
  
  // Direct login button listener (fallback)
  if (loginBtn) {
    console.log('%c[Auth] Login button found, attaching click listener', 'color: #10b981;');
    loginBtn.addEventListener('click', (e) => {
      console.log('%c[Auth] Login button clicked!', 'color: #f59e0b; font-weight: bold;');
      e.preventDefault();
      e.stopPropagation();
      
      const loginForm = document.getElementById('login-panel');
      if (loginForm) {
        console.log('%c[Auth] Dispatching login form submit event', 'color: #f59e0b;');
        // Trigger form submission
        const submitEvent = new Event('submit', { bubbles: true, cancelable: true });
        loginForm.dispatchEvent(submitEvent);
      }
    });
  } else {
    console.warn('%c[Auth] Login button NOT found!', 'color: #ef4444; font-weight: bold;');
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
