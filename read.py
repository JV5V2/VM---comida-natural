#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import serial
import threading
import time

# Configuração do modo GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Definição dos pinos
RELAY_PIN = 12  # Pino conectado ao relé

# Configuração do pino do relé como saída
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.output(RELAY_PIN, GPIO.LOW)  # Inicialmente desligado

# Inicialização do leitor RFID
reader = SimpleMFRC522()

# Configuração do leitor de código de barras (modo USB COM)
# Ajuste a porta serial conforme necessário (geralmente /dev/ttyUSB0 ou /dev/ttyACM0)
BARCODE_PORT = '/dev/ttyACM0'  # Ajuste para a porta correta do seu dispositivo
BARCODE_BAUDRATE = 9600  # Ajuste conforme a configuração do seu leitor

# Lista de tags RFID autorizadas (IDs)
authorized_rfid_tags = [
   495499357456   # Tag genérica de exemplo - substitua pelo ID real da sua tag
]

# Lista de códigos de barras autorizados
authorized_barcodes = [
    "15635308"   # exemplo de código de barras
]

# Variável para controlar o estado do relé
relay_active = False
relay_lock = threading.Lock()

def activate_relay():
    """Ativa o relé por 5 segundos em uma thread separada"""
    global relay_active

    with relay_lock:
        # Se o relé já estiver ativo, não faz nada
        if relay_active:
            return
        relay_active = True

    # Ativa o relé
    GPIO.output(RELAY_PIN, GPIO.HIGH)
    print("Relé ATIVADO por 5 segundos...")

    # Aguarda 5 segundos
    time.sleep(5)

    # Desativa o relé
    GPIO.output(RELAY_PIN, GPIO.LOW)
    print("Relé DESATIVADO. Aguardando próxima leitura...")

    with relay_lock:
        relay_active = False

def barcode_reader_thread():
    """Thread para leitura contínua do leitor de código de barras"""
    try:
        # Tenta abrir a porta serial para o leitor de código de barras
        barcode_serial = serial.Serial(
            port=BARCODE_PORT,
            baudrate=BARCODE_BAUDRATE,
            timeout=1
        )
        print(f"Leitor de código de barras conectado em {BARCODE_PORT}")

        # Loop de leitura contínua
        while True:
            if barcode_serial.in_waiting > 0:
                # Lê o código de barras da porta serial
                barcode_data = barcode_serial.readline().decode('utf-8').strip()

                if barcode_data:
                    print(f"\nCódigo de barras lido: {barcode_data}")
                    # Verifica se o código de barras está autorizado
                    if barcode_data in authorized_barcodes:
                        print("Código de barras IDENTIFICADO! Ativando relé...")
                        # Inicia uma nova thread para ativar o relé
                        threading.Thread(target=activate_relay).start()
                    else:
                        print("Código de barras NÃO IDENTIFICADO! Tente novamente.")

            # Pequena pausa para evitar uso excessivo de CPU
            time.sleep(0.1)

    except serial.SerialException as e:
        print(f"Erro ao conectar ao leitor de código de barras: {e}")
        print("Verifique se o dispositivo está conectado e se a porta está correta.")
        print("O sistema continuará funcionando apenas com o leitor RFID.")

def rfid_reader_thread():
    """Thread para leitura contínua do leitor RFID"""
    print("Leitor RFID iniciado")

    while True:
        try:
            # Leitura da tag RFID
            id, text = reader.read()
            print(f"\nID da tag RFID lida: {id}")

            # Verificação se a tag está autorizada
            if id in authorized_rfid_tags:
                print("Tag RFID AUTORIZADA! Ativando relé...")
                # Inicia uma nova thread para ativar o relé
                threading.Thread(target=activate_relay).start()
            else:
                print("Tag RFID NÃO AUTORIZADA! Acesso negado.")

            # Pequena pausa antes da próxima leitura
            time.sleep(1)

        except Exception as e:
            print(f"Erro na leitura RFID: {e}")
            time.sleep(1)

def main():
    print("Sistema de Controle de Acesso RFID e Código de Barras iniciado")

    try:
        # Inicia a thread do leitor de código de barras
        barcode_thread = threading.Thread(target=barcode_reader_thread)
        barcode_thread.daemon = True  # Thread será encerrada quando o programa principal terminar
        barcode_thread.start()

        # Inicia a thread do leitor RFID
        rfid_thread = threading.Thread(target=rfid_reader_thread)
        rfid_thread.daemon = True  # Thread será encerrada quando o programa principal terminar
        rfid_thread.start()

        # Mantém o programa principal em execução
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nPrograma interrompido pelo usuário")
    finally:
        # Limpeza dos recursos GPIO ao encerrar
        GPIO.cleanup()
        print("Recursos GPIO liberados. Programa encerrado.")

if __name__ == "__main__":
    main()
