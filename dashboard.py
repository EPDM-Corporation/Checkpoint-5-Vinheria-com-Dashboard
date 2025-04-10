import requests
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import json

LED_CHECK = 1

# CONFIGURAÇÕES
IP_DO_SERVER = '4.205.195.87' # Ip do server

LUMINOSIDADE_MAX = 77
TEMPERATURA_MAX = 36
TEMPERATURA_MIN = -3
UMIDADE_MAX = 83
UMIDADE_MIN = 8

# CONFIGURAÇÃO DE LEITURA
lastN = 10  

# Inicializar figura fora da função para reutilizar
fig, ax = plt.subplots()

# Função para obter os dados da API
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

# Função de animação
def animate(i):
    ax.clear()
    luminosity = obter_dados(lastN, "luminosity", IP_DO_SERVER)
    temperature = obter_dados(lastN, "temperature", IP_DO_SERVER)
    humidity = obter_dados(lastN, "humidity", IP_DO_SERVER)

    if not (luminosity and temperature and humidity):
        print("Dados insuficientes para plotar.")
        return

    # Preparar os dados
    tempos = [entry['recvTime'][11:19] for entry in luminosity]  # Pegando só HH:MM:SS
    lum = [float(entry['attrValue']) for entry in luminosity]
    temp = [float(entry['attrValue']) for entry in temperature]
    hum = [float(entry['attrValue']) for entry in humidity]

    # Verificar limites
    verificar_limite(lum, "luminosidade")
    verificar_limite(temp, "temperatura")
    verificar_limite(hum, "umidade")

    # Plotar
    ax.plot(tempos, lum, 'r-o', label="Luminosidade")
    ax.plot(tempos, temp, 'g-s', label="Temperatura")
    ax.plot(tempos, hum, 'b-^', label="Umidade")

    # Linhas limites
    ax.axhline(LUMINOSIDADE_MAX, color='r', linestyle='--', label='Limite Luminosidade')
    ax.axhline(TEMPERATURA_MAX, color='g', linestyle='--', label='Temp Máx')
    ax.axhline(TEMPERATURA_MIN, color='g', linestyle='--', label='Temp Mín')
    ax.axhline(UMIDADE_MAX, color='b', linestyle='--', label='Umidade Máx')
    ax.axhline(UMIDADE_MIN, color='b', linestyle='--', label='Umidade Mín')

    ax.set_title("Sensor de Temperatura, Umidade e Luminosidade (Tempo real)")
    ax.set_xlabel("Tempo")
    ax.set_ylabel("Valores")
    ax.legend()
    ax.grid(True)
   
    plt.tight_layout()

# Executar animação
ani = FuncAnimation(fig, animate, interval=5000, cache_frame_data=False)  # Atualiza a cada 5 segundos
plt.xticks(rotation=45)
plt.show()
