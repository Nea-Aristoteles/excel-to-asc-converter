#!/usr/bin/env python3
from flask import Flask, render_template, request, send_file, flash, redirect, url_for, jsonify
import pandas as pd
from datetime import datetime
import os
import tempfile
import zipfile
from werkzeug.utils import secure_filename
import sys

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def format_date(date, format='%d/%m/%y'):
    """Formatta una data nel formato richiesto"""
    if pd.isna(date):
        return ''
    return date.strftime(format)

def format_avere_line(row_num, data_cont, importo, codice1, codice2, data_rif, codice3, codice4):
    """Formatta una riga per il file Avere.ASC"""
    importo_int = abs(int(round(importo * 100)))
    line = f"{format_date(data_cont)},C,{codice1:>9},{codice4:>6},{format_date(data_rif)},{importo_int:>5},{codice3:>9}"
    return line

def format_dare_line(row_num, data_cont, n_cli, nome, cognome, indirizzo, cap, citta_res, 
                     provincia, importo, citta_nascita, nazione, sigla_nazione, 
                     data_nascita, cod_fisc):
    """Formatta una riga per il file Dare.ASC"""
    nome_completo = f"{cognome} {nome}".strip()
    nome_field = f"{nome_completo:<35}"
    indirizzo_field = f"{indirizzo:<35}" if indirizzo else " " * 35
    citta_cap_field = f"{cap:05d} {citta_res:<30}"
    importo_int = int(round(importo * 100))
    importo_field = f"{importo_int:>9}"
    
    if citta_nascita and ',' in citta_nascita:
        citta_n, prov_n = citta_nascita.split(',', 1)
        citta_nascita_field = f"{citta_n:<26}"
        prov_nascita = "  "
    else:
        citta_nascita_field = f"{citta_nascita:<26}" if citta_nascita else " " * 26
        prov_nascita = "  "
    
    nazione_field = f"{nazione:<23}" if nazione else " " * 23
    sigla_naz_field = f"{sigla_nazione:<5}" if sigla_nazione else "     "
    
    if pd.notna(data_nascita):
        data_nasc_str = data_nascita.strftime('%Y-%m-%d')
    else:
        data_nasc_str = "          "
    
    if cod_fisc and cod_fisc.startswith(' '):
        cod_fisc_field = cod_fisc
    else:
        cod_fisc_field = cod_fisc if cod_fisc else ""
    
    line = f"{format_date(data_cont)},{n_cli:>5},{nome_field},{indirizzo_field},{citta_cap_field},{importo_field},{citta_nascita_field},{prov_nascita},{nazione_field},{sigla_naz_field},{data_nasc_str},{cod_fisc_field}"
    return line

def process_excel_file(filepath):
    """Processa il file Excel e genera i file ASC"""
    try:
        df = pd.read_excel(filepath)
        
        # Separa i record in base all'importo
        dare_records = df[df['Importo'] >= 0].copy()
        avere_records = df[df['Importo'] < 0].copy()
        
        results = {
            'total_records': len(df),
            'dare_count': len(dare_records),
            'avere_count': len(avere_records),
            'avere_content': '',
            'dare_content': ''
        }
        
        # Genera Avere.ASC
        avere_lines = []
        row_num = 1
        for idx, row in avere_records.iterrows():
            line = format_avere_line(
                row_num=row_num,
                data_cont=row['Data_contabilizzazione'],
                importo=row['Importo'],
                codice1=row['N_Cli'],
                codice2=0,
                data_rif=row['Data_contabilizzazione'],
                codice3=1,
                codice4=1
            )
            avere_lines.append(line)
            row_num += 1
        
        results['avere_content'] = '\n'.join(avere_lines)
        
        # Genera Dare.ASC
        dare_lines = []
        row_num = 1
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
            dare_lines.append(line)
            row_num += 1
        
        results['dare_content'] = '\n'.join(dare_lines)
        
        return results
        
    except Exception as e:
        raise Exception(f"Errore nel processare il file Excel: {str(e)}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('Nessun file selezionato')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('Nessun file selezionato')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        try:
            # Salva il file temporaneamente
            filename = secure_filename(file.filename)
            temp_path = os.path.join(tempfile.gettempdir(), filename)
            file.save(temp_path)
            
            # Processa il file
            results = process_excel_file(temp_path)
            
            # Pulisci il file temporaneo
            os.remove(temp_path)
            
            return render_template('results.html', results=results)
            
        except Exception as e:
            flash(f'Errore nel processare il file: {str(e)}')
            return redirect(url_for('index'))
    else:
        flash('Tipo di file non supportato. Utilizzare file .xlsx o .xls')
        return redirect(url_for('index'))

@app.route('/download/<file_type>')
def download_file(file_type):
    if file_type not in ['avere', 'dare']:
        return "File non trovato", 404
    
    # Questi dati dovrebbero essere memorizzati in sessione o database
    # Per semplicità, li riprocessiamo (in produzione usare sessioni)
    flash('Per scaricare i file, riprocessa il file Excel')
    return redirect(url_for('index'))

@app.route('/download_results', methods=['POST'])
def download_results():
    try:
        avere_content = request.form.get('avere_content', '')
        dare_content = request.form.get('dare_content', '')
        
        # Crea un file ZIP con entrambi i file ASC
        temp_zip = tempfile.NamedTemporaryFile(delete=False, suffix='.zip')
        
        with zipfile.ZipFile(temp_zip.name, 'w') as zip_file:
            if avere_content:
                zip_file.writestr('Avere.ASC', avere_content)
            if dare_content:
                zip_file.writestr('Dare.ASC', dare_content)
        
        temp_zip.close()
        
        return send_file(
            temp_zip.name,
            as_attachment=True,
            download_name='ASC_Files.zip',
            mimetype='application/zip'
        )
        
    except Exception as e:
        flash(f'Errore nel creare il download: {str(e)}')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080) 