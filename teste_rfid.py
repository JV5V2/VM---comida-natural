import time
import Adafruit_PN532 as PN532

# Configuração do PN532
try:
    # Configuração do PN532 via I2C
    pn532 = PN532.PN532(i2c_bus=1)  # Use i2c_bus=0 se estiver usando o barramento 0
    pn532.begin()
    pn532.SAM_configuration()  # Configura o módulo PN532
    print("PN532 inicializado com sucesso!")
except Exception as e:
    print(f"Erro ao inicializar o PN532: {e}")
    exit(1)

print("Aproxime uma tag RFID/NFC do leitor...")

try:
    while True:
        # Aguardar uma tag RFID/NFC
        uid = pn532.read_passive_target(timeout=1)  # Timeout de 1 segundo

        if uid is not None:
            print(f"Tag detectada! UID: {[hex(i) for i in uid]}")
        else:
            print("Nenhuma tag detectada. Aproxime uma tag...")

        time.sleep(1)  # Aguarda 1 segundo antes de verificar novamente

except KeyboardInterrupt:
    print("Teste interrompido pelo usuário.")
