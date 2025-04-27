# Checkpoint 5 - Vinheria com Dashboard
Esse projeto foi necessário utilizar os circuitos do checkpoint 4 e mandar eles para um dashboard e disponibilizar através de uma API 5000
## Sobre
- Utilize dashboard.py para pegar os dados diretos e criar um gráfico no matplotlib
- Para utilizar a API, é necessário colocar o sensorflask.service como serviço no linux Ubuntu de uma VM, também inserir o sensormain.py em uma pasta chamada "python" na home.
- Dependendo do server, é necessário mudar o IP nos scripts.
## Funcionalidades
- Atualização de dados em tempo real utilizando gráfico charts do NPM.
- Disponibilização da API na porta 5000, utilizando Flask de Python e Serviços do Linux em uma VM do Azure.

## Dependências
- VM com Docker para troca de informações (Para o exemplo do vídeo, foi utilizado Linux Ubuntu dentro de um Cloud Service)
### Bibliotecas do ESP32
- PubSubClient
- DHT sensor library

### Bibliotecas do Python
- Flask
- CORS
- request
- matplotlib (caso queira o gráfico no python)

## Integrantes
- Erik Kaiyu Suguiyama
- Belton Lee Carr
- Guilherme Vital
- Lucas Guerreiro

## Esquema do Circuito
![image](https://github.com/user-attachments/assets/fbe3f641-f54b-4853-9ebf-3f1af6fc1872)


## Video
https://youtu.be/_UkzW-MzAJk
## Projeto
https://wokwi.com/projects/426306197962039297
## Créditos
https://github.com/fabiocabrini/fiware
