def send_menu(msg, profile_name):
    name = get_formatted_name(profile_name)
    msg.body(f"Olá *{name}*, obrigado por escolher a Agricopel! Sou o assistente virtual e estou aqui para te ajudar \n-----\nSelecione a opção desejada: \n1•* - Comprar um produto \n*2* - Tirar dúvidas \n*3* - Nossos produtos \n*4* - Sobre a empresa\n-----\nDigite o NÚMERO da opção desejada")
    img_url = "https://raizen-lubrificantes-prd.s3.sa-east-1.amazonaws.com/raizen-lubrificantes/wp-content/uploads/2023/04/24140122/AGRICOPEL-1-scaled-1.jpg"
    msg.media(img_url)

def get_formatted_name(profile_name):
    return "Cliente" if not profile_name else profile_name.capitalize()