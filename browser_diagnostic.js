/**
 * BROWSER DIAGNOSTIC SCRIPT
 * Copy and paste this into your browser console (F12 > Console tab)
 * This will show what's going wrong
 */

console.log('============================================');
console.log('STRUCTIFY BROWSER DIAGNOSTIC');
console.log('============================================');
console.log('');

// Check 1: API_CONFIG loaded?
console.log('[1] API_CONFIG Check');
console.log('-'.repeat(40));
if (typeof API_CONFIG !== 'undefined') {
    console.log('✅ API_CONFIG loaded');
    console.log('   BACKEND_URL:', API_CONFIG.BACKEND_URL);
    console.log('   TIMEOUT:', API_CONFIG.TIMEOUT);
} else {
    console.log('❌ API_CONFIG NOT loaded - config.js not loaded!');
}
console.log('');

// Check 2: Page elements exist?
console.log('[2] DOM Elements Check');
console.log('-'.repeat(40));
const elements = {
    'userInput': document.getElementById('userInput'),
    'sendBtn': document.getElementById('sendBtn'),
    'chatMessages': document.getElementById('chatMessages'),
    'suggestionsContainer': document.getElementById('suggestionsContainer'),
    'brdModal': document.getElementById('brdModal')
};

for (const [name, elem] of Object.entries(elements)) {
    if (elem) {
        console.log(`✅ ${name}: Found`);
    } else {
        console.log(`❌ ${name}: NOT FOUND`);
    }
}
console.log('');

// Check 3: Functions defined?
console.log('[3] JavaScript Functions Check');
console.log('-'.repeat(40));
const functions = [
    'sendMessage',
    'analyzeWithBackend',
    'getBackendUrl',
    'fetchWithRetry',
    'openBrdModal',
    'generateBrd'
];

for (const func of functions) {
    if (typeof window[func] === 'function') {
        console.log(`✅ ${func}: Defined`);
    } else {
        console.log(`❌ ${func}: NOT DEFINED`);
    }
}
console.log('');

// Check 4: App state?
console.log('[4] Application State');
console.log('-'.repeat(40));
if (typeof analysisState !== 'undefined') {
    console.log('✅ analysisState exists');
    console.log('   Stage:', analysisState.stage);
    console.log('   Idea:', analysisState.idea);
    console.log('   Has API response:', !!analysisState.analysisResponse);
} else {
    console.log('❌ analysisState NOT defined');
}
console.log('');

// Check 5: Test backend connection
console.log('[5] Backend Connection Test');
console.log('-'.repeat(40));
const backendUrl = (typeof API_CONFIG !== 'undefined') ? API_CONFIG.BACKEND_URL : 'http://127.0.0.1:8001';
console.log('Testing:', backendUrl);

fetch(backendUrl + '/', {method: 'GET'})
    .then(r => {
        console.log(`✅ Backend responding: Status ${r.status}`);
        return r.json();
    })
    .then(data => {
        console.log('   Message:', data.message);
        console.log('   Timestamp:', data.timestamp);
    })
    .catch(err => {
        console.log(`❌ Backend connection failed: ${err.message}`);
    });

console.log('');
console.log('============================================');
console.log('COPY THIS OUTPUT AND SEND TO DEVELOPER');
console.log('============================================');
