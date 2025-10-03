import streamlit as st
import re
import string
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.metrics.pairwise import cosine_similarity

# --- Tema da Doceria ---
st.markdown("""
    <style>
        body, .stApp {
            background: linear-gradient(135deg, #ff69b4 0%, #fff0f5 50%, #ffefd5 100%);
        }
        
        /* Força texto preto em todos os elementos */
        .stApp, .main .block-container, p, div, span, label, h1, h2, h3, h4, h5, h6 {
            color: #000000 !important;
        }
        
        /* Input e widgets com texto preto */
        .stTextInput input, .stSelectbox select, .stTextArea textarea {
            color: #000000 !important;
            background-color: #ffffff !important;
        }
        
        /* Sidebar com texto branco */
        .css-1d391kg, .css-1d391kg p, .css-1d391kg div, .sidebar .sidebar-content,
        .css-1d391kg *, section[data-testid="stSidebar"] *, 
        .css-ng1t4o *, .css-18e3th9 *, .css-1lcbmhc * {
            color: #ffffff !important;
        }
        
        .doceria-title {
            font-size: 4em;
            color: #8b4513 !important;
            font-weight: bold;
            text-align: center;
            margin-bottom: 0.2em;
            letter-spacing: 0.05em;
            text-shadow: 2px 2px 4px rgba(255,192,203,0.5);
        }
        .subtitle {
            font-size: 1.5em;
            color: #d2691e !important;
            text-align: center;
            margin-bottom: 1em;
            font-style: italic;
        }
        .chat-container {
            background-color: rgba(255,255,255,0.9);
            padding: 20px;
            border-radius: 15px;
            border: 3px solid #ffc0cb;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .chat-container * {
            color: #000000 !important;
        }
    </style>
    <div class="doceria-title">🍰 Doce Encanto 🧁</div>
    <div class="subtitle">Sua doceria favorita - Chatbot de atendimento</div>
""", unsafe_allow_html=True)
# --- Fim do bloco visual ---

# Dataset de intents para a doceria
intents = {
    "greeting": {
        "examples": [
            "oi",
            "olá",
            "bom dia",
            "boa tarde",
            "boa noite",
            "e aí",
            "fala",
            "hey",
            "hello",
            "oi doceria",
            "alô"
        ],
        "responses": [
            "🍰 Olá! Bem-vindo à Doce Encanto! Em que posso ajudar você hoje?",
            "🧁 Oi! Que alegria ter você aqui! Como posso adoçar seu dia?",
            "🍭 Seja bem-vindo à nossa doceria! O que posso fazer por você?"
        ]
    },
    "goodbye": {
        "examples": [
            "tchau",
            "até mais",
            "até logo",
            "falou",
            "adeus",
            "obrigado tchau",
            "até breve"
        ],
        "responses": [
            "🍯 Até mais! Volte sempre para mais doçura!",
            "🧁 Tchau! Obrigado pela visita à Doce Encanto!",
            "🍰 Até logo! Esperamos você em breve com novos sabores!"
        ]
    },
    "thanks": {
        "examples": [
            "obrigado",
            "muito obrigado",
            "vlw",
            "agradecido",
            "valeu",
            "obrigada"
        ],
        "responses": [
            "🍭 Por nada! Foi um prazer atendê-lo!",
            "🧁 Disponha sempre! Estamos aqui para adoçar seu dia!",
            "🍰 De nada! Volte sempre que quiser algo doce!"
        ]
    },
    "menu": {
        "examples": [
            "qual o cardápio?",
            "que doces vocês tem?",
            "o que vocês vendem?",
            "quais os produtos?",
            "menu",
            "cardápio",
            "doces disponíveis",
            "que sabores tem?"
        ],
        "responses": [
            "🍰 Temos bolos, tortas, brigadeiros, beijinhos, cupcakes, cookies, brownies e muito mais! Qual tipo de doce você procura?",
            "🧁 Nossa especialidade são bolos personalizados, mas também temos docinhos para festa, sobremesas geladas e doces artesanais!",
            "🍭 Oferecemos: bolos (chocolate, morango, coco), brigadeiros gourmet, tortas doces, mousses e doces para festas!"
        ]
    },
    "hours": {
        "examples": [
            "que horas vocês abrem?",
            "qual o horário de funcionamento?",
            "vocês abrem hoje?",
            "horário",
            "que horas fecha?",
            "funcionamento"
        ],
        "responses": [
            "🕘 Abrimos de segunda a sábado das 8h às 19h, e domingo das 9h às 17h!",
            "🕒 Funcionamos seg-sáb: 8h-19h e domingo: 9h-17h. Venha nos visitar!",
            "⏰ Estamos abertos de segunda a sábado das 8h às 19h, domingo das 9h às 17h!"
        ]
    },
    "payment": {
        "examples": [
            "quais formas de pagamento?",
            "aceitam cartão?",
            "posso pagar no cartão?",
            "pix disponível?",
            "como pagar?",
            "aceita dinheiro?"
        ],
        "responses": [
            "💳 Aceitamos cartão (débito/crédito), PIX, dinheiro e até vale-refeição!",
            "💰 Você pode pagar com cartão, PIX, dinheiro ou vale-alimentação!",
            "🏪 Formas de pagamento: cartão, PIX, dinheiro e cartões de benefício!"
        ]
    },
    "delivery": {
        "examples": [
            "fazem entrega?",
            "delivery disponível?",
            "entregam em casa?",
            "posso pedir pelo whatsapp?",
            "como fazer pedido?"
        ],
        "responses": [
            "🚚 Sim! Fazemos delivery na região central. Taxa de entrega R$ 5,00. Pedidos pelo WhatsApp: (11) 99999-9999",
            "🛵 Entregamos sim! Área de cobertura até 5km da loja. Entre em contato: (11) 99999-9999",
            "📱 Delivery disponível! Ligue (11) 99999-9999 ou peça pelo WhatsApp. Taxa: R$ 5,00"
        ]
    },
    "prices": {
        "examples": [
            "quanto custa?",
            "qual o preço?",
            "valores",
            "preço do bolo",
            "quanto é?",
            "tabela de preços"
        ],
        "responses": [
            "💰 Bolos personalizados a partir de R$ 45,00. Docinhos R$ 2,50 cada. Quer saber de algo específico?",
            "🏷️ Temos opções para todos os bolsos! Bolos simples R$ 25,00, gourmet R$ 45,00+. O que você procura?",
            "💵 Brigadeiros R$ 2,50, cupcakes R$ 8,00, tortas individuais R$ 12,00. Precisa de algo específico?"
        ]
    },
    "orders": {
        "examples": [
            "quero fazer um pedido",
            "como encomendar?",
            "posso encomendar um bolo?",
            "fazer encomenda",
            "pedido personalizado"
        ],
        "responses": [
            "📋 Que ótimo! Para pedidos personalizados, preciso saber: sabor, tamanho, data e tema. Me conte mais!",
            "🎂 Adoramos fazer bolos especiais! Qual ocasião? Quantas pessoas? Tem preferência de sabor?",
            "📞 Para encomendas, ligue (11) 99999-9999 ou venha à loja! Precisamos de 48h de antecedência."
        ]
    },
    "location": {
        "examples": [
            "onde vocês ficam?",
            "endereço da loja",
            "como chegar?",
            "localização",
            "onde é a doceria?"
        ],
        "responses": [
            "📍 Estamos na Rua das Flores, 123 - Centro. Próximo ao shopping! Tem estacionamento na rua.",
            "🗺️ Endereço: Rua das Flores, 123 - Centro. Entre a padaria e a farmácia, fácil de achar!",
            "📌 Ficamos na Rua das Flores, 123. Ponto de referência: em frente à praça central!"
        ]
    },
    "fallback": {
        "examples": [
            "..."],
        "responses": [
            "🤔 Desculpe, não entendi bem. Você quer saber sobre nossos doces, horários, preços ou fazer um pedido?",
            "😅 Não compreendi. Posso ajudar com: cardápio, preços, horários, entregas ou encomendas. O que você precisa?"
        ]
    }
}

# transformar em dataframe simples (utterance, intent)
import pandas as pd
rows = []
for intent, v in intents.items():
    for ex in v["examples"]:
        rows.append({"text": ex, "intent": intent})

df = pd.DataFrame(rows)

# downloads (apenas na primeira execução)
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

stop_words = set(stopwords.words('portuguese')) if 'portuguese' in nltk.corpus.stopwords.fileids() else set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()


def normalize_text(text):
    """Lowercase, remove punctuation/extra spaces, tokenize, lemmatize (se possível)."""
    text = text.lower()
    text = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', text)
    tokens = nltk.word_tokenize(text)
    tokens = [t for t in tokens if t.isalpha()]
    tokens = [t for t in tokens if t not in stop_words]
    # nota: WordNetLemmatizer funciona melhor em inglês; para português usar lemmatizers dedicados
    tokens = [lemmatizer.lemmatize(t) for t in tokens]
    return ' '.join(tokens)

df['text_norm'] = df['text'].apply(normalize_text)

tfidf_vect = TfidfVectorizer()
X_tfidf = tfidf_vect.fit_transform(df['text_norm'])

def retrieve_response(query, vect=tfidf_vect, utter_vecs=X_tfidf, df=df, topk=1, threshold=0.6):
    """Retorna a resposta de maior similaridade; se menor que threshold, responde fallback."""
    q = normalize_text(query)
    qv = vect.transform([q])
    sims = cosine_similarity(qv, utter_vecs).flatten()
    idx_sorted = np.argsort(-sims)
    if sims[idx_sorted[0]] >= threshold:
        chosen_idx = idx_sorted[0]
        intent = df.iloc[chosen_idx]['intent']
        resp = np.random.choice(intents[intent]['responses'])
        return resp, intent, sims[idx_sorted[0]]
    else:
        return intents['fallback']['responses'][0], 'fallback', sims[idx_sorted[0]]

# Interface da Doceria
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1,3,1])
with col2:
    st.markdown("### 🍰 Converse conosco! 🧁")
    st.markdown("*Pergunte sobre nossos doces, horários, preços ou faça seu pedido!*")

# Área de chat
user = st.text_input('💬 Digite sua mensagem:', placeholder="Ex: Que doces vocês têm? Qual o horário? Quero fazer um pedido...")

if user:
    # Processamento da mensagem
    response, intent, confidence = retrieve_response(user)
    
    # Exibição das mensagens em formato de chat
    st.markdown("---")
    
    # Mensagem do usuário
    st.markdown(f"""
    <div style="background-color: #ffefd5; padding: 10px; border-radius: 10px; margin: 5px 0; border-left: 4px solid #ff69b4;">
        <strong>🧑‍💼 Você:</strong> {user}
    </div>
    """, unsafe_allow_html=True)
    
    # Resposta do bot
    st.markdown(f"""
    <div style="background-color: #fff0f5; padding: 10px; border-radius: 10px; margin: 5px 0; border-left: 4px solid #8b4513;">
        <strong>🤖 Doce Encanto:</strong> {response}
    </div>
    """, unsafe_allow_html=True)
    
    # Informações técnicas (expansível)
    with st.expander("📊 Informações técnicas"):
        st.write(f'**Texto processado:** {normalize_text(user)}')
        st.write(f'**Intenção identificada:** {intent}')
        st.write(f'**Confiança:** {confidence:.2f}')

# Informações da loja na sidebar
st.sidebar.markdown("## 🏪 Doce Encanto")
st.sidebar.markdown("### 📞 Contato")
st.sidebar.markdown("📱 WhatsApp: (11) 99999-9999")
st.sidebar.markdown("📧 Email: contato@doceencanto.com")

st.sidebar.markdown("### 🕒 Horários")
st.sidebar.markdown("🗓️ Segunda a Sábado: 8h às 19h")
st.sidebar.markdown("🗓️ Domingo: 9h às 17h")

st.sidebar.markdown("### 📍 Endereço")
st.sidebar.markdown("🏠 Rua das Flores, 123 - Centro")

st.sidebar.markdown("### 🎂 Especialidades")
st.sidebar.markdown("🧁 Bolos personalizados")
st.sidebar.markdown("🍭 Docinhos para festa")
st.sidebar.markdown("🍰 Tortas artesanais")
st.sidebar.markdown("🍪 Cookies gourmet")

st.markdown('</div>', unsafe_allow_html=True)
