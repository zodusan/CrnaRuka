#!/bin/bash

# Provera root privilegija
if [ "$EUID" -ne 0 ]; then 
  echo "[-] Greška: Molim te, pokreni kao sudo: sudo ./install.sh"
  exit 1
fi

echo "[*] Ažuriranje sistema i instalacija alata..."
apt update -y
apt install -y aircrack-ng hashcat hcxtools python3 unzip curl wget gunzip

# 1. RUKOVANJE SRPSKIM REČNIKOM
if [ -f "srpski.zip" ]; then
    echo "[*] Pronađena arhiva srpski.zip. Otpakujem..."
    if unzip -o srpski.zip; then
        echo "[+] Rečnik srpski.txt je spreman. Brišem srpski.zip..."
        rm srpski.zip
    else
        echo "[!] GREŠKA: Neuspelo otpakivanje srpski.zip."
    fi
else
    if [ -f "srpski.txt" ]; then
        echo "[+] srpski.txt je već spreman."
    else
        echo "[!] UPOZORENJE: Ni srpski.zip ni srpski.txt nisu pronađeni."
    fi
fi

# 2. RUKOVANJE ROCKYOU REČNIKOM
ROCKYOU_DIR="/usr/share/wordlists"
ROCKYOU_PATH="$ROCKYOU_DIR/rockyou.txt"
ROCKYOU_GZ="$ROCKYOU_DIR/rockyou.txt.gz"

echo "[*] Provera rockyou.txt rečnika..."

if [ -f "$ROCKYOU_PATH" ]; then
    echo "[+] rockyou.txt je već spreman."
elif [ -f "$ROCKYOU_GZ" ]; then
    echo "[*] rockyou.txt.gz pronađen. Raspakujem..."
    gunzip -k "$ROCKYOU_GZ"
    echo "[+] rockyou.txt je raspakovan."
else
    echo "[*] rockyou.txt nije pronađen. Pokušavam preuzimanje..."
    mkdir -p "$ROCKYOU_DIR"
    
    # Preuzimanje sa proverom uspešnosti
    # Koristimo wget jer je često pouzdaniji za direktne linkove
    wget -O "$ROCKYOU_PATH" https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt
    
    if [ $? -eq 0 ] && [ -f "$ROCKYOU_PATH" ]; then
        echo "[+] rockyou.txt uspešno preuzet i sačuvan u $ROCKYOU_PATH."
    else
        echo "[!] GREŠKA: Preuzimanje rockyou.txt nije uspelo! Proveri internet konekciju."
    fi
fi

# 3. PODEŠAVANJE DOZVOLA
echo "[*] Podešavanje dozvola za skripte..."
chmod +x rukovanje.py
chmod +x lokalno.py

echo "=========================================="
echo "[+] INSTALACIJA ZAVRŠENA!"
echo "=========================================="
