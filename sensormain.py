from flask import Flask, jsonify, request
import requests
import json

app = Flask(__name__)

# CONFIGURAÇÕES
IP_DO_SERVER = '52.237.23.203'  # Ip do server
# LUMINOSIDADE_MAX = 77
# TEMPERATURA_MAX = 36
# TEMPERATURA_MIN = -3
# UMIDADE_MAX = 83
# UMIDADE_MIN = 8

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
# Funções para mandar os dados em uma lista
@app.route('/sensor/luminosidade', methods=['GET'])
def get_luminosidade():
    lastN = request.args.get('lastN', 10, type=int)  # Padrão para 10
    luminosity = obter_dados(lastN, "luminosity", IP_DO_SERVER)
    lum = [float(entry['attrValue']) for entry in luminosity]
    return lum

@app.route('/sensor/temperatura', methods=['GET'])
def get_temperatura():
    lastN = request.args.get('lastN', 10, type=int)  # Padrão para 10
    temperature = obter_dados(lastN, "temperature", IP_DO_SERVER)
    temp = [float(entry['attrValue']) for entry in temperature]
    return temp

@app.route('/sensor/umidade', methods=['GET'])
def get_umidade():
    lastN = request.args.get('lastN', 10, type=int)  # Padrão para 10
    humidity = obter_dados(lastN, "humidity", IP_DO_SERVER)
    hum = [float(entry['attrValue']) for entry in humidity]
    return hum

@app.route('/sensor/tempo', methods=['GET'])
def get_tempo():
    lastN = request.args.get('lastN', 10, type=int)  # Padrão para 10
    humidity = obter_dados(lastN, "humidity", IP_DO_SERVER)
    tempos = [entry['recvTime'][11:19] for entry in humidity]
    return tempos


# @app.route('/sensor/status', methods=['GET'])
# def get_status():
#     status = {"LUMINOSIDADE_MAX": LUMINOSIDADE_MAX, 
#               "TEMPERATURA_MAX": TEMPERATURA_MAX, 
#               "TEMPERATURA_MIN": TEMPERATURA_MIN, 
#               "UMIDADE_MAX": UMIDADE_MAX, 
#               "UMIDADE_MIN": UMIDADE_MIN}
#     return jsonify(status)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # A API estará disponível na porta 5000
