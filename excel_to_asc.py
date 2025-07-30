#!/usr/bin/env python3
import pandas as pd
from datetime import datetime
import sys

def format_date(date, format='%d/%m/%y'):
    """Formatta una data nel formato richiesto"""
    if pd.isna(date):
        return ''
    return date.strftime(format)

def format_avere_line(row_num, data_cont, importo, codice1, codice2, data_rif, codice3, codice4):
    """Formatta una riga per il file Avere.ASC"""
    # Formato: data,C,importo,codice1,data_rif,codice2,codice3
    importo_int = abs(int(round(importo * 100)))  # Moltiplica per 100, arrotonda e prendi valore assoluto
    
    # Match the exact template format - N_Cli is field 3, importo is field 6
    line = f"{format_date(data_cont)},C,{codice1:>9},{codice4:>6},{format_date(data_rif)},{importo_int:>5},{codice3:>9}"
    
    return line

def format_dare_line(row_num, data_cont, n_cli, nome, cognome, indirizzo, cap, citta_res, 
                     provincia, importo, citta_nascita, nazione, sigla_nazione, 
                     data_nascita, cod_fisc):
    """Formatta una riga per il file Dare.ASC"""
    # Combina nome e cognome
    nome_completo = f"{cognome} {nome}".strip()
    
    # Formatta i campi con le lunghezze corrette
    nome_field = f"{nome_completo:<35}"
    indirizzo_field = f"{indirizzo:<35}" if indirizzo else " " * 35
    
    # Città con CAP - formato esatto del template con provincia
    cap_int = int(cap) if pd.notna(cap) and cap != 0 else 0
    prov_res = provincia if pd.notna(provincia) else ""
    citta_cap_field = f"{cap_int:05d} {citta_res:<25}{prov_res:>2}"
    
    # Formatta importo (moltiplicato per 100)
    importo_int = int(round(importo * 100))
    importo_field = f"{importo_int:>9}"
    
    # Parse città nascita e provincia se presenti nel formato "CITTÀ,PROV"
    if citta_nascita and ',' in citta_nascita:
        citta_n, prov_n = citta_nascita.split(',', 1)
        citta_nascita_field = f"{citta_n:<26}"
        prov_nascita = f"{prov_n.strip():>2}"
    else:
        citta_nascita_field = f"{citta_nascita:<26}" if citta_nascita else " " * 26
        prov_nascita = "  "
    
    # Nazione e sigla - IMPORTANT: sigla must be exactly 5 chars
    nazione_field = f"{nazione:<23}" if nazione else " " * 23
    sigla_naz_field = f"{sigla_nazione:<5}" if sigla_nazione else "     "
    
    # Data nascita nel formato DD/MM/YYYY
    if pd.notna(data_nascita):
        data_nasc_str = data_nascita.strftime('%d/%m/%Y')
    else:
        data_nasc_str = "          "
    
    # Codice fiscale - check if there's a leading space in the data
    if cod_fisc and cod_fisc.startswith(' '):
        cod_fisc_field = cod_fisc  # Keep the space
    else:
        cod_fisc_field = cod_fisc if cod_fisc else ""
    
    n_cli_int = int(n_cli) if pd.notna(n_cli) else 0
    line = f"{format_date(data_cont)},{n_cli_int:>5},{nome_field},{indirizzo_field},{citta_cap_field},{importo_field},{citta_nascita_field},{prov_nascita},{nazione_field},{sigla_naz_field},{data_nasc_str},{cod_fisc_field}"
    
    return line

def main():
    # Leggi il file Excel
    try:
        df = pd.read_excel('Test_Dario copia.xlsx')
        print(f"Letto file Excel con {len(df)} righe")
    except Exception as e:
        print(f"Errore nella lettura del file Excel: {e}")
        sys.exit(1)
    
    # Separa i record in base all'importo
    dare_records = df[df['Importo'] >= 0].copy()  # Changed from > to >=
    avere_records = df[df['Importo'] < 0].copy()
    
    print(f"Record per Dare.ASC (importo >= 0): {len(dare_records)}")
    print(f"Record per Avere.ASC (importo < 0): {len(avere_records)}")
    
    # Genera Avere.ASC
    with open('Avere.ASC', 'w', encoding='utf-8') as f:
        row_num = 1
        lines = []
        for idx, row in avere_records.iterrows():
            # Match template format exactly
            line = format_avere_line(
                row_num=row_num,
                data_cont=row['Data_contabilizzazione'],
                importo=row['Importo'],
                codice1=row['N_Cli'],  # This goes in field 3
                codice2=0,  # Not used in current mapping
                data_rif=row['Data_contabilizzazione'],
                codice3=1,  # Fixed value of 1 for field 7
                codice4=1   # Fixed value of 1 for field 4
            )
            lines.append(line)
            row_num += 1
        
        # Write all lines, no trailing newline on last line
        f.write('\n'.join(lines))
    
    print(f"Creato Avere.ASC con {row_num-1} record")
    
    # Genera Dare.ASC
    with open('Dare.ASC', 'w', encoding='utf-8') as f:
        row_num = 1
        lines = []
        for idx, row in dare_records.iterrows():
            line = format_dare_line(
                row_num=row_num,
                data_cont=row['Data_contabilizzazione'],
                n_cli=row['N_Cli'],
                nome=row['Nome'] if pd.notna(row['Nome']) else '',
                cognome=row['Cognome'] if pd.notna(row['Cognome']) else '',
                indirizzo=row['Indirizzo'] if pd.notna(row['Indirizzo']) else '',
                cap=row['CAP'] if pd.notna(row['CAP']) else 0,
                citta_res=row['Citta_residenza'] if pd.notna(row['Citta_residenza']) else '',
                provincia=row['Provincia'],
                importo=row['Importo'],
                citta_nascita=row['Citta_nascita'] if pd.notna(row['Citta_nascita']) else '',
                nazione=row['Nazione_nascita'] if pd.notna(row['Nazione_nascita']) else '',
                sigla_nazione=row['Sigla_nazione'] if pd.notna(row['Sigla_nazione']) else '',
                data_nascita=row['Data_nascita'],
                cod_fisc=row['Cod_fisc'] if pd.notna(row['Cod_fisc']) else ''
            )
            lines.append(line)
            row_num += 1
        
        # Write all lines, no trailing newline on last line
        f.write('\n'.join(lines))
    
    print(f"Creato Dare.ASC con {row_num-1} record")
    print("\nConversione completata!")

if __name__ == "__main__":
    main()