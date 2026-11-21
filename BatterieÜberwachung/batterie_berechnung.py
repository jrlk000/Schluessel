import math
import numpy as np

def entladezeit_tage(
    Q_0_Ah,
    I_ruhe_A=0.00005,
    I_druck_A=0.030,
    anzahl_druecker_pro_tag=10,
    zeit_druck_s=3,
    effektiver_anteil=0.85,
    selbstentladung_prozent_monat=3.0
    ):
    """Berechnet die Akkulaufzeit eines Tasters/Schlüssels in Tagen.

            Parameters:
            - Q_0_Ah: Nennkapazität des Akkus in Ah (z.B. 0.5 für 500 mAh)
            - I_ruhe_A: Ruhestrom inkl. LDO/Sensoren in Ampere (z.B. 0.00005 A = 50 µA)
            - I_druck_A: Strom beim Tastendruck in Ampere (z.B. 0.030 A = 30 mA)
            - anzahl_druecker_pro_tag: Wie oft wird die Taste pro Tag gedrückt?
            - zeit_druck_s: Dauer eines Tastendrucks in Sekunden
            - effektiver_anteil: Nutzbare Kapazität (0.85 = 85%)

            Returns:
            - Laufzeit in Tagen (float)
    """
    # 1. Nutzbare Kapazität in Ah
    q_nutzbar = Q_0_Ah * effektiver_anteil  # [Ah]

    # 2. Ruheverbrauch pro Tag in Ah (24 Stunden)
    q_ruhe_tag = I_ruhe_A * 24  # [Ah/Tag]

    # 3. Aktivverbrauch pro Tag in Ah (Sekunden / 3600 = Stunden)
    q_aktiv_tag = (
            anzahl_druecker_pro_tag * I_druck_A * (zeit_druck_s / 3600)
    )  # [Ah/Tag]

    # 4. Selbstentladung pro Tag in Ah
    # (Monatsverlust / 30 Tage = täglicher Verlust basierend auf Nennkapazität)
    q_selbst_tag = Q_0_Ah * ((selbstentladung_prozent_monat / 100) / 30)  # [Ah/Tag]

    # 4. Gesamter Tagesverbrauch in Ah
    q_gesamt_tag = q_ruhe_tag + q_aktiv_tag + q_selbst_tag  # [Ah/Tag]

    # Laufzeit = Nutzbare Kapazität / Tagesverbrauch
    tage = q_nutzbar / q_gesamt_tag
    return tage

print(entladezeit_tage(
            0.5,
            I_ruhe_A=44*1e-6,
            I_druck_A=0.1,
            anzahl_druecker_pro_tag=75,
            zeit_druck_s=3,
            effektiver_anteil=0.85,
    ))

print(entladezeit_tage(
            0.5,
            I_ruhe_A=1e-4,
            I_druck_A=0.1,
            anzahl_druecker_pro_tag=75,
            zeit_druck_s=3,
            effektiver_anteil=0.85,
    ))

print(entladezeit_tage(
            0.5,
            I_ruhe_A=15*1e-3,
            I_druck_A=0.1,
            anzahl_druecker_pro_tag=75,
            zeit_druck_s=3,
            effektiver_anteil=0.85,
    ))