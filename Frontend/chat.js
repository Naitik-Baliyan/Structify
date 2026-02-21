/* ============================================================
   STRUCTIFY CHAT SYSTEM - CLEAN REBUILD VERSION
   ============================================================ */

function getBackendUrl() {
    const url = (typeof API_CONFIG !== 'undefined' && API_CONFIG.BACKEND_URL) ? API_CONFIG.BACKEND_URL : 'http://127.0.0.1:8001';
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
    if (chatInitialized) return;
    chatInitialized = true;
    
    checkUserAuthentication();
    initializeChatInterface();
    setupBRDModalListeners();
});

let brdModalListenersInitialized = false;

function setupBRDModalListeners() {
    if (brdModalListenersInitialized) return;
    brdModalListenersInitialized = true;
    
    const brdModal = document.getElementById("brdModal");
    const brdCloseBtn = brdModal?.querySelector(".modal-close");
    const brdCancelBtn = document.getElementById("cancelBrdBtn");
    const brdGenerateBtn = document.getElementById("generateBrdBtn");

    if (brdCloseBtn) brdCloseBtn.addEventListener("click", closeBrdModal);
    if (brdCancelBtn) brdCancelBtn.addEventListener("click", closeBrdModal);
    if (brdGenerateBtn) brdGenerateBtn.addEventListener("click", generateBrd);

    if (brdModal) {
        brdModal.addEventListener("click", (e) => {
            if (e.target === brdModal) closeBrdModal();
        });
    }
}

/* =============================
   CHAT INTERFACE
============================= */

function initializeChatInterface() {

    const userInput = document.getElementById("userInput");
    const sendBtn = document.getElementById("sendBtn");

    if (userInput) {
        userInput.addEventListener("keydown", e => {
            if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });
    }

    sendBtn?.addEventListener("click", sendMessage);
}

/* =============================
   MESSAGE SYSTEM
============================= */

let isSending = false;

async function sendMessage() {
    if (isSending) return;
    
    const input = document.getElementById("userInput");
    const chatMessages = document.getElementById("chatMessages");

    if (!input || !chatMessages) return;

    const text = input.value.trim();
    if (!text || text.length === 0) return;
    
    isSending = true;

    addUserMessage(chatMessages, text);

    input.value = "";
    input.style.height = "auto";

    try {
        if (analysisState.stage === "collect_idea") {
            analysisState.idea = text;
            analysisState.stage = "collect_market";
            displayAIMessage(chatMessages, "Great! Now tell me your <b>target market</b>.");
            return;
        }
        if (analysisState.stage === "collect_market") {
            analysisState.target_market = text;
            analysisState.stage = "collect_problem";
            displayAIMessage(chatMessages, "Perfect! What problem does your idea solve?");
            return;
        }
        if (analysisState.stage === "collect_problem") {
            analysisState.problem_statement = text;
            analysisState.stage = "completed";
            await analyzeWithBackend(chatMessages);
            return;
        }
    } finally {
        isSending = false;
    }
}

/* =============================
   USER MESSAGE
============================= */

function addUserMessage(chatMessages, text) {

    const div = document.createElement("div");

    div.className = "message-group user-message";

    div.innerHTML = `
        <div class="message-bubble user">
            ${escapeHtml(text)}
        </div>
        <div class="message-avatar">👤</div>
    `;

    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

/* =============================
   AI MESSAGE
============================= */

function displayAIMessage(chatMessages, message) {

    const div = document.createElement("div");

    div.className = "message-group ai-message";

    div.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="message-bubble ai">
            ${message}
        </div>
    `;

    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;
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
            Thinking...
        </div>
    `;

    chatMessages.appendChild(typing);

    try {

        const backendUrl = getBackendUrl();
        const analyzeUrl = `${backendUrl}/analyze`;
        
        console.log('[analyzeWithBackend] Calling:', analyzeUrl);

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

        if (!response.ok)
            throw new Error(`Backend returned ${response.status}: ${response.statusText}`);

        const data = await response.json();
        
        // Store the analysis response for BRD generation
        analysisState.analysisResponse = data;

        document.getElementById("typingIndicator")?.remove();

        displayAIMessage(chatMessages, `
            <b>Analysis Complete 📊</b><br><br>
            Idea: ${escapeHtml(data.idea)}<br>
            Target Market: ${escapeHtml(data.target_market)}<br>
            Problem: ${escapeHtml(data.problem_statement)}<br><br>

            Analysis:<br>
            ${escapeHtml(data.analysis)}<br><br>

            Score: <span style="color:#10b981">
            ${data.compatibility_score}/100
            </span><br>
            Risk Level: <span style="color:#f59e0b">${escapeHtml(data.risk_level)}</span><br>
            Domain Tags: <span style="color:#8b5cf6">${data.domain_tags.join(", ")}</span><br><br>
            
            <button onclick="openBrdModal()" class="btn btn-primary" style="margin-top: 10px;">📄 Generate BRD</button>
        `);

    } catch (error) {

        console.error('[analyzeWithBackend] Error:', error);

        document.getElementById("typingIndicator")?.remove();

        displayAIMessage(chatMessages,
            `❌ Backend connection failed.<br><br>` +
            `Error: ${error.message}<br><br>` +
            `Backend URL: ${getBackendUrl()}<br>` +
            `Make sure FastAPI server is running!`
        );
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
            
            lastError = null;
            break;

            const disposition = response.headers.get("Content-Disposition");
            let filename = `BRD_${analysisState.analysisResponse.idea.replace(/\s+/g, "_").substring(0, 30)}.${selectedFormat === "image" ? "png" : selectedFormat === "pdf" ? "pdf" : selectedFormat === "docx" ? "docx" : "txt"}`;
            
            if (disposition) {
                const matches = disposition.match(/filename=(.+)/);
                if (matches) filename = matches[1].replace(/"/g, "");
            }

            const blob = await response.blob();
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

            closeBrdModal();
            alert(`✅ BRD generated successfully! File: ${filename}`);
            generateBtn.textContent = originalText;
            generateBtn.disabled = false;
            return;
            
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
            ? "Server issue. Please try again."
            : lastError.message;
        alert(`❌ Error generating BRD: ${userMessage}`);
    }

    generateBtn.textContent = originalText;
    generateBtn.disabled = false;
}

/* =============================
   NOTE: Modal listeners set by setupBRDModalListeners() from main DOMContentLoaded
============================= */
});