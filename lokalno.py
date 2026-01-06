import os
import subprocess
import sys

def pokreni_hashcat(fajl_22000):
    print("\n" + "="*35)
    print(f" ODABERI NAPAD ZA: {fajl_22000}")
    print("="*35)
    print("1) srpski.txt")
    print("2) rockyou.txt")
    print("3) 8 brojeva (0-9 brute-force)")
    print("4) Nazad na listu fajlova")
    print("5) Izlaz")
    
    izbor = input("\nIzaberi opciju (1-5): ")

    # --- PUTANJE DO WORDLISTI ---
    # Promeni ove putanje ako se tvoji fajlovi nalaze negde drugde
    putanja_srpski = "srpski.txt" 
    putanja_rockyou = "/usr/share/wordlists/rockyou.txt"

    if izbor == '1':
        if os.path.exists(putanja_srpski):
            print(f"[!] Pokrećem: srpski.txt...")
            subprocess.run(f"hashcat -m 22000 {fajl_22000} {putanja_srpski}", shell=True)
        else:
            print(f"[-] Greška: Fajl {putanja_srpski} nije pronađen!")
    
    elif izbor == '2':
        if os.path.exists(putanja_rockyou):
            print(f"[!] Pokrećem: rockyou.txt...")
            subprocess.run(f"hashcat -m 22000 {fajl_22000} {putanja_rockyou}", shell=True)
        else:
            print(f"[-] Greška: Fajl {putanja_rockyou} nije pronađen!")
            
    elif izbor == '3':
        print(f"[!] Pokrećem napad na 8 brojeva (maska ?d?d?d?d?d?d?d?d)...")
        subprocess.run(f"hashcat -m 22000 -a 3 {fajl_22000} ?d?d?d?d?d?d?d?d", shell=True)
        
    elif izbor == '4':
        return True # Vraća se u glavnu petlju da ponovo biraš fajl
        
    elif izbor == '5':
        sys.exit()
        
    return False

def main():
    while True:
        # Pronalazak svih .22000 fajlova u trenutnom folderu
        fajlovi = [f for f in os.listdir('.') if f.endswith('.22000')]

        if not fajlovi:
            print("[-] Nije pronađen nijedan .22000 fajl u ovom folderu.")
            break

        print("\n" + "="*35)
        print(" PRONAĐENI HANDSHAKE FAJLOVI:")
        print("="*35)
        for i, fajl in enumerate(fajlovi):
            print(f"{i}) {fajl}")
        
        print(f"{len(fajlovi)}) IZLAZ")

        try:
            izbor_fajla = int(input("\nOdaberi broj fajla za napad: "))
            
            if izbor_fajla == len(fajlovi):
                break
                
            odabrani_fajl = fajlovi[izbor_fajla]
            
            # Pokreni hashcat meni za taj fajl
            ponovo = pokreni_hashcat(odabrani_fajl)
            if not ponovo:
                break # Ako završi napad i ne traži "Nazad", izlazi

        except (ValueError, IndexError):
            print("[-] Neispravan unos. Pokušaj ponovo.")

if __name__ == "__main__":
    main()
