#!/bin/bash

# Provera root privilegija
if [ "$EUID" -ne 0 ]; then 
  echo "Molim te, pokreni kao sudo: sudo ./install.sh"
  exit
fi

echo "[*] Ažuriranje sistema i instalacija alata (aircrack, hashcat, hcxtools, curl)..."
apt update -y
apt install -y aircrack-ng hashcat hcxtools python3 unzip curl wget

# 1. RUKOVANJE SRPSKIM REČNIKOM
if [ -f "srpski.zip" ]; then
    echo "[*] Pronađena arhiva srpski.zip. Otpakujem..."
    unzip -o srpski.zip
    echo "[+] Rečnik srpski.txt je spreman."
else
    echo "[!] Upozorenje: srpski.zip nije pronađen."
fi

# 2. RUKOVANJE ROCKYOU REČNIKOM
ROCKYOU_PATH="/usr/share/wordlists/rockyou.txt"
ROCKYOU_GZ="/usr/share/wordlists/rockyou.txt.gz"

echo "[*] Provjera rockyou.txt rečnika..."

if [ -f "$ROCKYOU_PATH" ]; then
    echo "[+] rockyou.txt je već spreman na lokaciji $ROCKYOU_PATH."
elif [ -f "$ROCKYOU_GZ" ]; then
    echo "[*] rockyou.txt.gz pronađen. Raspakujem..."
    gunzip -k "$ROCKYOU_GZ"
    echo "[+] rockyou.txt je raspakovan."
else
    echo "[*] rockyou.txt nije pronađen na sistemu. Preuzimam sa interneta..."
    # Kreiramo folder ako ne postoji
    mkdir -p /usr/share/wordlists/
    # Preuzimanje sa pouzdanog izvora
    curl -L -o "$ROCKYOU_PATH" https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt
    echo "[+] Preuzimanje završeno."
fi

# 3. PODEŠAVANJE DOZVOLA
echo "[*] Podešavanje dozvola za skripte..."
chmod +x rukovanje.py
chmod +x lokalno.py

echo "=========================================="
echo "[+] INSTALACIJA ZAVRŠENA USPJEŠNO!"
echo "[+] Lokalne skripte: rukovanje.py, lokalno.py"
echo "[+] Rečnici: srpski.txt, rockyou.txt"
echo "=========================================="
echo "Pokreni hvatanje sa: sudo python3 rukovanje.py"
