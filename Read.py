

import MFRC522
import signal

continue_reading = True

# UID autorizado
AUTHORIZED_TAG = "BA4D9316"

# Função para converter o UID em uma string (corrigida para ordem correta)
def uidToString(uid):
    mystring = ""
    for i in uid:
        mystring += format(i, '02X')  # Concatena na ordem correta
    return mystring

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal, frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print("Welcome to the MFRC522 data read example")
print("Press Ctrl-C to stop.")

# This loop keeps checking for chips.
# If one is near it will get the UID and authenticate
while continue_reading:

    # Scan for cards
    (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print("Card detected")

        # Get the UID of the card
        (status, uid) = MIFAREReader.MFRC522_SelectTagSN()
        # If we have the UID, continue
        if status == MIFAREReader.MI_OK:
            uid_str = uidToString(uid)
            print("Card read UID: %s" % uid_str)

            # Verifica se a tag é autorizada
            if uid_str == AUTHORIZED_TAG:
                print("Tag autorizada!")
            else:
                print("Tag não autorizada!")
        else:
            print("Authentication error")
            print("Authentication error")