# 📊 Excel to ASC Converter

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Una moderna applicazione web per convertire file Excel in formato ASC per sistemi contabili. Supporta la separazione automatica dei record in file Avere e Dare con interfaccia web intuitiva.

![Screenshot](https://via.placeholder.com/800x400/667eea/ffffff?text=Excel+to+ASC+Converter)

## 🌟 Caratteristiche

- **🎨 Interface Web Moderna**: Design responsive con gradiente elegante
- **📤 Upload Sicuro**: Supporto per file .xlsx e .xls fino a 16MB
- **⚡ Conversione Automatica**: Separazione automatica in Avere.ASC e Dare.ASC
- **👀 Preview Risultati**: Anteprima dei file generati prima del download
- **📦 Download ZIP**: Scarica entrambi i file ASC in un archivio compresso
- **🔒 Sicurezza**: Validazione file, gestione errori completa, cleanup automatico
- **📱 Responsive**: Funziona perfettamente su desktop, tablet e mobile

## 🚀 Quick Start

### Prerequisiti
- Python 3.8 o superiore
- pip (package installer per Python)

### Installazione

1. **Clona il repository**
   ```bash
   git clone https://github.com/yourusername/excel-to-asc-converter.git
   cd excel-to-asc-converter
   ```

2. **Installa le dipendenze**
   ```bash
   pip3 install --user --break-system-packages -r requirements.txt
   ```

3. **Avvia l'applicazione**
   ```bash
   python3 run_server.py
   ```

4. **Apri il browser**
   
   Vai su: **http://localhost:8080**

## 🌐 Deploy to Production

### Quick Deploy to Render (Free)

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

1. Fork this repository
2. Create account on [Render.com](https://render.com)
3. Connect your GitHub repository
4. Deploy automatically!

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

## 📋 Come Utilizzare

1. **📁 Seleziona File**: Clicca su "Seleziona File Excel" e scegli il tuo file .xlsx o .xls
2. **🚀 Converti**: Clicca su "Converti in ASC" per elaborare il file
3. **👀 Anteprima**: Visualizza i risultati della conversione
4. **💾 Download**: Scarica i file ASC generati in formato ZIP

## 📁 Struttura File Excel Richiesta

Il file Excel deve contenere le seguenti colonne:

| Colonna | Descrizione | Esempio |
|---------|-------------|---------|
| `Data_contabilizzazione` | Data di contabilizzazione | 2025-01-01 |
| `N_Cli` | Numero cliente | 1 |
| `Nome` | Nome del cliente | MARIO |
| `Cognome` | Cognome del cliente | ROSSI |
| `Indirizzo` | Indirizzo del cliente | VIA ROMA 1 |
| `CAP` | Codice di avviamento postale | 00100 |
| `Citta_residenza` | Città di residenza | ROMA |
| `Provincia` | Provincia | RM |
| `Importo` | Importo (+ per Dare, - per Avere) | 100.50 |
| `Citta_nascita` | Città di nascita | ROMA,RM |
| `Nazione_nascita` | Nazione di nascita | ITALIA |
| `Sigla_nazione` | Sigla della nazione | I |
| `Data_nascita` | Data di nascita | 1980-01-01 |
| `Cod_fisc` | Codice fiscale | RSSMRA80A01H501X |

> 💡 **Suggerimento**: Usa il file `sample_data.xlsx` incluso nel repository come esempio di formato corretto.

## 📤 File di Output

### 📄 Avere.ASC
- Contiene record con **importo negativo** (crediti)
- Formato: `data,C,n_cli,1,data,importo,1`
- Esempio: `01/01/25,C,        5,     1,01/01/25, 7738,        1`

### 📄 Dare.ASC
- Contiene record con **importo ≥ 0** (debiti)
- Formato completo con tutti i dati anagrafici del cliente
- Include nome, indirizzo, città, importo, dati di nascita e codice fiscale

## 🏗️ Architettura del Progetto

```
excel-to-asc-converter/
├── 📁 templates/           # Template HTML
│   ├── index.html         # Pagina di upload
│   └── results.html       # Pagina risultati
├── 📄 app.py              # Applicazione Flask principale
├── 📄 run_server.py       # Script di avvio server
├── 📄 excel_to_asc.py     # Script originale (CLI)
├── 📄 requirements.txt    # Dipendenze Python
├── 📄 sample_data.xlsx    # File Excel di esempio
├── 📄 Avere_template.ASC  # Template formato Avere
├── 📄 Dare_template.ASC   # Template formato Dare
└── 📄 README.md          # Documentazione
```

## 🛠️ Sviluppo

### Eseguire in modalità sviluppo
```bash
export FLASK_ENV=development
python3 app.py
```

### Struttura del codice
- **Frontend**: Template HTML con CSS e JavaScript integrati
- **Backend**: Flask con logica di conversione integrata
- **Processing**: Utilizzo di Pandas per elaborazione Excel

### Contribuire
1. Fork del repository
2. Crea un branch per la tua feature (`git checkout -b feature/AmazingFeature`)
3. Commit delle modifiche (`git commit -m 'Add some AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Apri una Pull Request

## 🔧 Risoluzione Problemi

<details>
<summary><strong>❌ Errore "Module not found"</strong></summary>

```bash
pip3 install --user --break-system-packages pandas openpyxl flask werkzeug
```
</details>

<details>
<summary><strong>🔌 Porta già in uso</strong></summary>

Modifica la porta nel file `app.py` o `run_server.py`:
```python
app.run(debug=True, host='0.0.0.0', port=8080)  # Cambia porta
```
</details>

<details>
<summary><strong>📊 File Excel non riconosciuto</strong></summary>

- Assicurati che il file sia in formato .xlsx o .xls
- Verifica che contenga tutte le colonne richieste
- Controlla che non ci siano celle unite nell'header
- Usa il file `sample_data.xlsx` come riferimento
</details>

<details>
<summary><strong>🍎 macOS: Porta 5000 occupata da AirPlay</strong></summary>

L'app usa automaticamente la porta 8080. Se hai problemi:
- Disabilita AirPlay Receiver in Preferenze di Sistema → Generali → AirDrop e Handoff
- Oppure cambia porta nell'applicazione
</details>

## 📦 Dipendenze

| Pacchetto | Versione | Descrizione |
|-----------|----------|-------------|
| Flask | 3.0.0 | Framework web |
| Pandas | 2.2.0 | Elaborazione dati Excel |
| OpenPyXL | 3.1.2 | Lettura file Excel |
| Werkzeug | 3.0.1 | Utilità Flask |

## 🔒 Sicurezza

- ✅ Validazione tipo file
- ✅ Limite dimensione file (16MB)
- ✅ Sanificazione nome file
- ✅ File temporanei eliminati automaticamente
- ✅ Gestione errori completa
- ✅ Nessun dato persistente sul server

## 📄 Licenza

Questo progetto è distribuito sotto licenza MIT. Vedi il file `LICENSE` per dettagli.

## 🤝 Supporto

- 🐛 **Bug Reports**: Apri un issue su GitHub
- 💡 **Feature Requests**: Proponi nuove funzionalità via issue
- 📧 **Supporto**: Controlla la sezione "Issues" per problemi comuni

## 🏷️ Versioning

Usiamo [SemVer](http://semver.org/) per il versioning. Per le versioni disponibili, vedi i [tags su questo repository](https://github.com/yourusername/excel-to-asc-converter/tags).

---

<div align="center">

**Realizzato con ❤️ per semplificare la conversione di dati contabili**

[🌟 Star questo repo](https://github.com/yourusername/excel-to-asc-converter) se ti è stato utile!

</div> 