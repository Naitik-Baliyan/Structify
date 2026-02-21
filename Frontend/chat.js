/* ============================================================
   STRUCTIFY CHAT SYSTEM - CLEAN REBUILD VERSION
   ============================================================ */

const BACKEND_URL = "http://127.0.0.1:8000";

/* =============================
   AUTH CHECK
============================= */

function checkUserAuthentication() {
    const user = localStorage.getItem("structify_current_user");
    if (!user) window.location.href = "login.html";
}

/* =============================
   CHAT STATE
============================= */

const analysisState = {
    idea: null,
    target_market: null,
    problem_statement: null,
    stage: "collect_idea"
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

document.addEventListener("DOMContentLoaded", () => {
    checkUserAuthentication();
    initializeChatInterface();
});

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

async function sendMessage() {

    const input = document.getElementById("userInput");
    const chatMessages = document.getElementById("chatMessages");

    if (!input || !chatMessages) return;

    const text = input.value.trim();
    if (!text) return;

    addUserMessage(chatMessages, text);

    input.value = "";
    input.style.height = "auto";

    if (analysisState.stage === "collect_idea") {
        analysisState.idea = text;
        analysisState.stage = "collect_market";

        displayAIMessage(chatMessages,
            "Great! Now tell me your <b>target market</b>."
        );
        return;
    }

    if (analysisState.stage === "collect_market") {
        analysisState.target_market = text;
        analysisState.stage = "collect_problem";

        displayAIMessage(chatMessages,
            "Perfect! What problem does your idea solve?"
        );
        return;
    }

    if (analysisState.stage === "collect_problem") {
        analysisState.problem_statement = text;
        analysisState.stage = "completed";

        await analyzeWithBackend(chatMessages);
        return;
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

        const response = await fetch(`${BACKEND_URL}/analyze`, {
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
            throw new Error("Backend connection failed");

        const data = await response.json();

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
            </span>
        `);

    } catch (error) {

        console.error(error);

        document.getElementById("typingIndicator")?.remove();

        displayAIMessage(chatMessages,
            "Backend connection failed. Make sure FastAPI server is running."
        );
    }
}