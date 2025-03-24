import serial

# Configurações da porta serial
porta_serial = '/dev/ttyACM0'  # Substitua pela porta correta
baud_rate = 9600  # Taxa de transmissão (baud rate) do leitor

# Abre a porta serial
try:
    leitor = serial.Serial(porta_serial, baud_rate, timeout=1)
    print(f"Conectado ao leitor de código de barras na porta {porta_serial}.")
except Exception as e:
    print(f"Erro ao abrir a porta serial: {e}")
    exit(1)

try:
    print("Aguardando leitura de código de barras...")
    while True:
        # Lê os dados da porta serial
        codigo = leitor.readline().decode('utf-8').strip()
        if codigo:
            print(f"Código de barras lido: {codigo}")
except KeyboardInterrupt:
    print("Leitura interrompida pelo usuário.")
finally:
    # Fecha a porta serial
    leitor.close()
    print("Porta serial fechada.")
