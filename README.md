# 🍰 Doce Encanto - Chatbot da Doceria

Sistema completo de chatbot para doceria Doce Encanto.

## 🏗️ Estrutura do Projeto

```
cp_5_IA_fernanda_carmona/
├── app.py                 # Back-end Flask
├── requirements.txt       # Dependências
├── README.md             # Este arquivo
├── templates/            # Front-end HTML
│   └── index.html        # Página principal
├── static/               # Arquivos estáticos
│   ├── css/
│   │   └── style.css     # Estilos CSS
│   └── js/
│       └── script.js     # JavaScript do front-end
└── venv_doceria/         # Ambiente virtual
```

## 🚀 Como Executar

### 1. Ative o ambiente virtual
```powershell
.\venv_doceria\Scripts\Activate.ps1
```

### 2. Instale o Flask
```powershell
pip install flask
```

### 3. Execute a aplicação
```powershell
python app.py
```

### 4. Acesse no navegador
- **URL:** http://localhost:5000
- **Endpoint de saúde:** http://localhost:5000/health

## 🎨 Características do Front-end

### Design Moderno e Profissional
- ✨ Layout responsivo com CSS Grid e Flexbox
- 🎨 Cores harmoniosas (rosa, dourado, marrom)
- 🍰 Tema de doceria com gradientes suaves
- 📱 Mobile-first e totalmente responsivo
- 🎭 Animações suaves e transições elegantes

### Componentes
- 🏠 **Header:** Navegação fixa com logo e menu
- 🌟 **Hero Section:** Apresentação principal com call-to-actions
- 🧁 **Products:** Grid de produtos com cards animados
- 💬 **Chatbot:** Interface de chat moderna e interativa
- 📖 **About:** Seção sobre a doceria
- 📞 **Contact:** Informações de contato organizadas
- 🔗 **Footer:** Links sociais e informações

### Tecnologias Front-end
- 📄 **HTML5** semântico e acessível
- 🎨 **CSS3** com variáveis CSS e animações
- ⚡ **JavaScript ES6+** vanilla
- 🔤 **Google Fonts** (Poppins)
- 🎯 **Font Awesome** para ícones

## 🔧 Características do Back-end

### Arquitetura Limpa
- 🏗️ Separação clara de responsabilidades
- 📊 Classe `DoceEncantoChatbot` isolada
- 🛡️ Tratamento robusto de erros
- 📝 Sistema de logging completo
- 🔍 Validações de entrada

### Funcionalidades
- 🤖 **Processamento NLP:** NLTK + scikit-learn
- 🎯 **Intenções:** 11 tipos de conversação
- 🔄 **API REST:** Endpoints JSON bem estruturados
- 📈 **Métricas:** Confidence score e logging
- 🏥 **Health Check:** Monitoramento da aplicação

### Tecnologias Back-end
- 🐍 **Flask** framework web
- 🧠 **NLTK** processamento de linguagem natural
- 📊 **scikit-learn** machine learning
- 🐼 **pandas** manipulação de dados
- 🔢 **numpy** computação numérica

## 💬 Funcionalidades do Chatbot

### Intenções Suportadas
1. 👋 **Saudações** - Cumprimentos e boas-vindas (20+ variações)
2. 👋 **Despedidas** - Finalizações cordiais (17+ variações)
3. 🙏 **Agradecimentos** - Respostas a agradecimentos (16+ variações)
4. 🍰 **Menu** - Informações sobre produtos (19+ variações)
5. 🕒 **Horários** - Funcionamento da loja (16+ variações)
6. 💳 **Pagamento** - Formas de pagamento aceitas (15+ variações)
7. 🚚 **Delivery** - Informações sobre entrega (16+ variações)
8. 💰 **Preços** - Valores dos produtos (18+ variações)
9. 📝 **Pedidos** - Como fazer encomendas (17+ variações)
10. 📍 **Localização** - Endereço e como chegar (15+ variações)
11. 📞 **Contato** - WhatsApp e email (15+ variações)
12. 🎉 **Promoções** - Ofertas e combos do dia (16+ variações)
13. 🌱 **Restrições Dietéticas** - Sem glúten, lactose, vegano (16+ variações)
14. 🎁 **Sugestões de Presente** - Caixas e cestas personalizadas (15+ variações)
15. 📅 **Validade/Conservação** - Prazo e armazenamento dos doces (16+ variações)
16. 💙 **Feedback/Reclamações** - Opiniões e sugestões (15+ variações)
17. 📖 **História da Doceria** - Fundação e trajetória (14+ variações)
18. 🌿 **Ingredientes** - Qualidade e origem dos produtos (16+ variações)
19. 🎨 **Decorações Personalizadas** - Temas e customizações (15+ variações)
20. 🎃 **Especiais Sazonais** - Doces para datas comemorativas (16+ variações)
21. 🎉 **Serviços para Festas** - Mesas de doces e eventos (15+ variações)

### Exemplos de Uso

#### Conversas Básicas
```
👤 "oiee doceria!"
🤖 "🧁 Oi! Que alegria ter você aqui! Como posso adoçar seu dia?"

👤 "q doces vcs tem ai?"
🤖 "🍰 Temos bolos personalizados, tortas, brigadeiros, beijinhos, cupcakes, cookies, brownies e muito mais!"

👤 "tem promocao hoje?"
🤖 "🎉 Sim! Toda terça temos 20% OFF em bolos de chocolate! E no combo 'Festa Doce' você economiza R$ 25,00!"
```

#### Necessidades Especiais
```
👤 "tem doces sem gluten?"
🤖 "🌱 Temos opções sem glúten, sem lactose e veganas! Bolos funcionais, brigadeiros de tâmaras e cupcakes sem açúcar!"

👤 "quero algo para dar de presente"
🤖 "🎁 Nossas caixas-presente são perfeitas! Temos a 'Caixa Amor' (R$ 45) e 'Caixa Família' (R$ 78)!"

👤 "quanto tempo dura o bolo?"
🤖 "📅 Nossos bolos frescos duram 3 dias na geladeira! Sempre em recipiente fechado!"
```

#### Serviços Avançados
```
👤 "fazem bolo do unicornio?"
🤖 "🎨 Amamos personalizar! Fazemos qualquer tema: unicórnio, futebol, princesas! Valor adicional R$ 15-30!"

👤 "preciso de doces para uma festa"
🤖 "🎉 Fazemos mesas completas! Buffet de doces para 50 pessoas por R$ 380! Inclui variedades e decoração!"
```

## 🛠️ Desenvolvimento

### Estrutura de Pastas
- **`/templates`** - Arquivos HTML (Jinja2)
- **`/static/css`** - Folhas de estilo
- **`/static/js`** - Scripts JavaScript
- **`/static/images`** - Imagens (futuro)

### Padrões de Código
- 📏 **PEP 8** para Python
- 🎯 **Semantic HTML** para markup
- 📱 **Mobile-first** CSS
- ♿ **Acessibilidade** em mente
- 🔒 **Segurança** validações de entrada

## 📱 Responsividade

### Breakpoints
- 📱 **Mobile:** < 480px
- 📟 **Tablet:** 481px - 768px  
- 💻 **Desktop:** > 769px

### Características Mobile
- 🍔 Menu hamburger
- 📏 Layout vertical
- 👆 Botões otimizados para toque
- 📜 Scroll suave entre seções

## 🎨 Personalização

### Variáveis CSS
```css
:root {
    --primary-color: #ff69b4;    /* Rosa principal */
    --secondary-color: #8b4513;  /* Marrom dos títulos */
    --accent-color: #ffc0cb;     /* Rosa claro */
    /* ... mais variáveis */
}
```

### Cores da Marca
- 🌸 **Primary:** #ff69b4 (Rosa vibrante)
- 🌰 **Secondary:** #8b4513 (Marrom chocolate)
- 🌺 **Accent:** #ffc0cb (Rosa claro)
- ⚪ **Light:** #fff0f5 (Rosa muito claro)

## 🚀 Próximos Passos

### Melhorias Futuras
- 📊 Dashboard administrativo
- 🗃️ Banco de dados para conversas
- 🔐 Sistema de autenticação
- 📈 Analytics de conversas
- 🎨 Temas personalizáveis
- 🌐 Suporte multi-idioma

### Integrações Futuras
- 📱 WhatsApp Business API 
- 📧 Sistema de email
- 💳 Gateway de pagamento
- 📦 Sistema de pedidos

## 📞 Suporte

Para dúvidas ou sugestões:
- 📧 Email: contato@doceencanto.com
- 📱 WhatsApp: (11) 99999-9999

---

**Desenvolvido com 💖**