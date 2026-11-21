import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# --- Konfiguration ---
CSV_FILE = 'messdaten_entladung.csv'

# Resampling-Intervall für Langzeit-Messungen:
# '1s' = Sekunden (Rohdaten) | '1min' = 1-Minuten-Mittelwerte | '5min' = 5-Minuten-Mittelwerte
RESAMPLE_INTERVAL = '1min'

# --- Daten einlesen ---
print(f"Lade Messdaten aus '{CSV_FILE}'...")
try:
    df = pd.read_csv(CSV_FILE)
except FileNotFoundError:
    print(f"Fehler: Datei '{CSV_FILE}' nicht gefunden. Starte zuerst 'logger.py'!")
    exit(1)

if df.empty:
    print("Die CSV-Datei enthält noch keine Daten.")
    exit(1)

# Zeitstempel parsen und als Index setzen
df['timestamp'] = pd.to_datetime(df['timestamp'])
df.set_index('timestamp', inplace=True)

# --- Downsampling für flüssige Grafik ---
if RESAMPLE_INTERVAL:
    print(f"Aggregiere Daten auf Intervall: {RESAMPLE_INTERVAL}...")
    df_plot = df.resample(RESAMPLE_INTERVAL).mean().dropna()
else:
    df_plot = df

# --- Kenngrößen berechnen ---
dauer_stunden = (df.index[-1] - df.index[0]).total_seconds() / 3600.0
entladung_wh = - df['current_a'].mean() * dauer_stunden

print("=" * 40)
print(f"Messbeginn:       {df.index[0].strftime('%d.%m.%Y %H:%M:%S')}")
print(f"Messende:         {df.index[-1].strftime('%d.%m.%Y %H:%M:%S')}")
print(f"Gesamtdauer:      {dauer_stunden:.2f} Stunden")
print(f"Entladund: {entladung_wh:.2f} Ah")
print("=" * 40)

# --- Plot erstellen ---
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 8), sharex=True)
fig.suptitle('Entladeverlauf & Langzeitmessung', fontsize=14, fontweight='bold')

# 1. Spannung
ax1.plot(df_plot.index, df_plot['voltage_v'], color='#1f77b4', linewidth=1.5)
ax1.set_ylabel('Spannung [V]', color='#1f77b4', fontweight='bold')
ax1.grid(True, linestyle='--', alpha=0.6)

# 2. Strom
ax2.plot(df_plot.index, df_plot['current_a'], color='#d62728', linewidth=1.5)
ax2.set_ylabel('Strom [A]', color='#d62728', fontweight='bold')
ax2.grid(True, linestyle='--', alpha=0.6)

# 3. Leistung
ax3.plot(df_plot.index, df_plot['power_w'], color='#2ca02c', linewidth=1.5)
ax3.set_ylabel('Leistung [W]', color='#2ca02c', fontweight='bold')
ax3.set_xlabel('Datum / Uhrzeit', fontweight='bold')
ax3.grid(True, linestyle='--', alpha=0.6)

# Datum auf der X-Achse lesbar formatieren
ax3.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m %H:%M'))
fig.autofmt_xdate()

plt.tight_layout()
plt.show()