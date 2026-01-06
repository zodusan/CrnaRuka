#!/bin/bash

# Provera da li je korisnik root
if [ "$EUID" -ne 0 ]; then 
  echo "Molim te, pokreni kao sudo: sudo ./install.sh"
  exit
fi

echo "[*] Ažuriranje sistema..."
apt update -y

echo "[*] Instalacija neophodnih alata (aircrack-ng, hashcat, hcxtools)..."
apt install -y aircrack-ng hashcat hcxtools python3

# Provera da li hcxpcapngtool postoji, ako ne, ispisuje upozorenje
if ! command -v hcxpcapngtool &> /dev/null; then
    echo "[!] Upozorenje: hcxpcapngtool nije pronađen. Pokušavam instalaciju iz izvora..."
    apt install -y hcxtools
fi

echo "[*] Podešavanje dozvola za skripte..."
chmod +x rukovanje.py
chmod +x lokalno.py

echo "[+] Instalacija završena!"
echo "Sada možeš pokrenuti hvatanje sa: sudo python3 rukovanje.py"
