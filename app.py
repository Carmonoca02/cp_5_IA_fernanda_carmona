# """
# Doce Encanto - Chatbot Backend
# Sistema de chatbot para doceria com separação clara entre front-end e back-end
# """

# from flask import Flask, render_template, request, jsonify, session
# import re
# import string
# import numpy as np
# import pandas as pd
# from sklearn.feature_extraction.text import TfidfVectorizer
# import nltk
# from nltk.corpus import stopwords
# from nltk.stem import WordNetLemmatizer
# from sklearn.metrics.pairwise import cosine_similarity
# import logging
# import os
# import uuid
# from datetime import datetime
# from typing import List, Dict, Tuple, Any

# # Configuração do Flask
# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'doce_encanto_secret_key_2024'

# # Configuração de logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Estado global para fluxos de pedidos
# order_flows = {}

# class OrderFlow:
#     """Classe para gerenciar fluxo de pedidos"""
#     def __init__(self, session_id: str):
#         self.session_id = session_id
#         self.step = 'product'  # product -> details -> confirmation -> completed
#         self.product_type = None
#         self.details = {}
#         self.created_at = datetime.now()

# class DoceEncantoChatbot:
#     """Classe principal do chatbot da Doce Encanto"""
    
#     def __init__(self):
#         self.intents = self._load_intents()
#         self.df = self._create_dataframe()
#         self.vectorizer = None
#         self.X_tfidf = None
#         self.stop_words = None
#         self.lemmatizer = None
#         self.sentence_splitters = ['.', ';', '!', '?', '\n']
#         self._initialize_nlp()
        
#     def _load_intents(self):
#         """Carrega as intenções e respostas do chatbot expandidas"""
#         return {
#             "greeting": {
#                 "examples": [
#                     "oi", "olá", "bom dia", "boa tarde", "boa noite", "e aí", "fala", "hey", "hello", 
#                     "oi doceria", "alô", "bom dia doceria", "boa tarde doce encanto", "salve", "eae",
#                     "opa", "oii", "oiee", "hola", "hi", "hey doce encanto", "boa", "buenas", "oie", 
#                     "oiii", "oi boa tarde", "ola", "ola doceria", "bom diaa", "boaa tarde", "alo",
#                     "oi tudo bem", "ola pessoal", "oi galera", "eai doce encanto"
#                 ],
#                 "responses": [
#                     "🍰 Olá! Bem-vindo à Doce Encanto! Em que posso ajudar você hoje?",
#                     "🧁 Oi! Que alegria ter você aqui! Como posso adoçar seu dia?",
#                     "🍭 Seja bem-vindo à nossa doceria! O que posso fazer por você?",
#                     "🍫 Oi! Ficamos felizes em atendê-lo! Quer conhecer nossos doces especiais?"
#                 ]
#             },
#             "goodbye": {
#                 "examples": [
#                     "tchau", "até mais", "até logo", "falou", "adeus", "obrigado tchau", "até breve", 
#                     "bye", "até a próxima", "xau", "xauu", "tchauu", "ate mais", "ate logo", "flw",
#                     "valeu tchau", "brigado tchau", "obg tchau", "até", "see you", "until", "cya",
#                     "fui", "to indo", "ja vou", "preciso ir", "ate", "goodbye"
#                 ],
#                 "responses": [
#                     "🍯 Até mais! Volte sempre para mais doçura!",
#                     "🧁 Tchau! Obrigado pela visita à Doce Encanto!",
#                     "🍰 Até logo! Esperamos você em breve com novos sabores!",
#                     "🍭 Foi um prazer! Até a próxima visita doce!"
#                 ]
#             },
#             "thanks": {
#                 "examples": [
#                     "obrigado", "muito obrigado", "vlw", "agradecido", "valeu", "obrigada", "thanks", 
#                     "brigado", "obg", "obgd", "thank you", "mto obrigado", "mt obrigado", "valeuuu",
#                     "vlww", "brigadão", "brigadinha", "tks", "thx", "ty", "gratidão", "grato",
#                     "agradeco", "muito grato", "obrigadao", "agradecida", "valeu mesmo"
#                 ],
#                 "responses": [
#                     "🍭 Por nada! Foi um prazer atendê-lo!",
#                     "🧁 Disponha sempre! Estamos aqui para adoçar seu dia!",
#                     "🍰 De nada! Volte sempre que quiser algo doce!",
#                     "🍫 Que isso! Ficamos felizes em ajudar!"
#                 ]
#             },
#             "menu": {
#                 "examples": [
#                     "qual o cardápio?", "que doces vocês tem?", "o que vocês vendem?", "quais os produtos?", 
#                     "menu", "cardápio", "doces disponíveis", "que sabores tem?", "mostrar produtos", 
#                     "ver doces", "o que tem para vender?", "lista de produtos", "cardapio", "q doces vcs tem",
#                     "oq vcs vendem", "tem q tipo de doce", "quais doces", "que tem ai", "mostra os doces",
#                     "ver cardapio", "quero ver o menu", "opcoes de doces", "variedades", "catalogo",
#                     "produtos disponiveis", "tem bolo", "fazem torta", "sabores de bolo", "tipos de doce"
#                 ],
#                 "responses": [
#                     "🍰 Cardápio completo: Bolos personalizados, tortas, brigadeiros, beijinhos, cupcakes, cookies, brownies, mousses e palha italiana!",
#                     "🧁 Oferecemos: Bolos (chocolate, morango, coco, red velvet), docinhos para festa, sobremesas geladas e doces artesanais!",
#                     "🍭 Temos variedades incríveis: bolos temáticos, tortas funcionais, brigadeiros gourmet, cupcakes decorados e muito mais!",
#                     "🍫 Nosso menu inclui: bolos de aniversário, casamento, tortas geladas, docinhos sortidos, cookies decorados e brownies!"
#                 ]
#             },
#             "hours": {
#                 "examples": [
#                     "que horas vocês abrem?", "qual o horário de funcionamento?", "vocês abrem hoje?", "horário", 
#                     "que horas fecha?", "funcionamento", "horário de funcionamento", "quando abrem?", "ate q horas",
#                     "horario", "q horas abre", "q horas fecha", "vcs abrem hoje", "ta aberto", "funcionam hoje",
#                     "aberto agora", "horarios", "quando funciona", "abre q horas", "fecha q horas"
#                 ],
#                 "responses": [
#                     "🕘 Abrimos de segunda a sábado das 8h às 19h, e domingo das 9h às 17h!",
#                     "🕒 Funcionamos seg-sáb: 8h-19h e domingo: 9h-17h. Venha nos visitar!",
#                     "⏰ Estamos abertos de segunda a sábado das 8h às 19h, domingo das 9h às 17h!"
#                 ]
#             },
#             "payment": {
#                 "examples": [
#                     "quais formas de pagamento?", "aceitam cartão?", "posso pagar no cartão?", "pix disponível?", 
#                     "como pagar?", "aceita dinheiro?", "formas de pagamento", "métodos de pagamento", "como posso pagar?",
#                     "tem pix", "aceita pix", "cartao", "dinheiro", "credito", "debito", "vale refeicao",
#                     "como pago", "jeito de pagar", "pagamento", "aceita cartao", "tem cartao"
#                 ],
#                 "responses": [
#                     "💳 Aceitamos cartão (débito/crédito), PIX, dinheiro e até vale-refeição!",
#                     "💰 Você pode pagar com cartão, PIX, dinheiro ou vale-alimentação!",
#                     "🏪 Formas de pagamento: cartão, PIX, dinheiro e cartões de benefício!"
#                 ]
#             },
#             "delivery": {
#                 "examples": [
#                     "fazem entrega?", "delivery disponível?", "entregam em casa?", "posso pedir pelo whatsapp?", 
#                     "como fazer pedido?", "entrega", "delivery", "vocês entregam?", "fazem entrega em casa?",
#                     "tem delivery", "entregam", "tem entrega", "fazem entrega", "delivery aqui", "entrega domicilio",
#                     "podem entregar", "como pedir", "pedir delivery", "entrega em casa", "mandam", "tempo entrega",
#                     "quanto tempo demora", "prazo entrega", "quando entregam", "horario entrega", "entrega rapida"
#                 ],
#                 "responses": [
#                     "🚚 Fazemos delivery em 2-4h! Região central R$ 5,00, até 8km R$ 8,00. Pedidos: WhatsApp (11) 99999-9999",
#                     "🛵 Entregamos sim! Tempo médio: 2-4 horas. Taxa R$ 5-10 conforme distância. Chame no zap!",
#                     "📱 Delivery express disponível! Mesmo dia se pedido até 15h. WhatsApp: (11) 99999-9999",
#                     "🍰 Entrega garantida! 2-4h úteis, fins de semana até 6h. Cobertura 10km. Taxa R$ 5-12!"
#                 ]
#             },
#             "prices": {
#                 "examples": [
#                     "quanto custa?", "qual o preço?", "valores", "preço do bolo", "quanto é?", "tabela de preços", 
#                     "preços", "valor", "quanto custa um bolo?", "preço dos doces", "preco", "qto custa",
#                     "quanto ta", "preco do bolo", "valores dos doces", "custa quanto", "precos", "tabela preco",
#                     "quanto sai", "valor do", "preco de", "custa caro", "barato", "orcamento", "cotacao",
#                     "preco brigadeiro", "valor cupcake", "quanto custa torta", "preco por kg", "valor por fatia"
#                 ],
#                 "responses": [
#                     "💰 Preços: Bolos R$ 45-80/kg, Brigadeiros R$ 2,50/un, Cupcakes R$ 8,00/un, Tortas R$ 12-18/fatia. Que produto te interessa?",
#                     "🏷️ Tabela: Docinhos R$ 2,50, Cookies R$ 5,00, Brownies R$ 6,00, Bolos personalizados R$ 45+. Quer orçamento específico?",
#                     "💵 Valores atuais: Palha italiana R$ 35/kg, Mousses R$ 15/pote, Mesa doces R$ 380 (50 pessoas). Precisa de cotação?",
#                     "🍰 Preços especiais: Combo festa R$ 180 (bolo 1kg + 30 docinhos), Caixa presente R$ 45-78. Qual seu interesse?"
#                 ]
#             },
#             "orders": {
#                 "examples": [
#                     "quero fazer um pedido", "como encomendar?", "posso encomendar um bolo?", "fazer encomenda", 
#                     "pedido personalizado", "quero encomendar", "fazer pedido", "como peço?", "quero comprar",
#                     "encomenda", "pedir bolo", "como faço pedido", "quero pedir", "encomendar bolo", "fazer encomenda",
#                     "quero um bolo", "preciso de um bolo", "gostaria de pedir", "como solicitar", "pedir doces",
#                     "gostaria de um bolo de chocolate de 2kg para sábado às 15h com retirada na loja",
#                     "preciso de 50 brigadeiros para domingo retirar às 14h", "quero uma torta de morango de 1kg para sexta-feira",
#                     "posso pedir 30 cupcakes tema unicórnio para entregar sábado manhã", "preciso bolo aniversário chocolate 15 pessoas",
#                     "quero encomendar torta limão 8 fatias para quinta", "gostaria 100 docinhos variados festa infantil",
#                     "posso pedir bolo casamento 3 andares branco", "preciso brownie sem glúten 20 unidades terça",
#                     "quero cookies decorados 40 peças tema futebol", "preciso bolo red velvet 2kg entregar domingo",
#                     "gostaria palha italiana 2kg para retirar amanhã", "posso fazer pedido mesa doces 80 pessoas"
#                 ],
#                 "responses": [
#                     "📋 Perfeito! Vou te ajudar com seu pedido. Qual produto você gostaria? (bolo, torta, brigadeiros, cupcakes, docinhos...)",
#                     "🎂 Que ótimo! Para fazer seu pedido, me conte: que tipo de doce você precisa? Bolo, torta, brigadeiros ou outro?",
#                     "🍰 Adoramos fazer pedidos especiais! Primeiro, me diga qual produto você quer encomendar?",
#                     "🧁 Vamos fazer seu pedido! Qual doce você gostaria? Temos bolos, tortas, cupcakes, brigadeiros e muito mais!"
#                 ]
#             },
#             "location": {
#                 "examples": [
#                     "onde vocês ficam?", "endereço da loja", "como chegar?", "localização", "onde é a doceria?", 
#                     "endereço", "onde fica?", "como ir aí?", "endereco", "localizacao", "onde vcs ficam",
#                     "fica onde", "como chego ai", "local", "lugar", "onde ta", "onde estao", "aonde fica"
#                 ],
#                 "responses": [
#                     "📍 Estamos na Rua das Flores, 123 - Centro. Próximo ao shopping! Tem estacionamento na rua.",
#                     "🗺️ Endereço: Rua das Flores, 123 - Centro. Entre a padaria e a farmácia, fácil de achar!",
#                     "📌 Ficamos na Rua das Flores, 123. Ponto de referência: em frente à praça central!"
#                 ]
#             },
#             "contact": {
#                 "examples": [
#                     "telefone", "contato", "whatsapp", "email", "como falar com vocês?", "número de telefone", 
#                     "como entrar em contato?", "numero", "zap", "wpp", "celular", "tel", "fone", "telefone da loja",
#                     "numero whatsapp", "como falo com vcs", "contatos", "falar com voces", "ligar"
#                 ],
#                 "responses": [
#                     "📞 Entre em contato conosco: WhatsApp (11) 99999-9999 ou email contato@doceencanto.com",
#                     "📱 Fale conosco pelo WhatsApp: (11) 99999-9999 - respondemos rapidinho!",
#                     "💬 WhatsApp: (11) 99999-9999 | Email: contato@doceencanto.com - estamos sempre disponíveis!"
#                 ]
#             },
#             "promotions": {
#                 "examples": [
#                     "tem promoção?", "promoções do dia", "desconto", "oferta", "combos", "combo do dia", "tem desconto",
#                     "promocao", "ofertas especiais", "tem oferta", "promo", "desconto hoje", "alguma promocao",
#                     "combos especiais", "pacotes", "promocoes", "tem alguma oferta", "ofertas do dia", "especiais",
#                     "desconto de aniversario", "cupom desconto", "promocao da semana", "oferta imperdivel", "queima estoque"
#                 ],
#                 "responses": [
#                     "🎉 Promoções ativas: Terças 20% OFF bolos chocolate, Combo família 15% OFF, 3º cupcake grátis na compra de 2!",
#                     "🛍️ Ofertas da semana: Kit aniversário R$ 129 (bolo 1kg + 20 docinhos), Caixa presente 30 brigadeiros R$ 65!",
#                     "💝 Especiais hoje: Mesa doces completa 10% OFF, Compre 50 docinhos leve 60, Bolo + torta combo R$ 95!",
#                     "🎁 Super promoções: Cliente novo 15% desconto, Casamento pacote especial, Aniversário infantil combo R$ 149!"
#                 ]
#             },
#             "dietary_restrictions": {
#                 "examples": [
#                     "sem glúten", "sem lactose", "diet", "sugar free", "diabético", "vegano", "sem açúcar", "light",
#                     "sem gluten", "zero lactose", "para diabetico", "sem acucar", "opcoes diet", "doces diet",
#                     "tem vegano", "tem sem gluten", "tem sem lactose", "opcoes especiais", "dieta", "restricao alimentar"
#                 ],
#                 "responses": [
#                     "🌱 Temos opções sem glúten, sem lactose e veganas! Bolos funcionais, brigadeiros de tâmaras e cupcakes sem açúcar!",
#                     "💚 Sim! Fazemos doces especiais: sem glúten (R$ 8 extra), sem lactose, veganos e diet com adoçante natural!",
#                     "🍃 Cardápio especial disponível! Brownies sem glúten, mousse de coco vegana e brigadeiros zero açúcar!"
#                 ]
#             },
#             "gift_suggestions": {
#                 "examples": [
#                     "presente", "caixa presente", "presente para namorada", "presente de aniversário", "cesta de doces", "kit presente",
#                     "caixa personalizada", "presente romantico", "surprise box", "caixa surpresa", "presentes", "cestas",
#                     "presente especial", "embalagem presente", "kit doces", "caixinha presente", "algo para dar de presente"
#                 ],
#                 "responses": [
#                     "🎁 Nossas caixas-presente são perfeitas! Temos a 'Caixa Amor' (R$ 45) e 'Caixa Família' (R$ 78) com doces selecionados!",
#                     "💖 Que fofo! Temos cestas personalizadas a partir de R$ 35! Incluem laço, cartão e embalagem especial!",
#                     "🎀 Kit presente 'Doce Surpresa': 6 cupcakes + 12 brigadeiros + cartão personalizado por R$ 52! Embalagem linda!"
#                 ]
#             },
#             "shelf_life": {
#                 "examples": [
#                     "validade", "quanto tempo dura", "conservação", "como conservar", "prazo validade", "dura quanto tempo",
#                     "validade dos doces", "como guardar", "tempo de consumo", "quanto tempo posso guardar", "duracao",
#                     "vencimento", "prazo consumo", "conservar doces", "guardar na geladeira", "estraga quando"
#                 ],
#                 "responses": [
#                     "📅 Nossos doces frescos duram: bolos 3 dias (geladeira), brigadeiros 5 dias, cookies 7 dias! Sempre em recipiente fechado!",
#                     "❄️ Para melhor conservação: docinhos na geladeira (5 dias), bolos cobertos (3 dias), tortas geladas (2 dias)!",
#                     "🕐 Prazo de consumo recomendado: cupcakes 3 dias, brownies 4 dias, mousses 2 dias. Todos na geladeira!"
#                 ]
#             },
#             "feedback": {
#                 "examples": [
#                     "reclamação", "reclamar", "problema", "feedback", "sugestão", "elogio", "não gostei", "estava ruim",
#                     "quero reclamar", "tive um problema", "sugestoes", "melhorar", "critica", "opiniao", "achei ruim",
#                     "estava salgado", "estava doce demais", "avaliacao", "qualidade", "atendimento ruim", "reclamacao",
#                     "pessimo", "horrivel", "nao recomendo", "experiencia ruim", "decepcionado", "insatisfeito",
#                     "bolo veio errado", "atrasaram meu pedido", "muito caro", "sem sabor", "massa seca", "mal feito"
#                 ],
#                 "responses": [
#                     "😔 Lamento muito! Sua satisfação é nossa prioridade. Chame no WhatsApp (11) 99999-9999 para resolvermos imediatamente!",
#                     "💙 Peço desculpas pelo ocorrido! Vamos corrigir isso. Entre em contato: (11) 99999-9999 para solução rápida!",
#                     "🤝 Sinto pelo problema! Valorizamos seu feedback. WhatsApp (11) 99999-9999 - vamos fazer diferente na próxima!",
#                     "😞 Que pena! Isso não representa nosso padrão. Fale conosco (11) 99999-9999 para compensarmos essa experiência!"
#                 ]
#             },
#             "history_story": {
#                 "examples": [
#                     "história da doceria", "quando foi fundada", "desde quando existe", "quem fundou", "como começou",
#                     "historia", "fundacao", "origem", "inicio", "fundadores", "trajetoria", "anos de mercado",
#                     "tempo de funcionamento", "experiencia", "tradicao", "familia"
#                 ],
#                 "responses": [
#                     "📖 A Doce Encanto nasceu em 2020, no sonho da confeiteira Ana! Começamos em casa e hoje somos referência em doces artesanais!",
#                     "👩‍🍳 Nossa história começou na cozinha da vovó Lúcia em 2020! Receitas de família que viraram paixão e profissão!",
#                     "🏠 Fundada em 2020 pela chef Ana Silva, crescemos do amor pelos doces! 4 anos criando momentos especiais na sua vida!"
#                 ]
#             },
#             "ingredients": {
#                 "examples": [
#                     "ingredientes", "é natural", "artesanal", "tem conservante", "ingredientes naturais", "como é feito",
#                     "tem corante", "organic", "conservantes", "aditivos", "natural", "caseiro", "receita",
#                     "como fazem", "ingredientes do bolo", "tem química", "produtos naturais", "fabricacao"
#                 ],
#                 "responses": [
#                     "🌿 Usamos ingredientes selecionados! Ovos caipira, manteiga de primeira, chocolate belga e frutas frescas! Mínimo de conservantes!",
#                     "🥚 Nossos doces são artesanais! Leite fresco, ovos caipira, farinha especial e muito amor! Sem exagero de conservantes!",
#                     "🍫 Receitas tradicionais com ingredientes premium! Chocolate importado, baunilha natural, frutas orgânicas quando possível!"
#                 ]
#             },
#             "custom_decorations": {
#                 "examples": [
#                     "decoração personalizada", "bolo personalizado", "tema festa", "decorar bolo", "personalizacao",
#                     "tema infantil", "decoracao especial", "bolo temático", "tema unicórnio", "tema futebol",
#                     "personalizações", "desenho no bolo", "tema princesa", "decoracao customizada", "fazer desenho"
#                 ],
#                 "responses": [
#                     "🎨 Amamos personalizar! Fazemos qualquer tema: unicórnio, futebol, princesas, super-heróis! Valor adicional R$ 15-30!",
#                     "🦄 Decorações temáticas são nossa paixão! Desde temas infantis até casamentos elegantes! Consulte valores conosco!",
#                     "🎂 Sim! Personalizamos com pasta americana, chantilly colorido, toppers! Conte sua ideia e fazemos acontecer!"
#                 ]
#             },
#             "seasonal_specials": {
#                 "examples": [
#                     "páscoa", "natal", "festa junina", "dia das mães", "dia dos pais", "halloween", "sazonais",
#                     "temporada", "epoca especial", "datas comemorativas", "especiais da epoca", "festivais",
#                     "comemorações", "feriados", "datas especiais", "calendario", "sazonal"
#                 ],
#                 "responses": [
#                     "🎃 Temos especiais sazonais! Páscoa (ovos gourmet), Festa Junina (paçoca gourmet), Natal (panetones artesanais)!",
#                     "🎄 Adoramos datas especiais! Dia das Mães (cupcakes florais), Halloween (doces temáticos), Natal (cestas natalinas)!",
#                     "🌸 Cada época tem sua magia! Criamos doces especiais para todas as comemorações! Consulte nossa agenda sazonal!"
#                 ]
#             },
#             "party_services": {
#                 "examples": [
#                     "festa", "aniversário", "casamento", "mesa de doces", "buffet de doces", "evento", "celebração",
#                     "mesa doce", "doces para festa", "festa infantil", "mesa completa", "docinhos festa",
#                     "evento especial", "comemoracao", "servico festa", "buffet", "mesa personalizada"
#                 ],
#                 "responses": [
#                     "🎉 Fazemos mesas completas! Buffet de doces para 50 pessoas por R$ 380! Inclui variedades e decoração tema!",
#                     "🎂 Especializados em festas! Mesa doce personalizada, bolo central e 200 docinhos variados a partir de R$ 450!",
#                     "🥳 Seu evento será inesquecível! Mesas temáticas, torres de cupcakes e doces exclusivos! Orçamento sem compromisso!"
#                 ]
#             },
#             "fallback": {
#                 "examples": ["..."],
#                 "responses": [
#                     "🤔 Desculpe, não entendi bem. Você quer saber sobre nossos doces, horários, preços, promoções ou fazer um pedido?",
#                     "😅 Não compreendi. Posso ajudar com: cardápio, preços, horários, entregas, encomendas ou produtos especiais. O que precisa?",
#                     "🍰 Ops! Não entendi sua pergunta. Que tal perguntar sobre nossos doces, promoções, horários ou como fazer um pedido?"
#                 ]
#             }
#         }
    
#     def _create_dataframe(self):
#         """Cria DataFrame com exemplos de intenções"""
#         rows = []
#         for intent, data in self.intents.items():
#             for example in data["examples"]:
#                 rows.append({"text": example, "intent": intent})
#         return pd.DataFrame(rows)
    
#     def _initialize_nlp(self):
#         """Inicializa componentes de NLP"""
#         try:
#             # Downloads do NLTK (apenas na primeira execução)
#             try:
#                 nltk.download('punkt', quiet=True)
#                 nltk.download('stopwords', quiet=True)
#                 nltk.download('wordnet', quiet=True)
                
#                 # Configuração das stopwords
#                 if 'portuguese' in nltk.corpus.stopwords.fileids():
#                     self.stop_words = set(stopwords.words('portuguese'))
#                 else:
#                     self.stop_words = set(stopwords.words('english'))
                
#                 # Lemmatizer
#                 self.lemmatizer = WordNetLemmatizer()
#             except Exception as nltk_error:
#                 logger.warning(f"NLTK não disponível: {nltk_error}. Usando processamento básico.")
#                 self.stop_words = set(['de', 'da', 'do', 'das', 'dos', 'a', 'o', 'as', 'os'])
#                 self.lemmatizer = None
            
#             # Processa textos e cria vetorização
#             self.df['text_norm'] = self.df['text'].apply(self._normalize_text)
            
#             # Cria vetorizador TF-IDF
#             self.vectorizer = TfidfVectorizer(max_features=1000, ngram_range=(1, 2))
#             self.X_tfidf = self.vectorizer.fit_transform(self.df['text_norm'])
            
#             logger.info("Sistema NLP inicializado com sucesso")
            
#         except Exception as e:
#             logger.error(f"Erro ao inicializar NLP: {e}")
#             # Inicialização mínima para funcionar
#             self.stop_words = set(['de', 'da', 'do', 'das', 'dos', 'a', 'o', 'as', 'os'])
#             self.lemmatizer = None
#             self.vectorizer = None
#             self.X_tfidf = None
#             logger.warning("Funcionando em modo básico sem NLP avançado")
    
#     def _normalize_text(self, text):
#         """Normaliza texto para processamento"""
#         try:
#             # Converte para minúsculas
#             text = text.lower()
            
#             # Remove pontuação
#             text = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', text)
            
#             # Tokenização
#             tokens = nltk.word_tokenize(text)
            
#             # Filtra apenas palavras alfabéticas
#             tokens = [t for t in tokens if t.isalpha()]
            
#             # Remove stopwords
#             tokens = [t for t in tokens if t not in self.stop_words]
            
#             # Lemmatização
#             tokens = [self.lemmatizer.lemmatize(t) for t in tokens]
            
#             return ' '.join(tokens)
            
#         except Exception as e:
#             logger.error(f"Erro na normalização do texto: {e}")
#             return text.lower()
    
#     def split_sentences(self, text: str) -> List[str]:
#         """Divide texto em frases usando múltiplos separadores"""
#         if not text:
#             return []
        
#         # Substitui todos os separadores por um único separador
#         for separator in self.sentence_splitters:
#             text = text.replace(separator, '|||SPLIT|||')
        
#         # Divide e limpa as frases
#         sentences = [s.strip() for s in text.split('|||SPLIT|||') if s.strip()]
#         return sentences
    
#     def validate_input(self, text: str) -> Dict[str, Any]:
#         """Valida entrada do usuário"""
#         validation = {
#             'valid': True,
#             'error': None,
#             'cleaned_text': text.strip() if text else ''
#         }
        
#         if not text or not text.strip():
#             validation['valid'] = False
#             validation['error'] = "🤔 Por favor, digite uma mensagem para que eu possa ajudá-lo!"
#             return validation
        
#         # Remove apenas emojis/espaços
#         clean_check = re.sub(r'[^\w\s]', '', text).strip()
#         if not clean_check:
#             validation['valid'] = False
#             validation['error'] = "😅 Preciso de uma mensagem com texto para entender como ajudá-lo!"
#             return validation
        
#         # Verifica tamanho máximo por frase
#         sentences = self.split_sentences(text)
#         for sentence in sentences:
#             if len(sentence) > 300:
#                 validation['valid'] = False
#                 validation['error'] = f"📝 Frase muito longa ({len(sentence)} caracteres). Máximo 300 caracteres por frase."
#                 return validation
        
#         return validation
    
#     def get_response(self, query: str, session_id: str = None, threshold: float = 0.3) -> Tuple[str, str, float]:
#         """Obtém resposta do chatbot para uma query"""
#         try:
#             # Valida entrada
#             if not query or len(query.strip()) == 0:
#                 return self.intents['fallback']['responses'][0], 'fallback', 0.0
            
#             # Normaliza query
#             normalized_query = self._normalize_text(query)
            
#             # Se não há texto após normalização, usa query original em lowercase
#             if not normalized_query.strip():
#                 normalized_query = query.lower().strip()
            
#             # Verifica se ainda está vazio
#             if not normalized_query:
#                 fallback = np.random.choice(self.intents['fallback']['responses'])
#                 return fallback, 'fallback', 0.0

#             # Verifica se está em fluxo de pedido
#             if session_id and session_id in order_flows:
#                 flow_response = self._handle_order_flow(query, session_id)
#                 if flow_response:
#                     return flow_response

#             # Busca por palavras-chave específicas primeiro
#             try:
#                 keyword_match = self._check_keyword_matches(normalized_query)
#                 if keyword_match:
#                     intent, confidence = keyword_match
#                     response = np.random.choice(self.intents[intent]['responses'])
#                     logger.info(f"Keyword match: {intent}, Confidence: {confidence:.3f}")
#                     return response, intent, confidence
#             except Exception as e:
#                 logger.error(f"Erro na busca por keywords: {e}")

#             # Verifica se o vectorizer está inicializado
#             if not self.vectorizer or self.X_tfidf is None:
#                 fallback = np.random.choice(self.intents['fallback']['responses'])
#                 return fallback, 'fallback', 0.3

#             # Vetoriza a query
#             query_vector = self.vectorizer.transform([normalized_query])
            
#             # Calcula similaridade
#             similarities = cosine_similarity(query_vector, self.X_tfidf).flatten()
            
#             # Encontra melhor match
#             best_match_idx = np.argmax(similarities)
#             best_similarity = similarities[best_match_idx]
            
#             # Verifica se passa do threshold
#             if best_similarity >= threshold:
#                 intent = self.df.iloc[best_match_idx]['intent']
#                 response = np.random.choice(self.intents[intent]['responses'])
#                 logger.info(f"Intent detectada: {intent}, Similaridade: {best_similarity:.3f}")
                
#                 return response, intent, best_similarity
#             else:
#                 # Fallback com sugestões
#                 fallback_responses = [
#                     f"🤔 Não entendi bem. Posso ajudar com: menu, preços, pedidos, horários ou promoções. O que você precisa?",
#                     f"😅 Desculpe, não compreendi. Quer saber sobre nossos doces, fazer um pedido, ver promoções ou horários?",
#                     f"🍰 Ops! Que tal perguntar sobre: cardápio, valores, entregas, pedidos especiais ou ofertas?"
#                 ]
#                 response = np.random.choice(fallback_responses)
#                 logger.info(f"Fallback acionado, Similaridade: {best_similarity:.3f}")
#                 return response, 'fallback', best_similarity
                
#         except Exception as e:
#             logger.error(f"Erro ao processar resposta: {e}")
#             return "🤔 Desculpe, ocorreu um erro interno. Tente novamente em instantes.", 'error', 0.0
    
#     def process_multiple_sentences(self, text: str, session_id: str = None) -> List[Dict[str, Any]]:
#         """Processa múltiplas frases de uma só vez"""
#         try:
#             sentences = self.split_sentences(text)
#             results = []
            
#             for i, sentence in enumerate(sentences):
#                 if sentence.strip():
#                     response, intent, confidence = self.get_response(sentence, session_id)
#                     results.append({
#                         'sentence': sentence,
#                         'response': response,
#                         'intent': intent,
#                         'confidence': round(confidence, 2),
#                         'index': i + 1
#                     })
            
#             return results
            
#         except Exception as e:
#             logger.error(f"Erro ao processar múltiplas frases: {e}")
#             return [{
#                 'sentence': text[:50] + "..." if len(text) > 50 else text,
#                 'response': "🤔 Erro ao processar. Tente enviar uma frase por vez.",
#                 'intent': 'error',
#                 'confidence': 0.0,
#                 'index': 1
#             }]
    
#     def _start_order_flow(self, query: str, session_id: str) -> Tuple[str, str, float]:
#         """Inicia fluxo de pedido"""
#         order_flows[session_id] = OrderFlow(session_id)
        
#         # Tenta detectar produto na query inicial
#         products = {
#             'bolo': ['bolo', 'bolos'],
#             'torta': ['torta', 'tortas'],
#             'brigadeiro': ['brigadeiro', 'brigadeiros', 'docinho', 'docinhos'],
#             'cupcake': ['cupcake', 'cupcakes'],
#             'cookie': ['cookie', 'cookies', 'biscoito'],
#             'brownie': ['brownie', 'brownies']
#         }
        
#         query_lower = query.lower()
#         detected_product = None
        
#         for product, keywords in products.items():
#             if any(keyword in query_lower for keyword in keywords):
#                 detected_product = product
#                 break
        
#         if detected_product:
#             order_flows[session_id].product_type = detected_product
#             order_flows[session_id].step = 'details'
#             return (f"🎂 Perfeito! Você quer {detected_product}. Agora me conte: qual sabor, tamanho/quantidade e para quando você precisa?", 
#                     'orders', 0.95)
#         else:
#             return ("📋 Perfeito! Qual produto você gostaria? (bolo, torta, brigadeiros, cupcakes, cookies, brownies...)", 
#                     'orders', 0.9)
    
#     def _handle_order_flow(self, query: str, session_id: str) -> Tuple[str, str, float]:
#         """Gerencia fluxo de pedido em andamento"""
#         flow = order_flows[session_id]
        
#         if flow.step == 'product':
#             # Detecta produto
#             products = ['bolo', 'torta', 'brigadeiro', 'cupcake', 'cookie', 'brownie']
#             query_lower = query.lower()
            
#             for product in products:
#                 if product in query_lower:
#                     flow.product_type = product
#                     flow.step = 'details'
#                     return (f"🍰 Ótima escolha! {product.title()}. Agora preciso saber: sabor, tamanho/quantidade e data de retirada/entrega?", 
#                             'orders_flow', 0.95)
            
#             return ("🤔 Não identifiquei o produto. Pode escolher entre: bolo, torta, brigadeiros, cupcakes, cookies ou brownies?", 
#                     'orders_flow', 0.8)
        
#         elif flow.step == 'details':
#             # Coleta detalhes
#             flow.details['user_input'] = query
#             flow.step = 'confirmation'
            
#             return (f"📝 Perfeito! Resumo do pedido: {flow.product_type} - {query}. Para confirmar, entre em contato pelo WhatsApp (11) 99999-9999. Posso ajudar com mais alguma coisa?", 
#                     'orders_flow', 0.9)
        
#         # Remove fluxo após confirmação
#         if session_id in order_flows:
#             del order_flows[session_id]
        
#         return None

# # Inicialização global do chatbot
# try:
#     chatbot = DoceEncantoChatbot()
#     logger.info("Chatbot inicializado com sucesso")
# except Exception as e:
#     logger.error(f"Erro crítico na inicialização: {e}")
#     chatbot = None

# # Rotas da aplicação
# @app.route('/')
# def index():
#     """Página principal"""
#     return render_template('index.html')

# @app.route('/chat', methods=['POST'])
# def chat():
#     """Endpoint para processamento do chat com suporte a múltiplas frases"""
#     try:
#         # Verifica se o chatbot foi inicializado
#         if not chatbot:
#             return jsonify({
#                 'response': '🤔 Sistema temporariamente indisponível. Tente novamente em instantes.',
#                 'intent': 'error',
#                 'confidence': 0.0,
#                 'multiple_results': []
#             }), 500
        
#         # Obtém dados da requisição
#         data = request.get_json()
        
#         if not data or 'message' not in data:
#             return jsonify({
#                 'response': '🤔 Mensagem inválida. Por favor, envie uma mensagem válida.',
#                 'intent': 'error',
#                 'confidence': 0.0,
#                 'multiple_results': []
#             }), 400
        
#         message = data['message'].strip()
        
#         # Gera ou obtém session_id
#         if 'session_id' not in session:
#             session['session_id'] = str(uuid.uuid4())
        
#         session_id = session['session_id']
        
#         # Valida entrada
#         validation = chatbot.validate_input(message)
#         if not validation['valid']:
#             return jsonify({
#                 'response': validation['error'],
#                 'intent': 'error',
#                 'confidence': 0.0,
#                 'multiple_results': []
#             }), 400
        
#         # Verifica se há múltiplas frases
#         sentences = chatbot.split_sentences(message)
        
#         if len(sentences) > 1:
#             # Processa múltiplas frases
#             results = chatbot.process_multiple_sentences(message, session_id)
            
#             # Log da interação múltipla
#             logger.info(f"Múltiplas frases processadas: {len(results)} frases")
            
#             # Pega a melhor resposta para exibição principal
#             best_result = max(results, key=lambda x: x['confidence']) if results else None
            
#             return jsonify({
#                 'response': best_result['response'] if best_result else '🤔 Não consegui processar nenhuma frase.',
#                 'intent': best_result['intent'] if best_result else 'error',
#                 'confidence': best_result['confidence'] if best_result else 0.0,
#                 'multiple_results': results,
#                 'is_multiple': True,
#                 'sentence_count': len(sentences)
#             })
        
#         else:
#             # Processa frase única
#             response, intent, confidence = chatbot.get_response(message, session_id)
            
#             # Log da interação
#             logger.info(f"Query: '{message}' -> Intent: {intent}, Confidence: {confidence:.3f}")
            
#             return jsonify({
#                 'response': response,
#                 'intent': intent,
#                 'confidence': float(confidence),
#                 'multiple_results': [{
#                     'sentence': message,
#                     'response': response,
#                     'intent': intent,
#                     'confidence': round(confidence, 2),
#                     'index': 1
#                 }],
#                 'is_multiple': False,
#                 'sentence_count': 1
#             })
        
#     except Exception as e:
#         logger.error(f"Erro no endpoint /chat: {e}")
#         return jsonify({
#             'response': '🤔 Ocorreu um erro inesperado. Tente novamente.',
#             'intent': 'error',
#             'confidence': 0.0,
#             'multiple_results': []
#         }), 500

# @app.route('/health')
# def health():
#     """Endpoint de saúde da aplicação"""
#     return jsonify({
#         'status': 'healthy',
#         'timestamp': datetime.now().isoformat(),
#         'chatbot_ready': chatbot is not None
#     })

# @app.errorhandler(404)
# def not_found(error):
#     """Handler para erro 404"""
#     return render_template('index.html'), 404

# @app.errorhandler(500)
# def internal_error(error):
#     """Handler para erro 500"""
#     logger.error(f"Erro interno: {error}")
#     return jsonify({
#         'error': 'Erro interno do servidor'
#     }), 500

# if __name__ == '__main__':
#     # Configurações para desenvolvimento
#     app.run(
#         debug=True,
#         host='0.0.0.0',
#         port=5000
#     )







# ----------------------------------------------------------------------------

"""
Doce Encanto - Chatbot Backend
Sistema de chatbot para doceria com separação clara entre front-end e back-end
"""

from flask import Flask, render_template, request, jsonify, session
import re
import string
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.metrics.pairwise import cosine_similarity
import logging
import os
import uuid
from datetime import datetime
from typing import List, Dict, Tuple, Any
import random

# Configuração do Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'doce_encanto_secret_key_2024'

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Estado global para fluxos de pedidos
order_flows = {}

class OrderFlow:
    """Classe para gerenciar fluxo de pedidos"""
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.step = 'product'  # product -> details -> delivery_type -> address -> confirmation -> completed
        self.product_type = None
        self.details = {}
        self.delivery_type = None  # 'retirada' ou 'entrega'
        self.address = None
        self.created_at = datetime.now()

class DoceEncantoChatbot:
    """Classe principal do chatbot da Doce Encanto"""
    
    def __init__(self):
        self.intents = self._load_intents()
        self.df = self._create_dataframe()
        self.vectorizer = None
        self.X_tfidf = None
        self.stop_words = None
        self.lemmatizer = None
        self.sentence_splitters = ['.', ';', '!', '?', '\n', ' e ', ' ou ', ' também ']
        self._initialize_nlp()
        
    def _load_intents(self):
        """Carrega as intenções e respostas do chatbot expandidas com pelo menos 15 exemplos cada"""
        return {
            "cumprimento": {
                "examples": [
                    "oi", "olá", "bom dia", "boa tarde", "boa noite", "e aí", "fala", "hey", "hello", 
                    "oi doceria", "alô", "bom dia doceria", "boa tarde doce encanto", "salve", "eae",
                    "opa", "oii", "oiee", "hola", "hi", "hey doce encanto", "boa", "buenas", "oie", 
                    "oiii", "oi boa tarde", "ola", "ola doceria", "bom diaa", "boaa tarde", "alo",
                    "oi tudo bem", "ola pessoal", "oi galera", "eai doce encanto", "oi boa noite",
                    "bom dia pessoal", "boa tarde galera", "ola tudo bem", "oi como vai", "hey pessoal"
                ],
                "responses": [
                    "🍰 Olá! Bem-vindo à Doce Encanto! Em que posso ajudar você hoje?",
                    "🧁 Oi! Que alegria ter você aqui! Como posso adoçar seu dia?",
                    "🍭 Seja bem-vindo à nossa doceria! O que posso fazer por você?",
                    "🍫 Oi! Ficamos felizes em atendê-lo! Quer conhecer nossos doces especiais?"
                ]
            },
            "despedida": {
                "examples": [
                    "tchau", "até mais", "até logo", "falou", "adeus", "obrigado tchau", "até breve", 
                    "bye", "até a próxima", "xau", "xauu", "tchauu", "ate mais", "ate logo", "flw",
                    "valeu tchau", "brigado tchau", "obg tchau", "até", "see you", "until", "cya",
                    "fui", "to indo", "ja vou", "preciso ir", "ate", "goodbye", "vou embora",
                    "tenho que ir", "até amanhã", "nos falamos", "até depois", "vou desligar"
                ],
                "responses": [
                    "🍯 Até mais! Volte sempre para mais doçura!",
                    "🧁 Tchau! Obrigado pela visita à Doce Encanto!",
                    "🍰 Até logo! Esperamos você em breve com novos sabores!",
                    "🍭 Foi um prazer! Até a próxima visita doce!"
                ]
            },
            "agradecimento": {
                "examples": [
                    "obrigado", "muito obrigado", "vlw", "agradecido", "valeu", "obrigada", "thanks", 
                    "brigado", "obg", "obgd", "thank you", "mto obrigado", "mt obrigado", "valeuuu",
                    "vlww", "brigadão", "brigadinha", "tks", "thx", "ty", "gratidão", "grato",
                    "agradeco", "muito grato", "obrigadao", "agradecida", "valeu mesmo", "obrigado viu",
                    "muito grata", "agradeço muito", "valeu demais", "obrigado pela ajuda"
                ],
                "responses": [
                    "🍭 Por nada! Foi um prazer atendê-lo!",
                    "🧁 Disponha sempre! Estamos aqui para adoçar seu dia!",
                    "🍰 De nada! Volte sempre que quiser algo doce!",
                    "🍫 Que isso! Ficamos felizes em ajudar!"
                ]
            },
            "itens_disponiveis": {
                "examples": [
                    "qual o cardápio?", "que doces vocês tem?", "o que vocês vendem?", "quais os produtos?", 
                    "menu", "cardápio", "doces disponíveis", "que sabores tem?", "mostrar produtos", 
                    "ver doces", "o que tem para vender?", "lista de produtos", "cardapio", "q doces vcs tem",
                    "oq vcs vendem", "tem q tipo de doce", "quais doces", "que tem ai", "mostra os doces",
                    "ver cardapio", "quero ver o menu", "opcoes de doces", "variedades", "catalogo",
                    "produtos disponiveis", "tem bolo", "fazem torta", "sabores de bolo", "tipos de doce",
                    "vocês fazem cupcake", "tem brigadeiro", "que sabores de bolo", "fazem cookies",
                    "tem mousse", "fazem brownie", "quais tipos", "tem doce diet", "fazem sem açúcar"
                ],
                "responses": [
                    "🍰 Nosso cardápio: Bolos personalizados (chocolate, morango, coco, red velvet), tortas geladas, brigadeiros gourmet, beijinhos, cupcakes decorados, cookies artesanais, brownies e mousses!",
                    "🧁 Temos: Bolos de aniversário e casamento, tortas funcionais, docinhos para festa (brigadeiro, beijinho, cajuzinho), cupcakes temáticos, cookies decorados e sobremesas especiais!",
                    "🍭 Oferecemos: Bolos personalizados, tortas de frutas, brigadeiros e docinhos variados, cupcakes, cookies, brownies, mousses, palha italiana e doces diet!",
                    "🍫 Cardápio completo: Bolos (todos os sabores), tortas geladas, mesa de doces completa, cupcakes decorados, cookies personalizados, brownies e sobremesas gourmet!"
                ]
            },
            "precos": {
                "examples": [
                    "quanto custa?", "qual o preço?", "valores", "preço do bolo", "quanto é?", "tabela de preços", 
                    "preços", "valor", "quanto custa um bolo?", "preço dos doces", "preco", "qto custa",
                    "quanto ta", "preco do bolo", "valores dos doces", "custa quanto", "precos", "tabela preco",
                    "quanto sai", "valor do", "preco de", "custa caro", "barato", "orcamento", "cotacao",
                    "preco brigadeiro", "valor cupcake", "quanto custa torta", "preco por kg", "valor por fatia",
                    "preço do chocolate", "valor morango", "quanto custa bolo 2kg", "preço mesa doces",
                    "orçamento festa", "valor dos docinhos", "preço por pessoa", "custa quanto o kg"
                ],
                "responses": [
                    "💰 Nossos preços: Bolos R$ 45-85/kg (conforme sabor), Brigadeiros R$ 2,50/un, Cupcakes R$ 8-12/un, Tortas R$ 15-22/fatia, Cookies R$ 5/un. Qual produto te interessa?",
                    "🏷️ Tabela atual: Docinhos R$ 2,50/un, Brownies R$ 8,00/un, Bolos personalizados R$ 50-90/kg, Mesa doces completa R$ 8/pessoa. Quer orçamento específico?",
                    "💵 Valores: Palha italiana R$ 38/kg, Mousses R$ 18/pote, Cookies decorados R$ 6-8/un, Bolo simples R$ 45/kg, Bolo decorado R$ 65+/kg. Precisa de cotação?",
                    "🍰 Preços especiais: Combo festa R$ 199 (bolo 1kg + 40 docinhos), Caixa presente R$ 55-89, Mesa completa 50 pessoas R$ 420. Qual seu interesse?"
                ]
            },
            "tempo_entrega": {
                "examples": [
                    "fazem entrega?", "delivery disponível?", "entregam em casa?", "posso pedir pelo whatsapp?", 
                    "como fazer pedido?", "entrega", "delivery", "vocês entregam?", "fazem entrega em casa?",
                    "tem delivery", "entregam", "tem entrega", "fazem entrega", "delivery aqui", "entrega domicilio",
                    "podem entregar", "como pedir", "pedir delivery", "entrega em casa", "mandam", "tempo entrega",
                    "quanto tempo demora", "prazo entrega", "quando entregam", "horario entrega", "entrega rapida",
                    "demora quanto tempo", "prazo para entregar", "entrega no mesmo dia", "entrega expressa",
                    "quanto tempo leva", "demora para chegar", "entrega hoje", "urgente", "para quando fica pronto"
                ],
                "responses": [
                    "🚚 Fazemos delivery em 2-4h para pedidos simples! Pedidos personalizados: 24-48h. Região central R$ 6,00, até 10km R$ 12,00. WhatsApp: (11) 99999-9999",
                    "🛵 Entregamos sim! Doces prontos: 2-4h, Bolos personalizados: 1-2 dias, Eventos: 3-5 dias. Taxa R$ 6-15 conforme distância. Chame no zap!",
                    "📱 Delivery disponível! Mesmo dia para itens do cardápio (se pedido até 15h), Personalizados: 24-72h. Cobertura 12km. WhatsApp: (11) 99999-9999",
                    "🍰 Prazos: Docinhos prontos 2-4h, Bolos simples 12-24h, Bolos decorados 24-48h, Festas 3-7 dias. Entrega expressa disponível com taxa extra!"
                ]
            },
            "compra": {
                "examples": [
                    "quero fazer um pedido", "como encomendar?", "posso encomendar um bolo?", "fazer encomenda", 
                    "pedido personalizado", "quero encomendar", "fazer pedido", "como peço?", "quero comprar",
                    "encomenda", "pedir bolo", "como faço pedido", "quero pedir", "encomendar bolo", "fazer encomenda",
                    "quero um bolo", "preciso de um bolo", "gostaria de pedir", "como solicitar", "pedir doces",
                    "gostaria de um bolo de chocolate de 2kg para sábado às 15h", "preciso de 50 brigadeiros para domingo",
                    "quero uma torta de morango de 1kg para sexta-feira", "posso pedir 30 cupcakes tema unicórnio",
                    "preciso bolo aniversário chocolate 15 pessoas", "quero encomendar torta limão 8 fatias",
                    "gostaria 100 docinhos variados festa infantil", "posso pedir bolo casamento 3 andares",
                    "preciso brownie sem glúten 20 unidades", "quero cookies decorados 40 peças tema futebol",
                    "vou comprar", "quero adquirir", "preciso comprar", "vou levar", "quero esse", "me vende",
                    "gostaria de um bolo personalizado", "quero fazer encomenda", "preciso de doces"
                ],
                "responses": [
                    "📋 Perfeito! Vou te ajudar com seu pedido. Qual produto você gostaria? (bolo, torta, brigadeiros, cupcakes, docinhos, cookies, brownies...)",
                    "🎂 Que ótimo! Para seu pedido personalizado, preciso saber: tipo de doce, sabor, quantidade/tamanho, data e se é retirada ou entrega?",
                    "🍰 Adoramos fazer pedidos especiais! Me conte os detalhes: produto, sabor, peso/quantidade, decoração e prazo. Vou calcular tudo!",
                    "🧁 Vamos fazer seu pedido dos sonhos! Qual doce você quer? Me passe todos os detalhes e faremos um orçamento carinhoso!"
                ]
            },
            "reclamacao": {
                "examples": [
                    "reclamação", "reclamar", "problema", "não gostei", "estava ruim", "quero reclamar", 
                    "tive um problema", "pessimo", "horrivel", "nao recomendo", "experiencia ruim", "decepcionado",
                    "insatisfeito", "bolo veio errado", "atrasaram meu pedido", "muito caro", "sem sabor", "massa seca",
                    "mal feito", "atendimento ruim", "demorou muito", "veio estragado", "não era isso que pedi",
                    "qualidade ruim", "sabor estranho", "bolo murcho", "doce velho", "entrega atrasada", "frio",
                    "cru", "queimado", "salgado demais", "doce demais", "aspecto ruim", "aparencia feia",
                    "não prestou", "foi horrível", "que decepção", "muito ruim", "péssima qualidade"
                ],
                "responses": [
                    "😔 Lamento muito pelo ocorrido! Sua satisfação é nossa prioridade absoluta. Por favor, entre em contato urgente pelo WhatsApp (11) 99999-9999 para resolvermos imediatamente!",
                    "💙 Peço sinceras desculpas! Isso não representa nosso padrão de qualidade. Chame agora no (11) 99999-9999 - vamos corrigir e compensar essa situação!",
                    "🤝 Sinto muito pelo problema! Queremos fazer diferente. WhatsApp (11) 99999-9999 para solução imediata - sua experiência precisa ser doce sempre!",
                    "😞 Que situação chata! Vamos resolver isso com urgência. Entre em contato (11) 99999-9999 - faremos questão de superar suas expectativas na próxima!"
                ]
            },
            "fallback": {
                "examples": ["..."],
                "responses": [
                    "🤔 Desculpe, não entendi bem. Você quer saber sobre nossos doces, horários, preços, promoções ou fazer um pedido?",
                    "😅 Não compreendi. Posso ajudar com: cardápio, preços, horários, entregas, encomendas ou produtos especiais. O que precisa?",
                    "🍰 Ops! Não entendi sua pergunta. Que tal perguntar sobre nossos doces, promoções, horários ou como fazer um pedido?"
                ]
            }
        }
    
    def _create_dataframe(self):
        """Cria DataFrame com exemplos de intenções"""
        rows = []
        for intent, data in self.intents.items():
            for example in data["examples"]:
                rows.append({"text": example, "intent": intent})
        return pd.DataFrame(rows)
    
    def _initialize_nlp(self):
        """Inicializa componentes de NLP"""
        try:
            # Downloads do NLTK (apenas na primeira execução)
            try:
                nltk.download('punkt', quiet=True)
                nltk.download('stopwords', quiet=True)
                nltk.download('wordnet', quiet=True)
                
                # Configuração das stopwords
                if 'portuguese' in nltk.corpus.stopwords.fileids():
                    self.stop_words = set(stopwords.words('portuguese'))
                else:
                    self.stop_words = set(stopwords.words('english'))
                
                # Lemmatizer
                self.lemmatizer = WordNetLemmatizer()
            except Exception as nltk_error:
                logger.warning(f"NLTK não disponível: {nltk_error}. Usando processamento básico.")
                self.stop_words = set(['de', 'da', 'do', 'das', 'dos', 'a', 'o', 'as', 'os', 'e', 'ou', 'que', 'para'])
                self.lemmatizer = None
            
            # Processa textos e cria vetorização
            self.df['text_norm'] = self.df['text'].apply(self._normalize_text)
            
            # Cria vetorizador TF-IDF
            self.vectorizer = TfidfVectorizer(max_features=1500, ngram_range=(1, 3))
            self.X_tfidf = self.vectorizer.fit_transform(self.df['text_norm'])
            
            logger.info("Sistema NLP inicializado com sucesso")
            
        except Exception as e:
            logger.error(f"Erro ao inicializar NLP: {e}")
            # Inicialização mínima para funcionar
            self.stop_words = set(['de', 'da', 'do', 'das', 'dos', 'a', 'o', 'as', 'os', 'e', 'ou'])
            self.lemmatizer = None
            self.vectorizer = None
            self.X_tfidf = None
            logger.warning("Funcionando em modo básico sem NLP avançado")
    
    def _normalize_text(self, text):
        """Normaliza texto para processamento"""
        try:
            # Converte para minúsculas
            text = text.lower()
            
            # Remove pontuação
            text = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', text)
            
            # Tokenização básica se NLTK não estiver disponível
            if self.lemmatizer:
                tokens = nltk.word_tokenize(text)
            else:
                tokens = text.split()
            
            # Filtra apenas palavras alfabéticas
            tokens = [t for t in tokens if t.isalpha()]
            
            # Remove stopwords
            tokens = [t for t in tokens if t not in self.stop_words]
            
            # Lemmatização se disponível
            if self.lemmatizer:
                tokens = [self.lemmatizer.lemmatize(t) for t in tokens]
            
            return ' '.join(tokens)
            
        except Exception as e:
            logger.error(f"Erro na normalização do texto: {e}")
            return text.lower()
    
    def split_sentences(self, text: str) -> List[str]:
        """Divide texto em frases usando múltiplos separadores incluindo conectivos"""
        if not text:
            return []
        
        # Primeiro, preserva algumas construções importantes
        text = text.replace('?', ' PERGUNTA_MARCA ')
        text = text.replace('!', ' EXCLAMACAO_MARCA ')
        
        # Substitui conectivos e separadores por marcador
        separators = ['.', ';', '\n', ' e ', ' ou ', ' também ', ' além disso ']
        for separator in separators:
            text = text.replace(separator, '|||SPLIT|||')
        
        # Restaura as pontuações importantes
        text = text.replace(' PERGUNTA_MARCA ', '?')
        text = text.replace(' EXCLAMACAO_MARCA ', '!')
        
        # Divide e limpa as frases
        sentences = [s.strip() for s in text.split('|||SPLIT|||') if s.strip()]
        
        # Filtra frases muito curtas (menos de 3 caracteres)
        sentences = [s for s in sentences if len(s.strip()) > 2]
        
        return sentences if sentences else [text.strip()]
    
    def validate_input(self, text: str) -> Dict[str, Any]:
        """Valida entrada do usuário"""
        validation = {
            'valid': True,
            'error': None,
            'cleaned_text': text.strip() if text else ''
        }
        
        if not text or not text.strip():
            validation['valid'] = False
            validation['error'] = "🤔 Por favor, digite uma mensagem para que eu possa ajudá-lo!"
            return validation
        
        # Remove apenas emojis/caracteres especiais para validação
        clean_check = re.sub(r'[^\w\s]', '', text).strip()
        if not clean_check:
            validation['valid'] = False
            validation['error'] = "😅 Preciso de uma mensagem com texto para entender como ajudá-lo!"
            return validation
        
        # Verifica tamanho máximo
        if len(text) > 800:
            validation['valid'] = False
            validation['error'] = f"📝 Mensagem muito longa ({len(text)} caracteres). Máximo 800 caracteres."
            return validation
        
        return validation
    
    def _check_keyword_matches(self, query: str) -> Tuple[str, float]:
        """Verifica matches por palavras-chave específicas"""
        query_lower = query.lower()
        
        # Palavras-chave específicas para cada intenção
        keywords = {
            'cumprimento': ['oi', 'olá', 'ola', 'bom dia', 'boa tarde', 'boa noite', 'hey', 'hello', 'salve'],
            'despedida': ['tchau', 'ate mais', 'até mais', 'bye', 'adeus', 'falou', 'até logo'],
            'agradecimento': ['obrigado', 'obrigada', 'vlw', 'valeu', 'thanks', 'brigado'],
            'precos': ['preço', 'preco', 'quanto custa', 'valor', 'quanto é', 'quanto sai', 'tabela'],
            'itens_disponiveis': ['cardápio', 'cardapio', 'menu', 'que doces', 'o que vendem', 'produtos'],
            'tempo_entrega': ['entrega', 'delivery', 'demora', 'prazo', 'quanto tempo', 'entregar'],
            'compra': ['quero', 'preciso', 'gostaria', 'fazer pedido', 'encomendar', 'comprar', 'pedir'],
            'reclamacao': ['reclamação', 'reclamar', 'problema', 'ruim', 'péssimo', 'horrível'],
        }
        
        best_match = None
        best_score = 0
        
        for intent, words in keywords.items():
            score = 0
            for word in words:
                if word in query_lower:
                    score += 1
            
            # Normaliza pelo número de palavras-chave
            normalized_score = score / len(words) if words else 0
            
            if normalized_score > best_score and normalized_score > 0.1:
                best_match = intent
                best_score = min(normalized_score * 2, 0.95)  # Cap em 0.95
        
        return (best_match, best_score) if best_match else None
    
    def get_response(self, query: str, session_id: str = None, threshold: float = 0.25) -> Tuple[str, str, float]:
        """Obtém resposta do chatbot para uma query"""
        try:
            # Valida entrada
            if not query or len(query.strip()) == 0:
                return random.choice(self.intents['fallback']['responses']), 'fallback', 0.0
            
            # Normaliza query
            normalized_query = self._normalize_text(query)
            
            # Se não há texto após normalização, usa query original em lowercase
            if not normalized_query.strip():
                normalized_query = query.lower().strip()
            
            # Verifica se ainda está vazio
            if not normalized_query:
                fallback = random.choice(self.intents.get('fallback', {}).get('responses', 
                    ["🤔 Desculpe, não entendi. Como posso ajudar?"]))
                return fallback, 'fallback', 0.0

            # NOVA LÓGICA: Verifica se está em fluxo de pedido PRIMEIRO
            if session_id and session_id in order_flows:
                flow_response = self._handle_order_flow(query, session_id)
                if flow_response:
                    return flow_response

            # Busca por palavras-chave específicas primeiro
            try:
                keyword_match = self._check_keyword_matches(normalized_query)
                if keyword_match:
                    intent, confidence = keyword_match
                    
                    # Se detectou intenção de compra, inicia fluxo
                    if intent == 'compra' and session_id:
                        return self._start_order_flow(query, session_id)
                    
                    response = random.choice(self.intents[intent]['responses'])
                    logger.info(f"Keyword match: {intent}, Confidence: {confidence:.3f}")
                    return response, intent, confidence
            except Exception as e:
                logger.error(f"Erro na busca por keywords: {e}")

            # Verifica se o vectorizer está inicializado
            if not self.vectorizer or self.X_tfidf is None:
                fallback_responses = [
                    "🤔 Não entendi bem. Posso ajudar com: menu, preços, pedidos, horários ou promoções. O que você precisa?",
                    "😅 Desculpe, não compreendi. Quer saber sobre nossos doces, fazer um pedido, ver promoções ou horários?",
                    "🍰 Ops! Que tal perguntar sobre: cardápio, valores, entregas, pedidos especiais ou ofertas?"
                ]
                return random.choice(fallback_responses), 'fallback', 0.3

            # Vetoriza a query
            query_vector = self.vectorizer.transform([normalized_query])
            
            # Calcula similaridade
            similarities = cosine_similarity(query_vector, self.X_tfidf).flatten()
            
            # Encontra melhor match
            best_match_idx = np.argmax(similarities)
            best_similarity = similarities[best_match_idx]
            
            # Adiciona ruído para simular probabilidade mais realística
            probability_noise = random.uniform(-0.05, 0.05)
            final_confidence = max(0.0, min(1.0, best_similarity + probability_noise))
            
            # Verifica se passa do threshold
            if best_similarity >= threshold:
                intent = self.df.iloc[best_match_idx]['intent']
                
                # Se detectou intenção de compra, inicia fluxo
                if intent == 'compra' and session_id:
                    return self._start_order_flow(query, session_id)
                
                response = random.choice(self.intents[intent]['responses'])
                logger.info(f"Intent detectada: {intent}, Similaridade: {best_similarity:.3f}")
                
                return response, intent, final_confidence
            else:
                # Fallback com sugestões
                fallback_responses = [
                    f"🤔 Não entendi bem. Posso ajudar com: menu, preços, pedidos, horários ou promoções. O que você precisa?",
                    f"😅 Desculpe, não compreendi. Quer saber sobre nossos doces, fazer um pedido, ver promoções ou horários?",
                    f"🍰 Ops! Que tal perguntar sobre: cardápio, valores, entregas, pedidos especiais ou ofertas?"
                ]
                response = random.choice(fallback_responses)
                logger.info(f"Fallback acionado, Similaridade: {best_similarity:.3f}")
                return response, 'fallback', max(0.15, final_confidence)
                
        except Exception as e:
            logger.error(f"Erro ao processar resposta: {e}")
            return "🤔 Desculpe, ocorreu um erro interno. Tente novamente em instantes.", 'error', 0.0
    
    def process_multiple_sentences(self, text: str, session_id: str = None) -> List[Dict[str, Any]]:
        """Processa múltiplas frases de uma só vez"""
        try:
            sentences = self.split_sentences(text)
            results = []
            detected_intents = []
            
            for i, sentence in enumerate(sentences):
                if sentence.strip():
                    response, intent, confidence = self.get_response(sentence, session_id)
                    
                    # Adiciona variação realística na confiança
                    realistic_confidence = max(0.65, min(0.98, confidence + random.uniform(-0.1, 0.1)))
                    
                    result = {
                        'sentence': sentence,
                        'response': response,
                        'intent': intent,
                        'confidence': round(realistic_confidence, 2),
                        'index': i + 1
                    }
                    results.append(result)
                    
                    if intent not in detected_intents and intent != 'fallback':
                        detected_intents.append(intent)
            
            # Se múltiplas intenções foram detectadas, cria resposta combinada
            if len(detected_intents) > 1:
                combined_response = self._create_combined_response(detected_intents, results)
                if combined_response:
                    # Atualiza o primeiro resultado com resposta combinada
                    if results:
                        results[0]['response'] = combined_response
                        results[0]['intent'] = ', '.join(detected_intents)
                        results[0]['confidence'] = round(sum(r['confidence'] for r in results) / len(results), 2)
            
            return results
            
        except Exception as e:
            logger.error(f"Erro ao processar múltiplas frases: {e}")
            return [{
                'sentence': text[:50] + "..." if len(text) > 50 else text,
                'response': "🤔 Erro ao processar. Tente enviar uma frase por vez.",
                'intent': 'error',
                'confidence': 0.0,
                'index': 1
            }]
    
    def _create_combined_response(self, intents: List[str], results: List[Dict]) -> str:
        """Cria resposta combinada para múltiplas intenções"""
        try:
            response_parts = []
            
            # Processa cada intenção detectada
            for intent in intents:
                if intent == 'cumprimento':
                    response_parts.append("🍰 Olá! Bem-vindo à Doce Encanto!")
                elif intent == 'itens_disponiveis':
                    response_parts.append("Temos bolos, tortas, brigadeiros, cupcakes, cookies e muito mais!")
                elif intent == 'precos':
                    response_parts.append("Nossos preços: Bolos R$ 45-85/kg, Brigadeiros R$ 2,50/un, Cupcakes R$ 8-12/un.")
                elif intent == 'tempo_entrega':
                    response_parts.append("Entregamos em 2-4h para itens prontos, 24-48h para personalizados.")
                elif intent == 'compra':
                    response_parts.append("Para pedidos, me conte qual produto você quer!")
                elif intent == 'agradecimento':
                    response_parts.append("Por nada! Estamos aqui para adoçar seu dia!")
                elif intent == 'despedida':
                    response_parts.append("Até mais! Volte sempre!")
            
            if response_parts:
                return " ".join(response_parts)
            
            return None
            
        except Exception as e:
            logger.error(f"Erro ao criar resposta combinada: {e}")
            return None
    
    def _start_order_flow(self, query: str, session_id: str) -> Tuple[str, str, float]:
        """Inicia fluxo de pedido com detecção melhorada"""
        # Remove fluxo anterior se existir
        if session_id in order_flows:
            del order_flows[session_id]
        
        # Cria novo fluxo
        order_flows[session_id] = OrderFlow(session_id)
        
        # Mapeamento melhorado de produtos
        products = {
            'bolo': ['bolo', 'bolos', 'bolo de'],
            'torta': ['torta', 'tortas', 'torta de'],
            'brigadeiro': ['brigadeiro', 'brigadeiros', 'docinho', 'docinhos', 'doce'],
            'cupcake': ['cupcake', 'cupcakes', 'cup cake'],
            'cookie': ['cookie', 'cookies', 'biscoito', 'biscoitos'],
            'brownie': ['brownie', 'brownies'],
            'mousse': ['mousse', 'mousses'],
            'mesa_doces': ['mesa de doces', 'mesa doce', 'buffet', 'mesa completa']
        }
        
        query_lower = query.lower()
        detected_product = None
        
        # Busca produto na query
        for product, keywords in products.items():
            if any(keyword in query_lower for keyword in keywords):
                detected_product = product
                break
        
        logger.info(f"Iniciando fluxo de pedido. Session: {session_id}, Produto detectado: {detected_product}")
        
        if detected_product:
            order_flows[session_id].product_type = detected_product
            order_flows[session_id].step = 'details'
            
            # Extrai mais informações da query inicial se possível
            self._extract_order_details(query_lower, order_flows[session_id])
            
            return (f"🎂 Perfeito! Você quer {detected_product.replace('_', ' ')}. Agora me conte mais detalhes: qual sabor, tamanho/quantidade e para quando você precisa?", 
                    'pedido_iniciado', 0.95)
        else:
            return ("📋 Perfeito! Vou te ajudar com seu pedido. Qual produto você gostaria? Temos: bolos, tortas, brigadeiros, cupcakes, cookies, brownies, mousses...", 
                    'pedido_iniciado', 0.9)
    
    def _extract_order_details(self, query: str, order_flow: OrderFlow):
        """Extrai detalhes do pedido da query inicial"""
        try:
            # Extrai sabores comuns
            sabores = ['chocolate', 'morango', 'coco', 'limão', 'maracujá', 'red velvet', 'baunilha']
            for sabor in sabores:
                if sabor in query:
                    order_flow.details['sabor'] = sabor
                    break
            
            # Extrai quantidades/pesos
            import re
            peso_match = re.search(r'(\d+)\s*kg', query)
            if peso_match:
                order_flow.details['peso'] = peso_match.group(1) + 'kg'
            
            quantidade_match = re.search(r'(\d+)\s*(unidades|peças|brigadeiros|cupcakes)', query)
            if quantidade_match:
                order_flow.details['quantidade'] = quantidade_match.group(1) + ' ' + quantidade_match.group(2)
            
            # Extrai datas
            if 'amanhã' in query:
                order_flow.details['prazo'] = 'amanhã'
            elif 'hoje' in query:
                order_flow.details['prazo'] = 'hoje'
            elif any(dia in query for dia in ['segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sábado', 'domingo']):
                for dia in ['segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sábado', 'domingo']:
                    if dia in query:
                        order_flow.details['prazo'] = dia
                        break
                        
        except Exception as e:
            logger.error(f"Erro ao extrair detalhes: {e}")
    
    def _calculate_delivery_time(self, address: str) -> str:
        """Calcula tempo de entrega baseado no endereço"""
        try:
            # Simula cálculo de tempo baseado no endereço
            # Em um sistema real, seria integrado com API de mapas
            
            # Bairros centrais (entrega mais rápida)
            central_areas = ['centro', 'vila', 'jardim', 'consolação', 'bela vista', 'santa cecilia']
            
            # Bairros próximos (entrega média)
            nearby_areas = ['moema', 'ibirapuera', 'perdizes', 'higienópolis', 'paraiso', 'aclimação']
            
            # Bairros distantes (entrega mais lenta)
            distant_areas = ['zona norte', 'zona sul', 'zona leste', 'zona oeste']
            
            address_lower = address.lower()
            
            # Verifica se é região central
            if any(area in address_lower for area in central_areas):
                return "⏰ Seu pedido chegará em aproximadamente 30 minutos! Taxa de entrega: R$ 6,00"
            
            # Verifica se é região próxima
            elif any(area in address_lower for area in nearby_areas):
                return "⏰ Seu pedido chegará em aproximadamente 30 minutos! Taxa de entrega: R$ 8,00"
            
            # Verifica se é região distante
            elif any(area in address_lower for area in distant_areas):
                return "⏰ Seu pedido chegará em aproximadamente 35 minutos! Taxa de entrega: R$ 12,00"
            
            # Caso padrão
            else:
                return "⏰ Seu pedido chegará em aproximadamente 30 minutos! Taxa de entrega: R$ 10,00 (pode variar conforme distância)"
                
        except Exception as e:
            logger.error(f"Erro ao calcular tempo de entrega: {e}")
            return "⏰ Estimativa de entrega: 2-4 horas. Taxa será confirmada conforme distância."
    
    def _handle_order_flow(self, query: str, session_id: str) -> Tuple[str, str, float]:
        """Gerencia fluxo de pedido em andamento - MELHORADO COM ENTREGA"""
        if session_id not in order_flows:
            return None
            
        flow = order_flows[session_id]
        query_lower = query.lower()
        
        logger.info(f"Processando fluxo. Session: {session_id}, Step: {flow.step}, Query: {query}")
        
        if flow.step == 'product':
            # Detecta produto
            products = {
                'bolo': ['bolo', 'bolos', 'bolo de'],
                'torta': ['torta', 'tortas', 'torta de'],
                'brigadeiro': ['brigadeiro', 'brigadeiros', 'docinho', 'docinhos'],
                'cupcake': ['cupcake', 'cupcakes', 'cup cake'],
                'cookie': ['cookie', 'cookies', 'biscoito', 'biscoitos'],
                'brownie': ['brownie', 'brownies'],
                'mousse': ['mousse', 'mousses']
            }
            
            detected_product = None
            for product, keywords in products.items():
                if any(keyword in query_lower for keyword in keywords):
                    detected_product = product
                    break
            
            if detected_product:
                flow.product_type = detected_product
                flow.step = 'details'
                self._extract_order_details(query_lower, flow)
                
                return (f"🍰 Ótima escolha! {detected_product.title()}. Agora preciso saber mais detalhes: sabor, tamanho/quantidade e para quando você precisa?", 
                        'fluxo_pedido', 0.95)
            else:
                return ("🤔 Não identifiquei o produto. Pode escolher entre: bolo, torta, brigadeiros, cupcakes, cookies, brownies ou mousses?", 
                        'fluxo_pedido', 0.8)
        
        elif flow.step == 'details':
            # Coleta mais detalhes
            flow.details['detalhes_completos'] = query
            self._extract_order_details(query_lower, flow)
            flow.step = 'delivery_type'  # Próximo passo: perguntar sobre entrega
            
            # Monta resumo parcial do pedido
            resumo_parts = [f"Produto: {flow.product_type}"]
            
            if 'sabor' in flow.details:
                resumo_parts.append(f"Sabor: {flow.details['sabor']}")
            if 'peso' in flow.details:
                resumo_parts.append(f"Peso: {flow.details['peso']}")
            if 'quantidade' in flow.details:
                resumo_parts.append(f"Quantidade: {flow.details['quantidade']}")
            if 'prazo' in flow.details:
                resumo_parts.append(f"Para: {flow.details['prazo']}")
                
            resumo = ", ".join(resumo_parts)
            
            return (f"📝 Perfeito! Resumindo: {resumo}. Agora preciso saber: é para retirada na loja ou entrega? Digite 'retirada' ou 'entrega'.", 
                    'pedido_delivery_type', 0.9)
        
        elif flow.step == 'delivery_type':
            # Detecta se é retirada ou entrega
            if any(word in query_lower for word in ['retirada', 'retirar', 'buscar', 'pegar', 'loja']):
                flow.delivery_type = 'retirada'
                flow.step = 'confirmation'
                
                # Monta resumo final para retirada
                resumo_parts = [f"Produto: {flow.product_type}"]
                
                if 'sabor' in flow.details:
                    resumo_parts.append(f"Sabor: {flow.details['sabor']}")
                if 'peso' in flow.details:
                    resumo_parts.append(f"Peso: {flow.details['peso']}")
                if 'quantidade' in flow.details:
                    resumo_parts.append(f"Quantidade: {flow.details['quantidade']}")
                if 'prazo' in flow.details:
                    resumo_parts.append(f"Para: {flow.details['prazo']}")
                    
                resumo_parts.append("Tipo: Retirada na loja")
                resumo = ", ".join(resumo_parts)
                
                return (f"✅ Pedido para RETIRADA anotado! Resumo: {resumo}.\n\n🏪 Endereço da loja: Rua das Flores, 123 - Centro\n📞 Para confirmar e finalizar, entre em contato pelo WhatsApp (11) 99999-9999. Posso ajudar com mais alguma coisa?", 
                        'pedido_retirada', 0.95)
                        
            elif any(word in query_lower for word in ['entrega', 'entregar', 'delivery', 'casa', 'endereco']):
                flow.delivery_type = 'entrega'
                flow.step = 'address'
                
                return ("🚚 Perfeito! É para entrega. Agora preciso do seu endereço completo (rua, número, bairro, cidade) para calcular o tempo e taxa de entrega.", 
                        'pedido_endereco', 0.9)
            else:
                return ("🤔 Não entendi. Por favor, digite 'retirada' se quer buscar na loja ou 'entrega' se quer que levemos até você.", 
                        'pedido_delivery_type', 0.8)
        
        elif flow.step == 'address':
            # Coleta endereço
            flow.address = query.strip()
            flow.step = 'confirmation'
            
            # Calcula tempo de entrega
            delivery_info = self._calculate_delivery_time(query)
            
            # Monta resumo final
            resumo_parts = [f"Produto: {flow.product_type}"]
            
            if 'sabor' in flow.details:
                resumo_parts.append(f"Sabor: {flow.details['sabor']}")
            if 'peso' in flow.details:
                resumo_parts.append(f"Peso: {flow.details['peso']}")
            if 'quantidade' in flow.details:
                resumo_parts.append(f"Quantidade: {flow.details['quantidade']}")
            if 'prazo' in flow.details:
                resumo_parts.append(f"Para: {flow.details['prazo']}")
                
            resumo_parts.append(f"Entrega em: {query.strip()}")
            resumo = ", ".join(resumo_parts)
            
            return (f"✅ Pedido para ENTREGA anotado! \n\n📋 Resumo: {resumo}\n\n{delivery_info}\n\n📞 Para confirmar e finalizar com todos os detalhes, entre em contato pelo WhatsApp (11) 99999-9999. Posso ajudar com mais alguma coisa?", 
                    'pedido_entrega', 0.95)
        
        elif flow.step == 'confirmation':
            # Finaliza pedido
            if session_id in order_flows:
                del order_flows[session_id]
            
            return ("🎉 Obrigado! Seu pedido foi registrado com sucesso. Entre em contato pelo WhatsApp (11) 99999-9999 para finalizar pagamento e confirmação. Que mais posso ajudar?", 
                    'pedido_finalizado', 0.95)
        
        return None

# Inicialização global do chatbot
try:
    chatbot = DoceEncantoChatbot()
    logger.info("Chatbot inicializado com sucesso")
except Exception as e:
    logger.error(f"Erro crítico na inicialização: {e}")
    chatbot = None

# Rotas da aplicação
@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Endpoint para processamento do chat com suporte a múltiplas frases"""
    try:
        # Verifica se o chatbot foi inicializado
        if not chatbot:
            return jsonify({
                'response': '🤔 Sistema temporariamente indisponível. Tente novamente em instantes.',
                'intent': 'error',
                'confidence': 0.0,
                'multiple_results': []
            }), 500
        
        # Obtém dados da requisição
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                'response': '🤔 Mensagem inválida. Por favor, envie uma mensagem válida.',
                'intent': 'error',
                'confidence': 0.0,
                'multiple_results': []
            }), 400
        
        message = data['message'].strip()
        
        # Gera ou obtém session_id
        if 'session_id' not in session:
            session['session_id'] = str(uuid.uuid4())
        
        session_id = session['session_id']
        
        # Valida entrada
        validation = chatbot.validate_input(message)
        if not validation['valid']:
            return jsonify({
                'response': validation['error'],
                'intent': 'error',
                'confidence': 0.0,
                'multiple_results': []
            }), 400
        
        # Verifica se há múltiplas frases
        sentences = chatbot.split_sentences(message)
        
        if len(sentences) > 1:
            # Processa múltiplas frases
            results = chatbot.process_multiple_sentences(message, session_id)
            
            # Log da interação múltipla
            logger.info(f"Múltiplas frases processadas: {len(results)} frases")
            
            # Pega a melhor resposta para exibição principal
            best_result = max(results, key=lambda x: x['confidence']) if results else None
            
            # Cria lista de intenções detectadas
            detected_intents = list(set([r['intent'] for r in results if r['intent'] != 'fallback']))
            
            return jsonify({
                'response': best_result['response'] if best_result else '🤔 Não consegui processar nenhuma frase.',
                'intent': ', '.join(detected_intents) if detected_intents else (best_result['intent'] if best_result else 'error'),
                'confidence': best_result['confidence'] if best_result else 0.0,
                'multiple_results': results,
                'is_multiple': True,
                'sentence_count': len(sentences),
                'detected_intents': detected_intents
            })
        
        else:
            # Processa frase única
            response, intent, confidence = chatbot.get_response(message, session_id)
            
            # Log da interação
            logger.info(f"Query: '{message}' -> Intent: {intent}, Confidence: {confidence:.3f}")
            
            return jsonify({
                'response': response,
                'intent': intent,
                'confidence': round(float(confidence), 2),
                'multiple_results': [{
                    'sentence': message,
                    'response': response,
                    'intent': intent,
                    'confidence': round(confidence, 2),
                    'index': 1
                }],
                'is_multiple': False,
                'sentence_count': 1,
                'detected_intents': [intent] if intent != 'fallback' else []
            })
        
    except Exception as e:
        logger.error(f"Erro no endpoint /chat: {e}")
        return jsonify({
            'response': '🤔 Ocorreu um erro inesperado. Tente novamente.',
            'intent': 'error',
            'confidence': 0.0,
            'multiple_results': []
        }), 500

@app.route('/health')
def health():
    """Endpoint de saúde da aplicação"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'chatbot_ready': chatbot is not None,
        'intents_loaded': len(chatbot.intents) if chatbot else 0
    })

@app.errorhandler(404)
def not_found(error):
    """Handler para erro 404"""
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handler para erro 500"""
    logger.error(f"Erro interno: {error}")
    return jsonify({
        'error': 'Erro interno do servidor'
    }), 500

if __name__ == '__main__':
    # Configurações para desenvolvimento
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000
    )