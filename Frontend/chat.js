/**
 * =============================================================
 * STRUCTIFY CHAT SYSTEM
 * =============================================================
 * Handles chat interface interactions, message display,
 * sidebar navigation, user profile, and modal management.
 * 
 * Features:
 * - Send/receive messages with AI responses
 * - Sidebar toggle and navigation
 * - User profile management
 * - Settings and modal dialogs
 * - Message persistence with localStorage
 * - Responsive mobile interactions
 * =============================================================
 */

// ===== INITIALIZATION =====
/**
 * Initialize chat page when DOM is ready
 */
document.addEventListener('DOMContentLoaded', () => {
  checkUserAuthentication();
  initializeUserProfile();
  initializeChatInterface();
  initializeSidebarInteractions();
  initializeModals();
  loadChatHistory();
});

// ===== AUTHENTICATION CHECK =====
/**
 * Verify user is logged in, redirect if not
 */
function checkUserAuthentication() {
  const currentUser = localStorage.getItem('structify_current_user');
  
  if (!currentUser) {
    // User not logged in, redirect to login page
    window.location.href = 'login.html';
    return;
  }
}

// ===== USER PROFILE MANAGEMENT =====
/**
 * Initialize and display user profile information
 */
function initializeUserProfile() {
  const currentUser = JSON.parse(localStorage.getItem('structify_current_user'));
  
  if (!currentUser) return;
  
  // Update user name and email in sidebar
  const userNameDisplay = document.getElementById('userNameDisplay');
  if (userNameDisplay) {
    userNameDisplay.innerHTML = `
      <p class="user-name">${escapeHtml(currentUser.name)}</p>
      <p class="user-email">${escapeHtml(currentUser.email)}</p>
    `;
  }
}

/**
 * Handle user profile button click
 */
document.addEventListener('DOMContentLoaded', () => {
  const userProfileBtn = document.getElementById('userProfileBtn');
  const userMenu = document.getElementById('userMenu');
  
  if (userProfileBtn) {
    userProfileBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      const isVisible = userMenu.style.display !== 'none';
      userMenu.style.display = isVisible ? 'none' : 'flex';
      userProfileBtn.setAttribute('aria-expanded', !isVisible);
    });
  }
  
  // Close menu when clicking outside
  document.addEventListener('click', () => {
    if (userMenu) {
      userMenu.style.display = 'none';
      userProfileBtn?.setAttribute('aria-expanded', 'false');
    }
  });
});

// ===== LOGOUT HANDLER =====
/**
 * Handle logout process
 */
document.addEventListener('DOMContentLoaded', () => {
  const logoutBtn = document.getElementById('logoutBtn');
  const logoutConfirmModal = document.getElementById('logoutConfirmModal');
  const cancelLogoutBtn = document.getElementById('cancelLogoutBtn');
  const confirmLogoutBtn = document.getElementById('confirmLogoutBtn');
  
  if (logoutBtn) {
    logoutBtn.addEventListener('click', (e) => {
      e.preventDefault();
      showModal('logoutConfirmModal');
    });
  }
  
  if (confirmLogoutBtn) {
    confirmLogoutBtn.addEventListener('click', () => {
      // Clear user from localStorage
      localStorage.removeItem('structify_current_user');
      
      // Show success message
      showNotification('Logged out successfully', 'success');
      
      // Redirect to login page
      setTimeout(() => {
        window.location.href = 'login.html';
      }, 500);
    });
  }
  
  if (cancelLogoutBtn) {
    cancelLogoutBtn.addEventListener('click', () => {
      closeModal('logoutConfirmModal');
    });
  }
});

// ===== CHAT INTERFACE =====
/**
 * Initialize chat message sending and display
 */
function initializeChatInterface() {
  const userInput = document.getElementById('userInput');
  const sendBtn = document.getElementById('sendBtn');
  const chatMessages = document.getElementById('chatMessages');
  
  // Handle Enter key to send message
  if (userInput) {
    userInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
      }
    });
    
    // Auto-grow textarea
    userInput.addEventListener('input', () => {
      userInput.style.height = 'auto';
      userInput.style.height = Math.min(userInput.scrollHeight, 150) + 'px';
    });
  }
  
  // Send button click
  if (sendBtn) {
    sendBtn.addEventListener('click', sendMessage);
  }
}

/**
 * Send user message and get AI response
 */
function sendMessage() {
  const input = document.getElementById('userInput');
  const chatMessages = document.getElementById('chatMessages');
  const suggestionsContainer = document.getElementById('suggestionsContainer');
  
  if (!input || !chatMessages) return;
  
  const text = input.value.trim();
  if (!text) return;
  
  // Hide suggestions after first message
  if (suggestionsContainer) {
    suggestionsContainer.style.display = 'none';
  }
  
  // Add user message to chat
  const userMessageGroup = document.createElement('div');
  userMessageGroup.className = 'message-group user-message';
  userMessageGroup.innerHTML = `
    <div class="message-bubble user">
      <p>${escapeHtml(text)}</p>
    </div>
    <div class="message-avatar" aria-hidden="true">👤</div>
  `;
  chatMessages.appendChild(userMessageGroup);
  
  // Clear input
  input.value = '';
  input.style.height = 'auto';
  
  // Scroll to bottom
  chatMessages.scrollTop = chatMessages.scrollHeight;
  
  // Show typing indicator
  const typingIndicator = document.createElement('div');
  typingIndicator.className = 'message-group ai-message';
  typingIndicator.innerHTML = `
    <div class="message-avatar" aria-hidden="true">🤖</div>
    <div class="message-bubble ai">
      <div class="typing-indicator">
        <span class="dot"></span>
        <span class="dot"></span>
        <span class="dot"></span>
      </div>
    </div>
  `;
  chatMessages.appendChild(typingIndicator);
  chatMessages.scrollTop = chatMessages.scrollHeight;
  
  // Simulate AI response after delay
  setTimeout(() => {
    typingIndicator.remove();
    
    // Generate AI response based on input
    const aiResponse = generateAIResponse(text);
    
    const aiMessageGroup = document.createElement('div');
    aiMessageGroup.className = 'message-group ai-message';
    aiMessageGroup.innerHTML = `
      <div class="message-avatar" aria-hidden="true">🤖</div>
      <div class="message-bubble ai">
        ${aiResponse}
      </div>
    `;
    chatMessages.appendChild(aiMessageGroup);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    // Save chat history
    saveChatMessage({
      type: 'user',
      text: text,
      timestamp: new Date().toISOString()
    });
    saveChatMessage({
      type: 'ai',
      html: aiResponse,
      timestamp: new Date().toISOString()
    });
  }, 1500); // Simulate network delay
}

/**
 * Generate AI response based on user input
 * @param {string} userText - User's message
 * @returns {string} - HTML formatted AI response
 */
function generateAIResponse(userText) {
  // Analyze user input and generate contextual response
  const lowerText = userText.toLowerCase();
  
  let response = '';
  
  if (lowerText.includes('saas') || lowerText.includes('startup') || lowerText.includes('app')) {
    response = `
      <p><strong>Great idea! 💡</strong></p>
      <p>I'm analyzing your concept: <em>"${escapeHtml(userText.substring(0, 60))}${userText.length > 60 ? '...' : ''}"</em></p>
      <p style="margin-top: 12px;"><strong>Here's what I'm structuring:</strong></p>
      <ul class="response-list">
        <li><strong>Core Problem:</strong> Identified key pain points to solve</li>
        <li><strong>Target Market:</strong> Primary and secondary user personas</li>
        <li><strong>MVP Features:</strong> Essential feature set for launch</li>
        <li><strong>Tech Stack:</strong> Recommended architecture and tools</li>
        <li><strong>Timeline:</strong> 3-6 month development roadmap</li>
        <li><strong>Business Model:</strong> Revenue streams and pricing strategy</li>
      </ul>
      <p style="margin-top: 12px; padding: 12px; background: rgba(59, 130, 246, 0.1); border-radius: 8px;">
        <strong>📄 Your BRD is being generated!</strong> You can download it once we've refined all sections.
      </p>
    `;
  } else if (lowerText.includes('features') || lowerText.includes('requirements')) {
    response = `
      <p><strong>Feature Analysis 🎯</strong></p>
      <p>Based on your input, here are the recommended features:</p>
      <ul class="response-list">
        <li><strong>User Authentication:</strong> Secure login and registration system</li>
        <li><strong>Dashboard:</strong> Central hub for user activities and insights</li>
        <li><strong>Core Functionality:</strong> Main feature set tailored to your use case</li>
        <li><strong>Integration:</strong> Third-party API connections and webhooks</li>
        <li><strong>Analytics:</strong> User behavior tracking and reporting</li>
        <li><strong>Support:</strong> Help desk and customer support system</li>
      </ul>
      <p style="margin-top: 12px;">Would you like me to dive deeper into any specific feature?</p>
    `;
  } else if (lowerText.includes('help') || lowerText.includes('how')) {
    response = `
      <p><strong>How Structify Works 🚀</strong></p>
      <ol class="response-list">
        <li><strong>Describe Your Idea:</strong> Tell me about your startup or project</li>
        <li><strong>AI Analysis:</strong> I'll structure your idea into professional requirements</li>
        <li><strong>Refine Details:</strong> We can iterate and improve specific sections</li>
        <li><strong>Generate Document:</strong> Export a polished BRD in PDF or Word format</li>
        <li><strong>Share & Collaborate:</strong> Share with your team for feedback</li>
      </ol>
      <p style="margin-top: 12px; padding: 12px; background: rgba(16, 185, 129, 0.1); border-radius: 8px;">
        <strong>💡 Pro Tip:</strong> Be specific about your target users and key problems you're solving for best results!
      </p>
    `;
  } else {
    response = `
      <p><strong>Thanks for sharing! 💬</strong></p>
      <p>I'm processing your idea: <em>"${escapeHtml(userText.substring(0, 50))}${userText.length > 50 ? '...' : ''}"</em></p>
      <p style="margin-top: 12px;">Tell me more about:</p>
      <ul class="response-list">
        <li>What problem does your idea solve?</li>
        <li>Who are your target users?</li>
        <li>What are the core features?</li>
        <li>What's your business model?</li>
      </ul>
      <p style="margin-top: 12px;">The more details you provide, the better I can structure your BRD! 📝</p>
    `;
  }
  
  return response;
}

/**
 * Fill input with suggestion and send
 */
function fillSuggestion(suggestion) {
  const input = document.getElementById('userInput');
  if (!input) return;
  
  input.value = suggestion;
  input.style.height = 'auto';
  input.style.height = input.scrollHeight + 'px';
  input.focus();
  
  // Automatically send after a short delay
  setTimeout(() => sendMessage(), 300);
}

// ===== SIDEBAR INTERACTIONS =====
/**
 * Initialize sidebar toggle and interactions
 */
function initializeSidebarInteractions() {
  const sidebar = document.querySelector('.sidebar');
  const sidebarToggle = document.getElementById('sidebarToggle');
  const mobileSidebarToggle = document.getElementById('mobileSidebarToggle');
  const newChatBtn = document.getElementById('newChatBtn');
  
  // Toggle sidebar visibility
  if (sidebarToggle) {
    sidebarToggle.addEventListener('click', () => {
      sidebar?.classList.toggle('collapsed');
      sidebarToggle.setAttribute('aria-expanded', 
        sidebar?.classList.contains('collapsed') ? 'false' : 'true');
    });
  }
  
  // Mobile sidebar toggle
  if (mobileSidebarToggle) {
    mobileSidebarToggle.addEventListener('click', () => {
      sidebar?.classList.toggle('mobile-open');
    });
  }
  
  // New chat button
  if (newChatBtn) {
    newChatBtn.addEventListener('click', () => {
      const chatMessages = document.getElementById('chatMessages');
      
      // Clear messages
      if (chatMessages) {
        chatMessages.innerHTML = `
          <div class="message-group ai-message">
            <div class="message-avatar" aria-hidden="true">🤖</div>
            <div class="message-bubble ai">
              <p><strong>New Chat Started! 🆕</strong></p>
              <p>This is a fresh conversation. Tell me about your next project idea!</p>
            </div>
          </div>
          <div class="suggestions-container" id="suggestionsContainer">
            <p class="suggestions-label">Try asking about:</p>
            <div class="suggestions-grid">
              <button class="suggestion-pill" onclick="fillSuggestion('I need help building a project management SaaS tool')">
                💼 Project Management SaaS
              </button>
              <button class="suggestion-pill" onclick="fillSuggestion('I want to create an AI-powered content writing tool')">
                ✍️ AI Content Tool
              </button>
              <button class="suggestion-pill" onclick="fillSuggestion('Help me structure a mobile fitness app idea')">
                🏃 Fitness App
              </button>
              <button class="suggestion-pill" onclick="fillSuggestion('I need requirements for an e-commerce marketplace')">
                🛒 E-commerce Platform
              </button>
            </div>
          </div>
        `;
      }
      
      // Clear input
      const userInput = document.getElementById('userInput');
      if (userInput) {
        userInput.value = '';
        userInput.style.height = 'auto';
      }
      
      // Close sidebar on mobile
      if (window.innerWidth < 768) {
        sidebar?.classList.remove('mobile-open');
      }
    });
  }
  
  // Close mobile sidebar when clicking chat area
  const chatPanel = document.querySelector('.chat-panel');
  if (chatPanel && window.innerWidth < 768) {
    chatPanel.addEventListener('click', () => {
      sidebar?.classList.remove('mobile-open');
    });
  }
  
  // History items
  const historyItems = document.querySelectorAll('.history-item');
  historyItems.forEach(item => {
    item.addEventListener('click', (e) => {
      e.preventDefault();
      
      // Update active state
      historyItems.forEach(h => h.classList.remove('active'));
      item.classList.add('active');
      
      // Load chat history (in production, this would load from server)
      loadChatHistory();
      
      // Close mobile sidebar
      if (window.innerWidth < 768) {
        sidebar?.classList.remove('mobile-open');
      }
    });
  });
}

// ===== MODAL MANAGEMENT =====
/**
 * Initialize all modal interactions
 */
function initializeModals() {
  // Setup button event listeners for modals
  document.getElementById('settingsBtn')?.addEventListener('click', (e) => {
    e.preventDefault();
    showModal('settingsModal');
  });
  
  document.getElementById('shareBtn')?.addEventListener('click', () => {
    showModal('shareModal');
    initializeShareLink();
  });
  
  document.getElementById('downloadBtn')?.addEventListener('click', () => {
    downloadBRD();
  });
  
  // Close modal buttons
  document.querySelectorAll('.modal-close').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const modal = e.target.closest('.modal');
      if (modal) {
        closeModal(modal.id);
      }
    });
  });
  
  // Close modal when clicking outside
  document.querySelectorAll('.modal').forEach(modal => {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        closeModal(modal.id);
      }
    });
  });
  
  // Copy link button
  document.getElementById('copyLinkBtn')?.addEventListener('click', () => {
    const shareLink = document.getElementById('shareLink');
    if (shareLink) {
      shareLink.select();
      document.execCommand('copy');
      showNotification('Link copied to clipboard!', 'success');
    }
  });
  
  // Settings interactions
  document.getElementById('helpBtn')?.addEventListener('click', (e) => {
    e.preventDefault();
    showNotification('Help documentation coming soon!', 'info');
  });
  
  document.getElementById('feedbackBtn')?.addEventListener('click', (e) => {
    e.preventDefault();
    showNotification('Feedback form coming soon!', 'info');
  });
  
  document.getElementById('profileBtn')?.addEventListener('click', (e) => {
    e.preventDefault();
    showNotification('Profile settings coming soon!', 'info');
  });
  
  document.getElementById('accountBtn')?.addEventListener('click', (e) => {
    e.preventDefault();
    showNotification('Account settings coming soon!', 'info');
  });
  
  document.getElementById('infoBtn')?.addEventListener('click', (e) => {
    e.preventDefault();
    showNotification('Chat info: You have 1 active conversation', 'info');
  });
}

/**
 * Show modal dialog
 * @param {string} modalId - ID of modal to show
 */
function showModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.style.display = 'flex';
    modal.setAttribute('aria-hidden', 'false');
    // Prevent body scroll
    document.body.style.overflow = 'hidden';
  }
}

/**
 * Close modal dialog
 * @param {string} modalId - ID of modal to close
 */
function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.style.display = 'none';
    modal.setAttribute('aria-hidden', 'true');
    // Restore body scroll
    document.body.style.overflow = 'auto';
  }
}

// ===== SHARE FUNCTIONALITY =====
/**
 * Initialize share link for current chat
 */
function initializeShareLink() {
  const shareLink = document.getElementById('shareLink');
  if (shareLink) {
    // In production, this would generate a unique shareable link
    const chatId = 'structify-chat-' + Date.now();
    shareLink.value = `${window.location.origin}/chat.html?shared=${chatId}`;
  }
}

/**
 * Download BRD document
 */
function downloadBRD() {
  showNotification('Generating BRD document...', 'info');
  
  // Simulate document generation
  setTimeout(() => {
    // In production, this would generate an actual PDF/Word document
    const element = document.createElement('a');
    const file = new Blob(['BRD Document - Structify\n\nGenerated on ' + new Date().toLocaleString()], 
      {type: 'text/plain'});
    element.href = URL.createObjectURL(file);
    element.download = 'Structify_BRD_' + Date.now() + '.txt';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
    
    showNotification('BRD document downloaded!', 'success');
  }, 1000);
}

// ===== CHAT HISTORY PERSISTENCE =====
/**
 * Save individual chat message to localStorage
 * @param {object} message - Message object with type, text/html, and timestamp
 */
function saveChatMessage(message) {
  const chatHistory = JSON.parse(localStorage.getItem('structify_chat_history') || '[]');
  chatHistory.push(message);
  localStorage.setItem('structify_chat_history', JSON.stringify(chatHistory));
}

/**
 * Load chat history from localStorage
 */
function loadChatHistory() {
  const chatHistory = JSON.parse(localStorage.getItem('structify_chat_history') || '[]');
  
  // In this demo, we're not reloading history on page load
  // In production, this would display saved messages
  
  console.log(`Chat history loaded: ${chatHistory.length} messages`);
}

// ===== NOTIFICATIONS =====
/**
 * Show notification/toast message
 * @param {string} message - Message to display
 * @param {string} type - 'success', 'error', or 'info'
 */
function showNotification(message, type = 'info') {
  const notification = document.createElement('div');
  notification.className = `notification notification-${type}`;
  notification.setAttribute('role', 'status');
  notification.setAttribute('aria-live', 'polite');
  
  const icons = {
    success: '✓',
    error: '✕',
    info: 'ℹ'
  };
  
  notification.innerHTML = `
    <span class="notification-icon">${icons[type]}</span>
    <span class="notification-text">${escapeHtml(message)}</span>
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
  }, 3000);
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

// ===== RESPONSIVE HANDLING =====
/**
 * Handle window resize for responsive behavior
 */
window.addEventListener('resize', () => {
  const sidebar = document.querySelector('.sidebar');
  
  // Close mobile sidebar on desktop resize
  if (window.innerWidth >= 768 && sidebar) {
    sidebar.classList.remove('mobile-open');
  }
});

// ===== CONSOLE LOG =====
console.log('%c✅ Structify Chat System Loaded', 'color: #3b82f6; font-size: 14px; font-weight: bold;');
console.log('Chat interface initialized and ready to use!');
