import csv
import json
import os
from datetime import datetime
import time
import serial

# --- Konfiguration ---
SERIAL_PORT = '/dev/ttyACM0'
BAUDRATE = 115200
CSV_FILE = 'messdaten_entladung.csv'

# Prüfen, ob die Datei bereits existiert
file_exists = os.path.exists(CSV_FILE)

print(f"Starte Data Logger... Speichere in '{CSV_FILE}'")

try:
    ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)
    print(f"Serielle Verbindung zu {SERIAL_PORT} hergestellt.")
except Exception as e:
    print(f"Fehler beim Öffnen des seriellen Ports: {e}")
    exit(1)

# CSV-Datei im Append-Modus öffnen
with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # Header nur schreiben, falls die Datei neu erstellt wird
    if not file_exists:
        writer.writerow(['timestamp', 'voltage_v', 'current_a', 'power_w'])
        file.flush()

    try:
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8', errors='ignore').strip()

                if not line:
                    continue

                # Debug um zu gucken, was tatsächlich über das Kabel rein kommt.
                print(f"Empfangen: {line}")

                try:
                    data = json.loads(line)
                    u = float(data['voltage'])
                    i = float(data['current'])
                    p = round(u * i, 4)  # P = U * I
                    timestamp = datetime.now().isoformat()
                    print(u, i, p, timestamp)

                    # Datenzeile schreiben
                    writer.writerow([timestamp, u, i, p])

                    # WICHTIG: Puffer sofort auf Festplatte flushen (Schutz vor Datenverlust)
                    file.flush()

                    print(f"[{timestamp[:19]}] U: {u:.2f} V | I: {i:.2f} A | P: {p:.2f} W")

                except (json.JSONDecodeError, KeyError, ValueError) as e:
                    # Unvollständige oder fehlerhafte Zeilen überspringen
                    print("In exception ")
                    print(f'gelaufener Fehler: {e}')
                    pass

            time.sleep(1)

    except KeyboardInterrupt:
        print("\nLogger durch Benutzer gestoppt.")
    finally:
        ser.close()
        print("Serielle Verbindung geschlossen.")