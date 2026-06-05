/* AmazonPeptide Chat Widget JS */

(function () {
    const API_URL = '/api/chat';
    let sessionMessages = [];
    let userMessageCount = 0;
    let isWaiting = false;

    // DOM Elements
    let containerEl = null;
    let launcherEl = null;
    let closeBtnEl = null;
    let feedEl = null;
    let inputEl = null;
    let goBtnEl = null;
    let sessionCountEl = null;

    const WELCOME_MESSAGE = "Welcome to the AmazonPeptide Research Database. Ask me any theoretical question about peptide therapeutics.";

    function init() {
        containerEl = document.getElementById('peptide-chat-widget');
        launcherEl = document.getElementById('chat-launcher');
        closeBtnEl = document.getElementById('chat-close-btn');
        feedEl = document.getElementById('chat-feed');
        inputEl = document.getElementById('chat-input');
        goBtnEl = document.getElementById('chat-go-btn');
        sessionCountEl = document.getElementById('chat-session-count');

        if (!containerEl || !launcherEl || !closeBtnEl || !feedEl || !inputEl || !goBtnEl || !sessionCountEl) {
            console.error("Peptide chat widget elements missing from DOM.");
            return;
        }

        // Event Listeners
        launcherEl.addEventListener('click', expandWidget);
        closeBtnEl.addEventListener('click', collapseWidget);
        goBtnEl.addEventListener('click', handleGoAction);
        inputEl.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleGoAction();
            }
        });

        // Initialize empty state
        resetChatState();
    }

    function expandWidget() {
        containerEl.classList.remove('collapsed');
        containerEl.classList.add('expanded');
        inputEl.focus();
    }

    function collapseWidget() {
        containerEl.classList.remove('expanded');
        containerEl.classList.add('collapsed');
    }

    function resetChatState() {
        sessionMessages = [];
        userMessageCount = 0;
        isWaiting = false;

        // Reset Feed
        feedEl.innerHTML = '';
        appendMessage('assistant', WELCOME_MESSAGE, false); // welcome message doesn't need typing effect

        // Reset inputs
        inputEl.value = '';
        inputEl.disabled = false;
        
        // Reset Go button to default state
        goBtnEl.innerText = 'Go!';
        goBtnEl.disabled = false;
        goBtnEl.style.background = 'linear-gradient(to bottom, #FFE099, #FFB040)';
        goBtnEl.style.borderColor = '#A87000';

        // Reset session label
        sessionCountEl.innerText = `Session: 0/5 messages`;
    }

    function handleGoAction() {
        if (userMessageCount >= 5) {
            resetChatState();
            return;
        }

        const text = inputEl.value.trim();
        if (!text) return;

        sendMessage(text);
    }

    async function sendMessage(text) {
        if (isWaiting) return;

        // 1. Add user message to local state & UI
        sessionMessages.push({ role: 'user', text: text });
        userMessageCount++;
        appendMessage('user', text, false);

        // Clear input and disable input elements
        inputEl.value = '';
        inputEl.disabled = true;
        goBtnEl.disabled = true;
        isWaiting = true;

        sessionCountEl.innerText = `Session: ${userMessageCount}/5 messages`;

        // 2. Add loading state to feed
        const loadingEl = addLoadingIndicator();

        try {
            // 3. Make backend API request
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ messages: sessionMessages })
            });

            removeLoadingIndicator(loadingEl);

            if (!response.ok) {
                throw new Error("Server error");
            }

            const data = await response.json();
            
            // 4. Update state with assistant reply
            sessionMessages.push({ role: 'model', text: data.reply });

            // Typewriter effect callback
            appendMessage('assistant', data.reply, true, () => {
                isWaiting = false;

                if (userMessageCount >= 5) {
                    // Lock inputs when session limit is reached
                    inputEl.disabled = true;
                    sessionCountEl.innerText = `5/5 messages used. Chat history cleared on reset.`;
                    
                    // Transition Go button to Reset Chat
                    goBtnEl.innerText = 'Reset Chat';
                    goBtnEl.disabled = false;
                    goBtnEl.style.background = 'linear-gradient(to bottom, #FFF099, #FFC040)';
                    goBtnEl.style.borderColor = '#A87000';
                } else {
                    inputEl.disabled = false;
                    goBtnEl.disabled = false;
                    inputEl.focus();
                }
            });

        } catch (error) {
            removeLoadingIndicator(loadingEl);
            isWaiting = false;
            userMessageCount--; // rollback count on error so user can retry
            sessionMessages.pop(); // rollback history
            sessionCountEl.innerText = `Session: ${userMessageCount}/5 messages`;
            
            appendMessage('system', "Database timeout. Please verify connection and click Go! again.", false);
            
            inputEl.disabled = false;
            goBtnEl.disabled = false;
            inputEl.focus();
        }
    }

    function appendMessage(role, text, useTypewriter = false, onComplete = null) {
        const msgContainer = document.createElement('div');
        msgContainer.classList.add('chat-msg', role);

        const textEl = document.createElement('span');
        textEl.classList.add('chat-msg-text');
        msgContainer.appendChild(textEl);

        feedEl.appendChild(msgContainer);
        scrollToBottom();

        if (useTypewriter) {
            let charIndex = 0;
            const speed = 15; // Fast typewriter (15ms per character)
            
            function typeNextChar() {
                if (charIndex < text.length) {
                    textEl.textContent += text.charAt(charIndex);
                    charIndex++;
                    scrollToBottom();
                    setTimeout(typeNextChar, speed);
                } else {
                    if (onComplete) onComplete();
                }
            }
            typeNextChar();
        } else {
            textEl.textContent = text;
            if (onComplete) onComplete();
        }
    }

    function addLoadingIndicator() {
        const loadingEl = document.createElement('div');
        loadingEl.classList.add('chat-loading');
        loadingEl.innerHTML = `Searching database<span class="chat-loading-dots">...</span>`;
        feedEl.appendChild(loadingEl);
        scrollToBottom();
        return loadingEl;
    }

    function removeLoadingIndicator(el) {
        if (el && el.parentNode) {
            el.parentNode.removeChild(el);
        }
    }

    function scrollToBottom() {
        feedEl.scrollTop = feedEl.scrollHeight;
    }

    window.AmazonPeptideChat = {
        init: init
    };
})();
