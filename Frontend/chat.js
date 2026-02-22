/* ============================================================
   STRUCTIFY CHAT SYSTEM - CLEAN REBUILD VERSION
   ============================================================ */

console.log('%c[chat.js] Script loaded successfully', 'color: #10b981; font-weight: bold; font-size: 14px;');

function getBackendUrl() {
    const url = (typeof API_CONFIG !== 'undefined' && API_CONFIG.BACKEND_URL) ? API_CONFIG.BACKEND_URL : 'http://127.0.0.1:8000';
    console.log('[chat.js] Backend URL:', url);
    return url;
}

/* =============================
   AUTH CHECK
============================= */

function checkUserAuthentication() {
    const user = localStorage.getItem("structify_current_user");
    // For development, allow access without login
    if (!user) {
        console.log('[Auth] No user found, setting dev user');
        localStorage.setItem("structify_current_user", JSON.stringify({
            name: "Dev User",
            email: "dev@structify.local"
        }));
    } else {
        console.log('[Auth] User found:', JSON.parse(user).name);
    }
}

/* =============================
   CHAT STATE
============================= */

const analysisState = {
    idea: null,
    target_market: null,
    problem_statement: null,
    stage: "collect_idea",
    analysisResponse: null  // Store the full analysis response
};

/* =============================
   ESCAPE HTML
============================= */

function escapeHtml(text) {
    if (!text) return "";
    return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");
}

/* =============================
   INITIALIZATION
============================= */

// Single consolidated DOMContentLoaded - prevents listener duplication
let chatInitialized = false;

document.addEventListener("DOMContentLoaded", () => {
    if (chatInitialized) {
        console.warn('[DOMContentLoaded] Already initialized, skipping');
        return;
    }
    
    console.log('[DOMContentLoaded] Firing - initializing chat interface');
    chatInitialized = true;
    
    checkUserAuthentication();
    initializeChatInterface();
    setupBRDModalListeners();
    
    console.log('[DOMContentLoaded] Initialization complete');
});

let brdModalListenersInitialized = false;

function setupBRDModalListeners() {
    if (brdModalListenersInitialized) {
        console.warn('[setupBRDModalListeners] Already initialized, skipping');
        return;
    }
    
    console.log('[setupBRDModalListeners] Starting setup...');
    brdModalListenersInitialized = true;
    
    const brdModal = document.getElementById("brdModal");
    const brdCloseBtn = brdModal?.querySelector(".modal-close");
    const brdCancelBtn = document.getElementById("cancelBrdBtn");
    const brdGenerateBtn = document.getElementById("generateBrdBtn");

    if (brdCloseBtn) {
        brdCloseBtn.addEventListener("click", closeBrdModal);
        console.log('[setupBRDModalListeners] Close button listener attached');
    }
    if (brdCancelBtn) {
        brdCancelBtn.addEventListener("click", closeBrdModal);
        console.log('[setupBRDModalListeners] Cancel button listener attached');
    }
    if (brdGenerateBtn) {
        brdGenerateBtn.addEventListener("click", generateBrd);
        console.log('[setupBRDModalListeners] Generate button listener attached');
    }

    if (brdModal) {
        brdModal.addEventListener("click", (e) => {
            if (e.target === brdModal) {
                console.log('[setupBRDModalListeners] Modal background clicked, closing');
                closeBrdModal();
            }
        });
        console.log('[setupBRDModalListeners] Modal background listener attached');
    } else {
        console.warn('[setupBRDModalListeners] BRD modal element NOT FOUND');
    }
    
    console.log('[setupBRDModalListeners] Setup complete');
}

/* =============================
   CHAT INTERFACE
============================= */

function initializeChatInterface() {
    console.log('[initializeChatInterface] Starting initialization...');

    const userInput = document.getElementById("userInput");
    const sendBtn = document.getElementById("sendBtn");

    if (!userInput) {
        console.error('[initializeChatInterface] userInput element NOT FOUND');
    } else {
        console.log('[initializeChatInterface] userInput element found');
        userInput.addEventListener("keydown", e => {
            if (e.key === "Enter" && !e.shiftKey) {
                console.log('[initializeChatInterface] Enter key pressed, calling sendMessage()');
                e.preventDefault();
                sendMessage();
            }
        });
        console.log('[initializeChatInterface] Enter key listener attached to userInput');
    }

    if (!sendBtn) {
        console.error('[initializeChatInterface] sendBtn element NOT FOUND');
    } else {
        console.log('[initializeChatInterface] sendBtn element found');
        sendBtn.addEventListener("click", () => {
            console.log('[initializeChatInterface] Send button clicked, calling sendMessage()');
            sendMessage();
        });
        console.log('[initializeChatInterface] Click listener attached to sendBtn');
    }
    
    console.log('[initializeChatInterface] Initialization complete');
}

/* =============================
   MESSAGE SYSTEM
============================= */

let isSending = false;

async function sendMessage() {
    if (isSending) {
        console.warn('[sendMessage] Request already sending, ignoring new input');
        return;
    }
    
    const input = document.getElementById("userInput");
    const chatMessages = document.getElementById("chatMessages");

    if (!input || !chatMessages) {
        console.error('[sendMessage] Critical elements missing: input=' + !!input + ', chatMessages=' + !!chatMessages);
        return;
    }

    const text = input.value.trim();
    if (!text || text.length === 0) {
        console.warn('[sendMessage] Empty input ignored');
        return;
    }
    
    // Log user input capture
    console.log('[sendMessage] User input captured:', {text: text, stage: analysisState.stage});
    
    isSending = true;

    addUserMessage(chatMessages, text);

    input.value = "";
    input.style.height = "auto";

    try {
        if (analysisState.stage === "collect_idea") {
            console.log('[sendMessage] Stage -> collect_idea, storing idea:', text);
            analysisState.idea = text;
            analysisState.stage = "collect_market";
            displayAIMessage(chatMessages, "Great! Now tell me your <b>target market</b>.");
            return;
        }
        if (analysisState.stage === "collect_market") {
            console.log('[sendMessage] Stage -> collect_market, storing market:', text);
            analysisState.target_market = text;
            analysisState.stage = "collect_problem";
            displayAIMessage(chatMessages, "Perfect! What problem does your idea solve?");
            return;
        }
        if (analysisState.stage === "collect_problem") {
            console.log('[sendMessage] Stage -> collect_problem, storing problem. Ready to analyze.', {
                idea: analysisState.idea,
                target_market: analysisState.target_market,
                problem_statement: text
            });
            analysisState.problem_statement = text;
            analysisState.stage = "completed";
            await analyzeWithBackend(chatMessages);
            return;
        }
    } catch (error) {
        console.error('[sendMessage] Unexpected error:', error);
        displayAIMessage(chatMessages, `❌ An unexpected error occurred: ${escapeHtml(error.message)}`);
    } finally {
        isSending = false;
        console.log('[sendMessage] Request complete, isSending reset to false');
    }
}

/* =============================
   USER MESSAGE
============================= */

function addUserMessage(chatMessages, text) {
    console.log('[addUserMessage] Creating user message element, text length:', text.length);
    
    const div = document.createElement("div");
    div.className = "message-group user-message";
    div.innerHTML = `
        <div class="message-bubble user">
            ${escapeHtml(text)}
        </div>
        <div class="message-avatar">👤</div>
    `;
    
    chatMessages.appendChild(div);
    console.log('[addUserMessage] User message appended to DOM. Total messages:', chatMessages.children.length);
    
    // Optimize scroll: use requestAnimationFrame to batch DOM updates
    if (chatMessages.scrollHeight > chatMessages.clientHeight) {
        requestAnimationFrame(() => {
            chatMessages.scrollTop = chatMessages.scrollHeight;
            console.log('[addUserMessage] Scrolled to bottom');
        });
    }
}

/* =============================
   AI MESSAGE
============================= */

function displayAIMessage(chatMessages, message) {
    console.log('[displayAIMessage] Creating AI message element, message length:', message.length);
    
    const div = document.createElement("div");
    div.className = "message-group ai-message";
    div.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="message-bubble ai">
            ${message}
        </div>
    `;
    
    chatMessages.appendChild(div);
    console.log('[displayAIMessage] AI message appended to DOM. Total messages:', chatMessages.children.length);
    
    // Optimize scroll: use requestAnimationFrame to batch DOM updates
    if (chatMessages.scrollHeight > chatMessages.clientHeight) {
        requestAnimationFrame(() => {
            chatMessages.scrollTop = chatMessages.scrollHeight;
            console.log('[displayAIMessage] Scrolled to bottom');
        });
    }
}

/* =============================
   BACKEND CONNECTION (FIXED)
============================= */

async function analyzeWithBackend(chatMessages) {

    const typing = document.createElement("div");
    typing.id = "typingIndicator";
    typing.className = "message-group ai-message";

    typing.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="message-bubble ai">
            🔄 Analyzing your idea...
        </div>
    `;

    chatMessages.appendChild(typing);
    console.log('[analyzeWithBackend] Typing indicator added to DOM');
    
    requestAnimationFrame(() => {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    });

    try {

        const backendUrl = getBackendUrl();
        const analyzeUrl = `${backendUrl}/analyze`;
        
        console.log('[analyzeWithBackend] POST request to:', analyzeUrl);
        console.log('[analyzeWithBackend] Request payload:', {
            idea: analysisState.idea,
            target_market: analysisState.target_market,
            problem_statement: analysisState.problem_statement
        });

        const response = await fetchWithRetry(analyzeUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                idea: analysisState.idea,
                target_market: analysisState.target_market,
                problem_statement: analysisState.problem_statement
            })
        });

        console.log('[analyzeWithBackend] Response received - Status:', response.status, 'OK:', response.ok);

        if (!response.ok) {
            throw new Error(`Backend returned ${response.status}: ${response.statusText}`);
        }

        let data;
        try {
            data = await response.json();
            console.log('[analyzeWithBackend] JSON parsed successfully', {
                hasAnalysis: !!data.analysis,
                hasScore: data.compatibility_score !== undefined,
                score: data.compatibility_score,
                riskLevel: data.risk_level,
                tagsCount: Array.isArray(data.domain_tags) ? data.domain_tags.length : 0
            });
        } catch (jsonError) {
            console.error('[analyzeWithBackend] JSON parsing error:', jsonError);
            throw new Error('Received invalid response from backend');
        }
        
        // Validate response has required fields with defensive guards
        if (!data) {
            console.error('[analyzeWithBackend] Response data is null or undefined');
            throw new Error('Backend returned empty response');
        }
        
        if (!data.analysis || typeof data.analysis !== 'string') {
            console.error('[analyzeWithBackend] Missing or invalid analysis field:', data.analysis);
            throw new Error('Backend returned incomplete analysis data (missing analysis field)');
        }
        
        if (data.compatibility_score === undefined || data.compatibility_score === null) {
            console.error('[analyzeWithBackend] Missing or invalid score field:', data.compatibility_score);
            throw new Error('Backend returned incomplete analysis data (missing score)');
        }
        
        if (!data.risk_level || typeof data.risk_level !== 'string') {
            console.error('[analyzeWithBackend] Missing or invalid risk_level field:', data.risk_level);
            throw new Error('Backend returned incomplete analysis data (missing risk level)');
        }
        
        // Safely access array fields
        const tags = Array.isArray(data.domain_tags) ? data.domain_tags : [];
        console.log('[analyzeWithBackend] Validation complete, all required fields present');
        
        // Store the analysis response for BRD generation
        analysisState.analysisResponse = data;
        console.log('[analyzeWithBackend] Analysis response stored in state for BRD generation');

        const typingElement = document.getElementById("typingIndicator");
        if (typingElement) {
            typingElement.remove();
            console.log('[analyzeWithBackend] Typing indicator removed from DOM');
        } else {
            console.warn('[analyzeWithBackend] Typing indicator element not found in DOM');
        }

        const aiResponse = `
            <b>Analysis Complete 📊</b><br><br>
            Idea: ${escapeHtml(data.idea || analysisState.idea)}<br>
            Target Market: ${escapeHtml(data.target_market || analysisState.target_market)}<br>
            Problem: ${escapeHtml(data.problem_statement || analysisState.problem_statement)}<br><br>

            Analysis:<br>
            ${escapeHtml(data.analysis)}<br><br>

            Score: <span style="color:#10b981">
            ${data.compatibility_score}/100
            </span><br>
            Risk Level: <span style="color:#f59e0b">${escapeHtml(data.risk_level)}</span><br>
            Domain Tags: <span style="color:#8b5cf6">${tags.map(t => escapeHtml(String(t))).join(", ")}</span><br><br>
            
            <button onclick="openBrdModal()" class="btn btn-primary" style="margin-top: 10px;">📄 Generate BRD</button>
        `;
        
        console.log('[analyzeWithBackend] Displaying AI response message');
        displayAIMessage(chatMessages, aiResponse);
        console.log('[analyzeWithBackend] Analysis complete and displayed');

    } catch (error) {

        console.error('[analyzeWithBackend] Error during analysis:', error.message);

        const typingElement = document.getElementById("typingIndicator");
        if (typingElement) {
            typingElement.remove();
            console.log('[analyzeWithBackend] Typing indicator removed due to error');
        }

        const backendUrl = getBackendUrl();
        const errorMsg = error.message.includes('unreachable') 
            ? `Backend server is not reachable at ${backendUrl}`
            : error.message;

        const errorResponse = 
            `❌ Analysis failed.<br><br>` +
            `<b>Error:</b> ${escapeHtml(errorMsg)}<br><br>` +
            `<b>Backend URL:</b> ${escapeHtml(backendUrl)}<br>` +
            `⚠️ Ensure FastAPI server is running:<br>` +
            `<code style="background:#f5f5f5;padding:4px 8px;border-radius:4px;">uvicorn main:app --reload</code>`;

        console.log('[analyzeWithBackend] Displaying error message to user');
        displayAIMessage(chatMessages, errorResponse);
    }
}

/* =============================
   BRD GENERATION
============================= */

function openBrdModal() {
    const modal = document.getElementById("brdModal");
    if (modal) {
        modal.style.display = "flex";
    }
}

function closeBrdModal() {
    const modal = document.getElementById("brdModal");
    if (modal) {
        modal.style.display = "none";
    }
}

// Store current PDF blob for download functionality
let currentPdfBlob = null;
let currentPdfFilename = null;

async function generateBrd() {
    if (!analysisState.analysisResponse) {
        alert("No analysis data available. Please complete an analysis first.");
        return;
    }

    const selectedFormat = document.querySelector('input[name="brdFormat"]:checked')?.value || "pdf";
    const generateBtn = document.getElementById("generateBrdBtn");
    
    if (!generateBtn || generateBtn.disabled) return;
    
    const originalText = generateBtn.textContent;
    generateBtn.textContent = "⏳ Generating...";
    generateBtn.disabled = true;

    const maxRetries = 2;
    let lastError = null;
    
    for (let attempt = 0; attempt < maxRetries; attempt++) {
        try {
            const response = await fetch(`${getBackendUrl()}/generate_brd`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    format: selectedFormat,
                    analysis_data: analysisState.analysisResponse
                })
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || `Server error: ${response.status}`);
            }
            
            // Successfully got response - extract filename
            const disposition = response.headers.get("Content-Disposition");
            let filename = `BRD_${analysisState.analysisResponse.idea.replace(/\s+/g, "_").substring(0, 30)}.${selectedFormat === "image" ? "png" : selectedFormat === "pdf" ? "pdf" : selectedFormat === "docx" ? "docx" : "txt"}`;
            
            if (disposition) {
                const matches = disposition.match(/filename=(.+)/);
                if (matches) filename = matches[1].replace(/"/g, "");
            }

            try {
                const blob = await response.blob();
                
                // Validate blob is not empty
                if (!blob || blob.size === 0) {
                    throw new Error('Generated document is empty');
                }
                
                // Type-specific handling
                if (selectedFormat === "pdf") {
                    // PDF: Show in viewer
                    displayPdfPreview(blob, filename);
                } else {
                    // Other formats: Download directly
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement("a");
                    a.href = url;
                    a.download = filename;
                    document.body.appendChild(a);
                    a.click();
                    
                    setTimeout(() => {
                        window.URL.revokeObjectURL(url);
                        document.body.removeChild(a);
                    }, 100);
                    
                    alert(`✅ ${selectedFormat.toUpperCase()} generated successfully! File: ${filename}`);
                }
                
                closeBrdModal();
                generateBtn.textContent = originalText;
                generateBtn.disabled = false;
                return;
                
            } catch (blobError) {
                console.error('Error processing file:', blobError);
                throw new Error('Failed to process generated file');
            }
            
        } catch (error) {
            lastError = error;
            console.error(`BRD Generation Error (attempt ${attempt + 1}/${maxRetries}):`, error);
            if (attempt < maxRetries - 1) {
                await new Promise(resolve => setTimeout(resolve, 500));
            }
        }
    }
    
    if (lastError) {
        const userMessage = lastError.message.includes('Server error') 
            ? "Backend issue. Please try again."
            : "Network error. Please check connection and try again.";
        alert(`❌ Error generating BRD:\n\n${userMessage}\n\nDetails: ${lastError.message}`);
    }

    generateBtn.textContent = originalText;
    generateBtn.disabled = false;
}

/**
 * Display PDF blob in the viewer
 * @param {Blob} blob - The PDF blob to display
 * @param {string} filename - The filename for download
 */
function displayPdfPreview(blob, filename) {
    try {
        // Store blob and filename for download
        currentPdfBlob = blob;
        currentPdfFilename = filename;
        
        // Create object URL from blob
        const blobUrl = window.URL.createObjectURL(blob);
        
        // Display in iframe
        const pdfViewer = document.getElementById("pdfViewer");
        const pdfViewerContainer = document.getElementById("pdfViewerContainer");
        
        if (!pdfViewer || !pdfViewerContainer) {
            throw new Error('PDF viewer elements not found in DOM');
        }
        
        pdfViewer.src = blobUrl;
        pdfViewerContainer.style.display = "flex";
        
        // Setup close handlers if not already done
        setupPdfViewerControls();
        
        console.log(`✅ PDF Preview loaded - Size: ${blob.size} bytes`);
        
    } catch (error) {
        console.error('Error displaying PDF:', error);
        alert('Failed to display PDF preview. The file may have been generated but try downloading instead.');
    }
}

/**
 * Setup event listeners for PDF viewer controls
 */
function setupPdfViewerControls() {
    const closeButton = document.getElementById("closePdfViewer");
    const closeBtn = document.getElementById("closePdfViewerBtn");
    const downloadBtn = document.getElementById("downloadFromViewer");
    
    // Remove existing listeners to avoid duplicates
    if (closeButton) {
        closeButton.onclick = null;
        closeButton.addEventListener("click", closePdfViewer, { once: false });
    }
    
    if (closeBtn) {
        closeBtn.onclick = null;
        closeBtn.addEventListener("click", closePdfViewer, { once: false });
    }
    
    if (downloadBtn) {
        downloadBtn.onclick = null;
        downloadBtn.addEventListener("click", downloadCurrentPdf, { once: false });
    }
}

/**
 * Close the PDF viewer and cleanup
 */
function closePdfViewer() {
    const pdfViewerContainer = document.getElementById("pdfViewerContainer");
    const pdfViewer = document.getElementById("pdfViewer");
    
    if (pdfViewerContainer) {
        pdfViewerContainer.style.display = "none";
    }
    
    if (pdfViewer && pdfViewer.src) {
        // Revoke the blob URL to free memory
        try {
            window.URL.revokeObjectURL(pdfViewer.src);
        } catch (e) {
            console.warn('Failed to revoke object URL:', e);
        }
        pdfViewer.src = "";
    }
    
    // Clear stored blob and filename
    currentPdfBlob = null;
    currentPdfFilename = null;
}

/**
 * Download the currently displayed PDF
 */
function downloadCurrentPdf() {
    if (!currentPdfBlob || !currentPdfFilename) {
        alert("No PDF available to download");
        return;
    }
    
    try {
        const url = window.URL.createObjectURL(currentPdfBlob);
        const a = document.createElement("a");
        a.href = url;
        a.download = currentPdfFilename;
        document.body.appendChild(a);
        a.click();
        
        setTimeout(() => {
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        }, 100);
        
        alert(`✅ PDF downloaded: ${currentPdfFilename}`);
    } catch (error) {
        console.error('Error downloading PDF:', error);
        alert('Failed to download PDF');
    }
}

/* =============================
   NOTE: Modal listeners set by setupBRDModalListeners() from main DOMContentLoaded
============================= */