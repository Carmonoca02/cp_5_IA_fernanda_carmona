// Variáveis globais
let isLoading = false;

// Funções de navegação
function scrollToChat() {
    document.getElementById('chatbot').scrollIntoView({ behavior: 'smooth' });
}

function scrollToProducts() {
    document.getElementById('products').scrollIntoView({ behavior: 'smooth' });
}

// Função para enviar mensagem
async function sendMessage() {
    const input = document.getElementById('user-input');
    const message = input.value.trim();
    
    if (!message || isLoading) return;
    
    // Limpa o input
    input.value = '';
    
    // Adiciona mensagem do usuário
    addMessage(message, 'user');
    
    // Mostra loading
    isLoading = true;
    const loadingElement = addLoadingMessage();
    
    try {
        // Envia para o backend
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });
        
        const data = await response.json();
        
        // Remove loading
        removeLoadingMessage(loadingElement);
        
        // Adiciona resposta do bot com informações completas
        addBotMessage(data);
        
    } catch (error) {
        console.error('Erro:', error);
        removeLoadingMessage(loadingElement);
        const errorData = {
            response: '🤔 Desculpe, ocorreu um erro. Tente novamente em instantes.',
            intent: 'error',
            confidence: 0.0,
            is_multiple: false
        };
        addBotMessage(errorData);
    } finally {
        isLoading = false;
    }
}

// Função para enviar sugestão
function sendSuggestion(text) {
    document.getElementById('user-input').value = text;
    sendMessage();
}

// Função para adicionar mensagem do usuário ao chat
function addMessage(text, sender) {
    const messagesContainer = document.getElementById('chat-messages');
    
    const messageElement = document.createElement('div');
    messageElement.className = `message ${sender}-message`;
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = sender === 'user' ? '👤' : '🤖';
    
    const content = document.createElement('div');
    content.className = 'message-content';
    const paragraph = document.createElement('p');
    paragraph.textContent = text;
    content.appendChild(paragraph);
    
    messageElement.appendChild(avatar);
    messageElement.appendChild(content);
    
    messagesContainer.appendChild(messageElement);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    
    return messageElement;
}

// Função para adicionar mensagem completa do bot
function addBotMessage(data) {
    const messagesContainer = document.getElementById('chat-messages');
    
    const messageElement = document.createElement('div');
    messageElement.className = 'message bot-message enhanced-bot-message';
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = '🤖';
    
    const content = document.createElement('div');
    content.className = 'message-content';
    
    // Resposta principal
    const responseText = document.createElement('p');
    responseText.className = 'bot-response-text';
    responseText.textContent = data.response;
    content.appendChild(responseText);
    
    // Informações técnicas em container separado
    const infoContainer = document.createElement('div');
    infoContainer.className = 'bot-info-container';
    
    // Intenção detectada
    const intentInfo = document.createElement('div');
    intentInfo.className = 'bot-info-item';
    intentInfo.innerHTML = `
        <span class="info-label">🎯 Intenção:</span> 
        <span class="info-value intent-value">${formatIntent(data.intent)}</span>
    `;
    infoContainer.appendChild(intentInfo);
    
    // Confiança/Probabilidade
    const confidenceInfo = document.createElement('div');
    confidenceInfo.className = 'bot-info-item';
    const confidencePercent = Math.round(data.confidence * 100);
    const confidenceClass = getConfidenceClass(data.confidence);
    confidenceInfo.innerHTML = `
        <span class="info-label">📊 Confiança:</span> 
        <span class="info-value confidence-value ${confidenceClass}">${confidencePercent}%</span>
    `;
    infoContainer.appendChild(confidenceInfo);
    
    // Informações adicionais se múltiplas sentenças
    if (data.is_multiple && data.sentence_count > 1) {
        const sentencesInfo = document.createElement('div');
        sentencesInfo.className = 'bot-info-item';
        sentencesInfo.innerHTML = `
            <span class="info-label">📝 Sentenças:</span> 
            <span class="info-value">${data.sentence_count} detectadas</span>
        `;
        infoContainer.appendChild(sentencesInfo);
        
        // Mostrar intenções detectadas se houver múltiplas
        if (data.detected_intents && data.detected_intents.length > 0) {
            const detectedInfo = document.createElement('div');
            detectedInfo.className = 'bot-info-item';
            detectedInfo.innerHTML = `
                <span class="info-label">🔍 Detectadas:</span> 
                <span class="info-value">${data.detected_intents.map(formatIntent).join(', ')}</span>
            `;
            infoContainer.appendChild(detectedInfo);
        }
    }
    
    content.appendChild(infoContainer);
    
    messageElement.appendChild(avatar);
    messageElement.appendChild(content);
    
    messagesContainer.appendChild(messageElement);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    
    return messageElement;
}

// Função para formatar nomes de intenções
function formatIntent(intent) {
    const intentMap = {
        'greeting': 'Saudação',
        'goodbye': 'Despedida', 
        'thanks': 'Agradecimento',
        'menu': 'Cardápio',
        'hours': 'Horário',
        'payment': 'Pagamento',
        'delivery': 'Entrega',
        'prices': 'Preços',
        'orders': 'Pedidos',
        'location': 'Localização',
        'about': 'Sobre',
        'contact': 'Contato',
        'fallback': 'Não identificada',
        'error': 'Erro'
    };
    
    return intentMap[intent] || intent;
}

// Função para determinar classe CSS baseada na confiança
function getConfidenceClass(confidence) {
    if (confidence >= 0.8) return 'confidence-high';
    if (confidence >= 0.5) return 'confidence-medium';
    return 'confidence-low';
}

// Função para adicionar loading
function addLoadingMessage() {
    const messagesContainer = document.getElementById('chat-messages');
    
    const messageElement = document.createElement('div');
    messageElement.className = 'message bot-message';
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = '🤖';
    
    const content = document.createElement('div');
    content.className = 'message-content';
    const loadingDiv = document.createElement('div');
    loadingDiv.innerHTML = '<div class="loading"></div>';
    content.appendChild(loadingDiv);
    
    messageElement.appendChild(avatar);
    messageElement.appendChild(content);
    
    messagesContainer.appendChild(messageElement);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    
    return messageElement;
}

// Função para remover loading
function removeLoadingMessage(element) {
    if (element && element.parentNode) {
        element.parentNode.removeChild(element);
    }
}

// Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    // Enter para enviar mensagem
    const input = document.getElementById('user-input');
    input.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    // Auto-resize do textarea (se necessário)
    input.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = Math.min(this.scrollHeight, 100) + 'px';
    });
    
    // Smooth scroll para links do menu
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
    
    // Menu mobile
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    
    if (hamburger && navMenu) {
        hamburger.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            this.classList.toggle('active');
        });
    }
    
    // Fechar menu ao clicar em link
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            navMenu.classList.remove('active');
            hamburger.classList.remove('active');
        });
    });
    
    // Header transparente no scroll
    const header = document.querySelector('.header');
    window.addEventListener('scroll', function() {
        if (window.scrollY > 100) {
            header.style.background = 'rgba(255, 255, 255, 0.98)';
        } else {
            header.style.background = 'rgba(255, 255, 255, 0.95)';
        }
    });
});

// Função para detectar se está no mobile
function isMobile() {
    return window.innerWidth <= 768;
}

// Animações ao scroll (Intersection Observer)
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observar elementos para animação
document.addEventListener('DOMContentLoaded', function() {
    const animatedElements = document.querySelectorAll('.product-card, .contact-card, .about-text');
    
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'all 0.6s ease';
        observer.observe(el);
    });
});

// Função para validar entrada do usuário
function validateInput(text) {
    if (!text || text.length > 200) {
        return false;
    }
    
    // Remove scripts maliciosos básicos
    const cleanText = text.replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '');
    return cleanText.trim();
}

// Função para formatar resposta do bot
function formatBotResponse(text) {
    // Adiciona quebras de linha e formatação básica
    return text.replace(/\n/g, '<br>');
}

// Função para debug (remover em produção)
function debug(message) {
    if (console && typeof console.log === 'function') {
        console.log('[Doce Encanto]:', message);
    }
}

// Easter egg - Konami code
let konamiCode = [];
const konamiSequence = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'KeyB', 'KeyA'];

document.addEventListener('keydown', function(e) {
    konamiCode.push(e.code);
    
    if (konamiCode.length > konamiSequence.length) {
        konamiCode.shift();
    }
    
    if (konamiCode.join('') === konamiSequence.join('')) {
        // Easter egg ativado!
        document.body.style.animation = 'rainbow 2s infinite';
        setTimeout(() => {
            document.body.style.animation = '';
        }, 6000);
        
        const easterEggData = {
            response: '🎉 Você encontrou o código secreto! Parabéns! 🍰',
            intent: 'easter_egg',
            confidence: 1.0,
            is_multiple: false
        };
        addBotMessage(easterEggData);
    }
});

// CSS para o easter egg
const style = document.createElement('style');
style.textContent = `
    @keyframes rainbow {
        0% { filter: hue-rotate(0deg); }
        100% { filter: hue-rotate(360deg); }
    }
`;
document.head.appendChild(style);