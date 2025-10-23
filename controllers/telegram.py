
import requests


# ===== CONFIGURAÇÃO =====
TELEGRAM_TOKEN = "8383002236:AAGqwNYWX2EIPrS7s6aCyiH_2s_e1ihQLkE"

# Seus dados
MEU_USER_ID = 7018372797   # Edivaldo
MEU_USER_NAME = "Edivaldo"

# Grupo do Rene
GROUP_CHAT_ID = -4824595325    # Grupo "Rene e SentinelaBot"
RENE_USER_ID = 8357123466
RENE_USER_NAME = "Rene"

def send_telegram_message(tipo, device_id, id_telegram):
    """Envia alerta para você diretamente e para o Rene no grupo"""

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    print(id_telegram)
    # Mensagem para você
    text_me = (
        f"🚨 *ALERTA DO SISTEMA SENTINELA* 🚨\n\n"
        f"📍 Casa: {device_id}\n"
        f"⚠ Tipo de alerta: {tipo}\n\n"
        f"🔔 Chamando [Responsável](tg://user?id={id_telegram})"
    )
    '''
    # Mensagem para o grupo chamando o Rene
    text_group = (
        f"🚨 *ALERTA DO SISTEMA SENTINELA* 🚨\n\n"
        f"📍 Dispositivo: {device_id}\n"
        f"⚠ Tipo de alerta: {tipo}\n\n"
        f"🔔 Chamando [{RENE_USER_NAME}](tg://user?id={RENE_USER_ID})"
    )

    '''

    resultado_me = {"error": "não enviado"}
    resultado_group = {"error": "não enviado"}

    try:
        # Envia para você
        resposta_me = requests.post(url, json={
            "chat_id": id_telegram,
            "text": text_me,
            "parse_mode": "Markdown"
        })
        resultado_me = resposta_me.json()
        print(resultado_me)
        '''
        # Envia para o grupo
        resposta_group = requests.post(url, json={
            "chat_id": GROUP_CHAT_ID,
            "text": text_group,
            "parse_mode": "Markdown"
        })
        resultado_group = resposta_group.json()

        '''

    except Exception as e:
        return {"error": str(e)}

    return {"me": resultado_me, "grupo": 'nada'}
