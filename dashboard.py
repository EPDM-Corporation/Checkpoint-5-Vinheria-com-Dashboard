import requests
import matplotlib.pyplot as plt
import json

LED_CHECK = 1

# CONFIGURAÇÕES
IP_DO_SERVER = '52.237.23.203' # Ip do server

LUMINOSIDADE_MAX = 77
TEMPERATURA_MAX = 36
TEMPERATURA_MIN = -3
UMIDADE_MAX = 83
UMIDADE_MIN = 8


# Função para obter os dados de luminosidade a partir da API
def obter_dados(lastN, sensorType, IP):
    url = f"http://{IP}:8666/STH/v1/contextEntities/type/Sensor/id/urn:ngsi-ld:Sensor:001/attributes/{sensorType}?lastN={lastN}"
    headers = {
        'fiware-service': 'smart',
        'fiware-servicepath': '/'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        try:
            return response.json()['contextResponses'][0]['contextElement']['attributes'][0]['values']
        except (KeyError, IndexError):
            return []
    else:
        print(f"Erro ao obter dados: {response.status_code}")
        return []

# Ligar/desligar LED
def ligar_desligar_led(command, IP):
    url = f"http://{IP}:1026/v2/entities/urn:ngsi-ld:Sensor:001/attrs"
    payload = json.dumps({
        command: {
            "type": "command",
            "value": ""
        }
    })
    headers = {
        'Content-Type': 'application/json',
        'fiware-service': 'smart',
        'fiware-servicepath': '/'
    }
    requests.patch(url, headers=headers, data=payload)

def alternar_led():
    global LED_CHECK
    LED_CHECK *= -1
    comando = "on" if LED_CHECK == -1 else "off"
    ligar_desligar_led(comando, IP_DO_SERVER)

def verificar_limite(var_lista, var_tipo):
    for n in var_lista:
        match var_tipo:
            case "luminosidade":
                if n >= LUMINOSIDADE_MAX:
                    alternar_led()
                else:
                    ligar_desligar_led('off', IP_DO_SERVER)
            case "temperatura":
                if n >= TEMPERATURA_MAX or n <= TEMPERATURA_MIN:
                    alternar_led()
                else:
                    ligar_desligar_led('off', IP_DO_SERVER)
            case "umidade":
                if n >= UMIDADE_MAX or n <= UMIDADE_MIN:
                    alternar_led()
                else:
                    ligar_desligar_led('off', IP_DO_SERVER)

# Função para criar e exibir o gráfico
def plotar_grafico():

    luminosity = obter_dados(lastN, "luminosity", IP_DO_SERVER)
    temperature = obter_dados(lastN, "temperature", IP_DO_SERVER)
    humidity = obter_dados(lastN, "humidity", IP_DO_SERVER)

    if not (luminosity and temperature and humidity):
        print("Dados insuficientes para plotar.")
        return
    
    tempos = [entry['recvTime'][11:19] for entry in luminosity]  # Pegando só HH:MM:SS
    lum = [float(entry['attrValue']) for entry in luminosity]
    temp = [float(entry['attrValue']) for entry in temperature]
    hum = [float(entry['attrValue']) for entry in humidity]

    # Verificar limites
    verificar_limite(lum, "luminosidade")
    verificar_limite(temp, "temperatura")
    verificar_limite(hum, "umidade")

    plt.figure(figsize=(12, 6))


    # Plotar
    plt.plot(tempos, lum, 'r-o', label="Luminosidade")
    plt.plot(tempos, temp, 'g-s', label="Temperatura")
    plt.plot(tempos, hum, 'b-^', label="Umidade")

    # Linhas limites
    plt.axhline(LUMINOSIDADE_MAX, color='r', linestyle='--', label='Limite Luminosidade')
    plt.axhline(TEMPERATURA_MAX, color='g', linestyle='--', label='Temp Máx')
    plt.axhline(TEMPERATURA_MIN, color='g', linestyle='--', label='Temp Mín')
    plt.axhline(UMIDADE_MAX, color='b', linestyle='--', label='Umidade Máx')
    plt.axhline(UMIDADE_MIN, color='b', linestyle='--', label='Umidade Mín')

    plt.title("Sensor de Temperatura, Umidade e Luminosidade (Tempo real)")
    plt.xlabel("Tempo")
    plt.ylabel("Valores")
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()
# # Solicitar ao usuário um valor "lastN" entre 1 e 100
# while True:
#     try:
#         lastN = int(input("Digite um valor para lastN (entre 1 e 100): "))
#         if 1 <= lastN <= 100:
#             break
#         else:
#             print("O valor deve estar entre 1 e 100. Tente novamente.")
#     except ValueError:
#         print("Por favor, digite um número válido.")

# Obter os dados e plotar o gráfico

# Variável fixa para serviço do linux Ubuntu
lastN = 10

plotar_grafico()
