from flask import request
from twilio.twiml.messaging_response import MessagingResponse
from app.menu import send_menu
from app.user_state import get_user_state, set_user_state


#Atribuições do chatbot
def bot():
    incoming_msg = request.values.get('Body', '').strip()
    user_phone = request.values.get('From', '')
    profile_name = request.values.get('ProfileName', '')

    resp = MessagingResponse()
    msg = resp.message()
    user_state = get_user_state(user_phone)

    if user_state == 'encerrado':
        msg.body("Atendimento encerrado. Para reiniciar, envie qualquer mensagem.")
        set_user_state(user_phone, 'menu')
        send_menu(msg, profile_name)
        return str(resp)

    if not user_state:
        set_user_state(user_phone, 'menu')
        user_state = 'menu'

    if user_state == 'menu':
        handle_menu(incoming_msg, msg, user_phone, profile_name)
    elif user_state == 'produtos':
        handle_produtos_regiao(incoming_msg, msg, user_phone)
    elif user_state == 'escolher_regiao_TRR':
        handle_atendente_regiao_TRR(incoming_msg, msg, user_phone)
    elif user_state == 'ultimaTRR_SC':
        assistenteTRRFinal_SC(incoming_msg, msg, user_phone)
    elif user_state == 'ultimaTRR_PR':
        assistenteTRRFinal_PR(incoming_msg, msg, user_phone)
    elif user_state == 'escolher_regiao_BIOAR':
        handle_atendente_regiao_BIOAR(incoming_msg, msg, user_phone)
    elif user_state == 'duvida':
        handle_duvida(incoming_msg, msg, user_phone)
    elif user_state == 'chamaCooldown':
        stopMessage(incoming_msg, msg, user_phone)
    elif user_state == 'msgRapida':
        stopMessage(incoming_msg, msg, user_phone)
    return str(resp)


#Escolhas do menu inicial
def handle_menu(incoming_msg, msg, user_phone, profile_name):
    if incoming_msg == "1":
        set_user_state(user_phone, 'produtos')
        msg.body("Nossos produtos:\n-----\n*1* - Diesel\n*2* - Arla-32\n-----\nDigite o NÚMERO da opção desejada ou a palavra *menu* para voltar.")
    elif incoming_msg == "2":
        set_user_state(user_phone, 'duvida')
        msg.body("Qual dúvida você tem?\n*1* - Horário de atendimento ⏱️\n*2* - Ver nota fiscal, xml ou boleto 🧾\n*3* - Falar com um assistente 👤\n-----\nDigite o NÚMERO da opção desejada ou a palavra *menu* para voltar")
    elif incoming_msg == "3":
        set_user_state(user_phone, 'msgRapida')
        msg.body("Nossos produtos ⛽\nhttps://agricopel.com.br/ \n\nProdutos Vectis 🚗 \nhttps://drive.google.com/file/d/13hu9KdVhBkmipfnimv5nKur4HxyeNI5K/view?usp=drive_link \n-----\nPara voltar digite a palavra *menu*")
    elif incoming_msg == "4":
        set_user_state(user_phone, 'msgRapida')
        msg.body("Nascemos em 1977, com um posto de combustíveis em Jaraguá do Sul (SC). Hoje, somos a maior rede de postos de Santa Catarina, formada pelos Postos Mime, que você já conhece... Novos negócios chegaram, e começamos a atuar também em outros segmentos.\n\nAtualmente, os segmentos que formam nosso Grupo:\n• *Agricopel TRR (Transportador-Revendedor- Retalhista)*\n• *Bioar (Arla 32)*\n• *Lubrificantes/Vectis*\n• *Transportes*\n• *Postos Mime*\n• *Ponto Mime*\n• *Posto Náutico Farol*\n\nR. Manoel Francisco da Costa, 2010 - Vieira, Jaraguá do Sul – SC 89257-207\n-----\nPara voltar digite a palavra *menu*")
        img_url = "https://ocp.news/wp-content/uploads/2023/08/Agricopel.jpeg"
        msg.media(img_url)
    else:
        send_menu(msg, profile_name)


#Escolha dos estados de cada produto
def handle_produtos_regiao(incoming_msg, msg, user_phone):
    if incoming_msg.lower() == "1":
        set_user_state(user_phone, 'escolher_regiao_TRR')
        msg.body("Ótimo, agora escolha o estado mais perto de você:\n-----\n1 - Santa Catarina\n2 - Paraná\n-----\nDigite o NÚMERO da opção desejada ou a palavra *menu* para voltar")
    elif incoming_msg.lower() == "2":
        set_user_state(user_phone, 'escolher_regiao_BIOAR')
        msg.body("Ótimo, agora escolha o estado mais perto de você:\n-----\n1 - Santa Catarina\n2 - Rio Grande do Sul\n3 - Mato Grosso do Sul\n4 - Paraná\n5 - São Paulo(Região metropolitana)\n6 - São Paulo(Interior)\n7 - Goiás\n8 - Minas Gerais\n-----\nDigite o NÚMERO da opção desejada ou a palavra *menu* para voltar")
    elif incoming_msg.lower() == "menu":
        set_user_state(user_phone, 'menu')
        send_menu(msg, '')
    else:
        msg.body("Opção inválida! Digite um número correspondente ou *menu* para voltar")


#Escolha da região do TRR
def handle_atendente_regiao_TRR(incoming_msg, msg, user_phone):
    if incoming_msg == "1": #SANTA CATARINA
        set_user_state(user_phone, 'ultimaTRR_SC')
        msg.body("Ótimo, agora escolha a região que mais corresponde à sua:\n-----\n1 - Grande Floripa\n2 - Norte Catarinense\n3 - Oeste Catarinense\n4 - Região Serrana\n5 - Sul Catarinense\n6 - Vale do Itajaí\n-----\nDigite o NÚMERO da opção desejada ou a palavra *menu* para voltar")
    elif incoming_msg == "2": #PARANÁ
        set_user_state(user_phone, 'ultimaTRR_PR')
        msg.body("Ótimo, agora escolha a região que mais corresponde à sua:\n-----\n1 - Centro-Oeste\n2 - Oeste\n3 - Curitiba e Região Metropolitana\n4 - Noroeste\n5 - Centro-Norte\n6 - Norte\n7 - Oeste\n8 - Sudeste\n9 - Sudoeste\n-----\nDigite o NÚMERO da opção desejada ou a palavra *menu* para voltar")
    elif incoming_msg.lower() == "menu":
        set_user_state(user_phone, 'menu')
        send_menu(msg, '')
    else:
        msg.body("Opção inválida! Digite um número correspondente ou *menu* caso queira voltar.")


#Atendentes BIOAR
def handle_atendente_regiao_BIOAR(incoming_msg, msg, user_phone):
    #Santa Catarina - Daiane
    if incoming_msg == "1":
        set_user_state(user_phone, 'chamaCooldown')
        msg.body("Fale com um de nossos assistentes 👇\n\nhttps://wa.me/5547992187876?text")
    #Rio Grande do Sul - Rosa
    elif incoming_msg == "2":
        set_user_state(user_phone, 'chamaCooldown')
        msg.body("Fale com um de nossos assistentes 👇\n\nhttps://wa.me/5547992713157?text")
    #Mato Grosso do Sul - Rosa
    elif incoming_msg == "3":
        set_user_state(user_phone, 'chamaCooldown')
        msg.body("Fale com um de nossos assistentes 👇\n\nhttps://wa.me/5547992713157?text")
    #Paraná - Graziele Salvá
    elif incoming_msg == "4":
        set_user_state(user_phone, 'chamaCooldown')
        msg.body("Fale com um de nossos assistentes 👇\n\nhttps://wa.me/5543996731211?text")
    #São Paulo(região metropolitana) - Graziele Medeiros
    elif incoming_msg == "5":
        set_user_state(user_phone, 'chamaCooldown')
        msg.body("Fale com um de nossos assistentes 👇\n\nhttps://wa.me/5547991563173?text")
    #São Paulo(interior) - Andressa
    elif incoming_msg == "6":
        set_user_state(user_phone, 'chamaCooldown')
        msg.body("Fale com um de nossos assistentes 👇\n\nhttps://wa.me/5547991668017?text")
    #Goiás - Josué
    elif incoming_msg == "7":
        set_user_state(user_phone, 'chamaCooldown')
        msg.body("Fale com um de nossos assistentes 👇\n\nhttps://wa.me/5547991938581?text")
    #Minas Gerais - Josué   
    elif incoming_msg == "8":
        set_user_state(user_phone, 'chamaCooldown')
        msg.body("Fale com um de nossos assistentes 👇\n\nhttps://wa.me/5547991938581?text")
    elif incoming_msg.lower() == "menu":
        set_user_state(user_phone, 'menu')
        send_menu(msg, '')


#Escoha das duvidas
def handle_duvida(incoming_msg, msg, user_phone):
    if incoming_msg.lower() == "1":
        set_user_state(user_phone, 'msgRapida')
        msg.body("O horário de atendimento é de segunda a sexta-feira, das *07:30h* às *17:15h*\n-----\nPara voltar digite a palavra *menu*")
    elif incoming_msg.lower() == "2":
        set_user_state(user_phone, 'msgRapida')
        msg.body("TUTORIAL DE ACESSO\n-----\n1° Passo: acesse o site https://agricopel.portaldocliente.online/ \n\n2° Passo: insira seu email\n*(Caso seja seu primeiro acesso, será enviado para seu email um link para a continuação da criação de um cadastro)*\n\n3° Passo: entre com suas informações no site\n\n4° Passo: adicione a sua empresa por CPF ou CNPJ\n\n5° Passo: confira as informações que deseja no site e baixe os documentos caso necessário")
    elif incoming_msg.lower() == "3":
        set_user_state(user_phone, 'msgRapida')
        msg.body("Fale com um de nossos assistentes 👇\nhttps://wa.me/5547992235576?text") #Contato Patricia
    else:
        msg.body("Opção inválida! Digite um número correspondente ou *menu* caso queira voltar..")


#Escolha final do TRR SANTA CATARINA
def assistenteTRRFinal_SC(incoming_msg, msg, user_phone):
    #Grande Floripa - Ana B
    if incoming_msg == "1": 
        set_user_state(user_phone, 'chamaCooldown')
        msg.body("Fale com um de nossos assistentes 👇\n\nhttps://wa.me/5547988860453?text")
    #Norte Catarinense - Oélita
    elif incoming_msg == "2":
        set_user_state(user_phone, 'chamaCooldown')
        msg.body("Fale com um de nossos assistentes 👇\n\nhttps://wa.me/5547992581260?text")
    #Oeste Catarinense - Samara
    elif incoming_msg == "3":
        set_user_state(user_phone, 'chamaCooldown')
        msg.body("Fale com um de nossos assistentes 👇\n\nhttps://wa.me/5547992809282?text")
    #Região Serrana - Ana B
    elif incoming_msg == "4":
        set_user_state(user_phone, 'chamaCooldown')
        msg.body("Fale com um de nossos assistentes 👇\n\nhttps://wa.me/5547988860453?text")
    #Sul Catarinense - Ana B
    elif incoming_msg == "5":
        set_user_state(user_phone, 'chamaCooldown')
        msg.body("Fale com um de nossos assistentes 👇\n\nhttps://wa.me/5547988860453?text")
    #Vale do Itajaí - Samara
    elif incoming_msg == "6":
        set_user_state(user_phone, 'chamaCooldown')
        msg.body("Fale com um de nossos assistentes 👇\n\nhttps://wa.me/5547992809282?text")
    elif incoming_msg.lower() == "menu":
        set_user_state(user_phone, 'menu')
        send_menu(msg, '')


#Escolha final do TRR PARANÁ
def assistenteTRRFinal_PR(incoming_msg, msg, user_phone):
    #Centro-Oeste - Jaqueline
    if incoming_msg == "1": 
        set_user_state(user_phone, 'chamaCooldown')
        msg.body("Fale com um de nossos assistentes 👇\n\nhttps://wa.me/5543999598460?text")
    #Leste - Pamela
    elif incoming_msg == "2":
        set_user_state(user_phone, 'chamaCooldown')
        msg.body("Fale com um de nossos assistentes 👇\n\nhttps://wa.me/5547988088386?text")
    #Curitiba e Região Metropolitana - Pamela
    elif incoming_msg == "3":
        set_user_state(user_phone, 'chamaCooldown')
        msg.body("Fale com um de nossos assistentes 👇\n\nhttps://wa.me/5547988088386?text")
    #Noroeste - Pamela
    elif incoming_msg == "4":
        set_user_state(user_phone, 'chamaCooldown')
        msg.body("Fale com um de nossos assistentes 👇\n\nhttps://wa.me/5547988088386?text")
    #Centro-Norte - Pamela
    elif incoming_msg == "5":
        set_user_state(user_phone, 'chamaCooldown')
        msg.body("Fale com um de nossos assistentes 👇\n\nhttps://wa.me/5547988088386?text")
    #Norte - Jaqueline
    elif incoming_msg == "6":
        set_user_state(user_phone, 'chamaCooldown')
        msg.body("Fale com um de nossos assistentes 👇\n\nhttps://wa.me/5543999598460?text")
    #Oeste - Jaqueline
    elif incoming_msg == "7":
        set_user_state(user_phone, 'chamaCooldown')
        msg.body("Fale com um de nossos assistentes 👇\n\nhttps://wa.me/5543999598460?text")
    #Sudeste - Ana Fabri
    elif incoming_msg == "8":
        set_user_state(user_phone, 'chamaCooldown')
        msg.body("Fale com um de nossos assistentes 👇\n\nhttps://wa.me/5542998104101?text")
    #Sudoeste - Jaqueline
    elif incoming_msg == "9":
        set_user_state(user_phone, 'chamaCooldown')
        msg.body("Fale com um de nossos assistentes 👇\n\nhttps://wa.me/5543999598460?text")
    elif incoming_msg.lower() == "menu":
        set_user_state(user_phone, 'menu')
        send_menu(msg, '')


#Ponto de parada para certas mensagens
def stopMessage(incoming_msg, msg, user_phone):
    if incoming_msg.lower() == "menu":
            set_user_state(user_phone, 'menu')
            send_menu(msg, '')
    else:
        set_user_state(user_phone, 'encerrado')
        msg.body("Agradecemos pela preferência😊 Caso queira reiniciar o atendimento, basta enviar qualquer mensagem")