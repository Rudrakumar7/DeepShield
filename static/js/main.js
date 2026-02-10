// Make Chatbot Launcher Draggable
const launcher = document.getElementById('chat-launcher');
const widget = document.getElementById('chat-widget');

let isDragging = false;
let hasMoved = false; // To distinguish drag from click

function makeDraggable(element) {
    let pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;

    element.onmousedown = dragMouseDown;

    function dragMouseDown(e) {
        e = e || window.event;
        e.preventDefault();
        // Get the mouse cursor position at startup:
        pos3 = e.clientX;
        pos4 = e.clientY;
        document.onmouseup = closeDragElement;
        document.onmousemove = elementDrag;
        hasMoved = false;
    }

    function elementDrag(e) {
        e = e || window.event;
        e.preventDefault();
        isDragging = true;
        hasMoved = true;
        // Calculate the new cursor position:
        pos1 = pos3 - e.clientX;
        pos2 = pos4 - e.clientY;
        pos3 = e.clientX;
        pos4 = e.clientY;
        // Set the element's new position:
        element.style.top = (element.offsetTop - pos2) + "px";
        element.style.left = (element.offsetLeft - pos1) + "px";
        element.style.bottom = 'auto'; // Reset bottom/right to allow free movement
        element.style.right = 'auto';

        // Move widget with the launcher (optional, or just update on toggle)
        updateWidgetPosition();
    }

    function closeDragElement() {
        // Stop moving when mouse button is released:
        document.onmouseup = null;
        document.onmousemove = null;
        setTimeout(() => { isDragging = false; }, 100); // Small delay to prevent click trigger
    }
}

function updateWidgetPosition() {
    // Position widget above the launcher
    const launcherRect = launcher.getBoundingClientRect();
    const widgetHeight = 500;
    const widgetWidth = 350;

    // Default: Above and to the left/right/center
    let top = launcherRect.top - widgetHeight - 10;
    let left = launcherRect.left - widgetWidth + launcherRect.width;

    // Boundary Validation
    if (top < 10) top = 10; // Don't go off-screen top
    if (left < 10) left = 10; // Don't go off-screen left

    // Check if right side goes off screen
    if (left + widgetWidth > window.innerWidth) {
        left = window.innerWidth - widgetWidth - 10;
    }

    widget.style.top = top + "px";
    widget.style.left = left + "px";
    widget.style.bottom = 'auto';
    widget.style.right = 'auto';
}

makeDraggable(launcher);

// Override toggleChat to handle move vs click and positioning
function toggleChat() {
    if (hasMoved) return; // Don't toggle if we just dragged

    if (widget.style.display === 'flex') {
        widget.style.display = 'none';
    } else {
        updateWidgetPosition();
        widget.style.display = 'flex';
        document.getElementById('chat-input').focus();
    }
}

function handleChatInput(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

async function sendMessage() {
    const inputField = document.getElementById('chat-input');
    const message = inputField.value.trim();
    if (!message) return;

    // Add User Message
    addMessage(message, 'user-message');
    inputField.value = '';

    // Show Typing Indicator (Optional, could just wait)

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });

        const data = await response.json();
        addMessage(data.response, 'bot-message');
    } catch (error) {
        console.error('Error sending message:', error);
        addMessage("Sorry, I'm having trouble connecting to the server.", 'bot-message');
    }
}

function addMessage(text, className) {
    const chatBody = document.getElementById('chat-body');
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${className}`;
    messageDiv.innerHTML = text; // Allow HTML for links
    chatBody.appendChild(messageDiv);
    chatBody.scrollTop = chatBody.scrollHeight;
}
