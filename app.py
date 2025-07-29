#!/usr/bin/env python3
from flask import Flask, render_template, request, send_file, flash, redirect, url_for
import pandas as pd
from datetime import datetime
import os
import tempfile
import zipfile
from werkzeug.utils import secure_filename
from excel_to_asc import process_excel_to_asc

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_excel_to_asc(filepath):
    """Process Excel file and return ASC content"""
    df = pd.read_excel(filepath)
    
    # Separate records based on amount
    dare_records = df[df['Importo'] >= 0].copy()
    avere_records = df[df['Importo'] < 0].copy()
    
    # Import formatting functions from excel_to_asc
    from excel_to_asc import format_avere_line, format_dare_line
    
    results = {
        'total_records': len(df),
        'dare_count': len(dare_records),
        'avere_count': len(avere_records),
        'avere_content': '',
        'dare_content': ''
    }
    
    # Generate Avere.ASC
    avere_lines = []
    for idx, row in avere_records.iterrows():
        line = format_avere_line(
            row_num=idx+1,
            data_cont=row['Data_contabilizzazione'],
            importo=row['Importo'],
            codice1=row['N_Cli'],
            codice2=0,
            data_rif=row['Data_contabilizzazione'],
            codice3=1,
            codice4=1
        )
        avere_lines.append(line)
    results['avere_content'] = '\n'.join(avere_lines)
    
    # Generate Dare.ASC
    dare_lines = []
    for idx, row in dare_records.iterrows():
        line = format_dare_line(
            row_num=idx+1,
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
    results['dare_content'] = '\n'.join(dare_lines)
    
    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file selected')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        try:
            filename = secure_filename(file.filename)
            temp_path = os.path.join(tempfile.gettempdir(), filename)
            file.save(temp_path)
            
            results = process_excel_to_asc(temp_path)
            os.remove(temp_path)
            
            return render_template('results.html', results=results)
            
        except Exception as e:
            flash(f'Error processing file: {str(e)}')
            return redirect(url_for('index'))
    else:
        flash('Unsupported file type. Use .xlsx or .xls files')
        return redirect(url_for('index'))

@app.route('/download', methods=['POST'])
def download_results():
    try:
        avere_content = request.form.get('avere_content', '')
        dare_content = request.form.get('dare_content', '')
        
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
        flash(f'Error creating download: {str(e)}')
        return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=False, host='0.0.0.0', port=port) 