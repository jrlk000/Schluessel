from machine import Pin, I2C, PWM
import json
import time

# I2C initialisieren (ESP32 Beispiel)
i2c = I2C(0, scl=Pin(7), sda=Pin(6), freq=400000)
#i2c scan liefert folgende Addresen, die von Verbindungen auf dem Board kommen müssen: [60, 81, 107] in hex ['0x3c', '0x51', '0x6b']



INA219_ADDR = 0x40 #Hauptaddrese
REG_SHUNT = 0x01 # Register Adresse
REG_BUS = 0x02 # Register Adresse
R_SHUNT = 0.1  # Widerstand in Ohm (meist 0.1 Ohm auf dem Modul)
BUZZER = PWM(Pin(5, Pin.OUT, Pin.PULL_DOWN, value=0))
BUZZER.freq(200)
BUZZER.duty_u16(500)


def read_ina219():
    # 1. Busspannung lesen (Register 0x02)
    bus_data = i2c.readfrom_mem(INA219_ADDR, REG_BUS, 2) #nbytes 2, jedes register liefert 2 bytes
    raw_bus = (bus_data[0] << 8) | bus_data[1]
    # Bit 3-15 nutzen, LSB = 4mV
    voltage = (raw_bus >> 3) * 0.004

    # 2. Shunt-Spannung lesen (Register 0x01)
    shunt_data = i2c.readfrom_mem(INA219_ADDR, REG_SHUNT, 2)
    raw_shunt = (shunt_data[0] << 8) | shunt_data[1]
    
    # Vorzeichenbehafteten 16-Bit-Wert auflösen
    if raw_shunt & 0x8000:
        raw_shunt -= 0x10000
        
    shunt_voltage = raw_shunt * 0.00001  # LSB = 10uV
    current = shunt_voltage / R_SHUNT    # I = U / R

    return voltage, current

# Hauptschleife für die Messwert-Ausgabe

try:
    while True:
        try:
            v, i = read_ina219()

            # Daten-Paket für den PC-Logger zusammenstellen
            payload = {
                "voltage": round(v, 3),
                "current": round(i, 4)
            }

            # JSON an den PC senden (über Print/Serial)
            print(json.dumps(payload))

        except Exception as e:
            # Falls I2C kurz stottert
            pass

        time.sleep(0.5)
except KeyboardInterrupt:
    # Sauberes Aufräumen beim Beenden
    print("Programm beendet. Räume auf...")
    BUZZER.deinit()

"""
Informationen für I2C Kommunikation:

Pin Belegung:
D4 SDA GPIO6
D5 SCL GPIO7

I2C(0, scl, sda, freq=4000)

suche nach I2C-Geräten
i2c.scan() -> Container mit Addressen (in hex() Verwandeln)

daten auslesen

addrese
i2c.readfrom(addres, 2)


Daten des INA219: 
0x01: (Register-Adresse) Spannung über den Messwiderstand
0x02: (Register-Adresse) Versorgungsspannung
"""
"""
# ---- Konstanten ----
SDA_PIN = Pin(6, Pin.OUT, value=0) # Ist hier ein Widerstand benötigt?
SCL_PIN = Pin(6, Pin.OUT, value=0)
I2C_FREQ = int(4e3)

#I2C erstellung
i2c = I2C(0, scl=SCL_PIN, sda=SDA_PIN, freq=I2C_FREQ)

#suche nach I2C fähigen Komponenten
i2c_addressen = i2c.scan()
print(f"I2C fähige Komponnetenadressen: {i2c_addressen}.")

for a in i2c_addressen: 
    print("Hex der obigen Addressen {hex(a)}")


#auslesen der daten des i2c Objektes
i2c.readfrom(addres, int)"""