# CrnaRuka  // Wi-Fi Handshake Automator & Cracker (Kali Linux)

Ovaj projekat sadrži set Python skripti za automatizaciju procesa hvatanja WPA/WPA2 handshake-ova i njihovo probijanje (cracking) koristeći Hashcat. Dizajnirano za **Kali Linux** i optimizovano srpski recnikom.


## 🚀 Mogućnosti
* **Automatska detekcija kartice:** Prepoznaje dostupne Wi-Fi interfejse.
* **Smart Monitor Mode:** Automatski prebacuje karticu u monitor mod i gasi procese koji smetaju.
* **Auto-Deauth:** Pokreće deauthentication napad u pozadini dok `airodump` hvata handshake.
* **Konverzija u .22000:** Automatski pretvara `.cap` fajl u format spreman za Hashcat koristeći `hcxpcapngtool`.
* **Lokalni Cracker:** Posebna skripta za upravljanje sačuvanim handshake-ovima i pokretanje tri različita tipa napada (srpski.txt rockyou.txt i kombinacija 8 brojeva)

## 🛠️ Preduslovi
Pre korišćenja, instaliraj neophodne alate:
```bash
sudo apt update
sudo apt install python3 aircrack-ng hcxtools hashcat
```


📂 Opis skripti
1. rukovanje.py (Hvatanje uživo)

Glavna skripta za rad na terenu.

    Pokreni sa: sudo python3 rukovanje.py

    Izaberi mrežnu kartu. (ako ima samo jedna automatski bira nju)

    Pronađi metu (BSSID i kanal).

    Skripta radi deauth i čeka handshake.

    Po završetku, čisti sistem, restartuje mrežu i nudi Hashcat meni.

2. lokalno.py (Offline rad)

Skripta koja skenira tvoj folder u potrazi za .22000 fajlovima.

    Pokreni sa: python3 lokalno.py

    Izaberi koji fajl želiš da napadneš.

    Biraj između: srpski.txt, rockyou.txt ili 8-digit brute force.

⚠️ Napomena (Disclaimer)

Ovaj alat je napravljen isključivo u edukativne svrhe i za penetraciono testiranje sopstvenih mreža ili mreža za koje imate dozvolu. Svaka zloupotreba je ilegalna i autor ne snosi odgovornost.
