# 📈 Napi Gazdasági Elemző Rendszer

Ez a rendszer egy automatizált, Bloomberg-szinthez közelítő minőségű, magyar nyelvű napi gazdasági elemzéseket készítő alkalmazás. A rendszer globális piaci híreket dolgoz fel angol nyelvű források alapján, majd ezeket a GPT-4.1 segítségével strukturált, elemző stílusú, Markdown formátumú jelentésekké alakítja, melyeket az MkDocs eszközzel publikál weben.

---

## 🚀 A projekt célja

- Automatikus napi piaci jelentések generálása
- Magas elemzői minőség, szakmai stílus
- Költséghatékony működtetés
- Strukturált, jól olvasható Markdown dokumentumok
- Automatizált publikáció weboldalon (MkDocs)

---

## 🛠️ Technológiai stack

A rendszer a következő technológiákra épül:

- **Python 3.12** *(programozási nyelv)*
- **OpenAI GPT-4.1 API** *(szöveg generálása)*
- **Google Custom Search API & Brave Search API** *(friss hírek keresése)*
- **MkDocs + Material Theme** *(webes dokumentáció és statikus site generálása)*
- **Cron job (ütemezett automatizálás)**

---

## 📁 Projekt könyvtárstruktúrája
piaci_elemzo_rendszer/
├── config/               # Konfigurációs YAML fájlok
│   ├── settings.yaml
│   └── credentials.yaml  # Érzékeny adatok (nem publikus)
├── data/                 # Adatok és logfájlok
├── docs/                 # MkDocs weboldal tartalmak
│   ├── index.md          # Kezdőlap
│   ├── daily/            # Napi jelentések
│   └── weekly/           # (opcionális) heti jelentések
├── prompts/              # Prompt sablonok GPT számára
│   ├── outline_prompt.txt
│   └── analysis_prompt.txt
├── scripts/              # Python szkriptek
│   ├── config_loader.py
│   ├── api_clients.py
│   ├── query_builder.py
│   ├── run_searches.py
│   └── generate_report.py
├── mkdocs.yml            # MkDocs konfiguráció
├── .gitignore            # Git ignorált fájlok
└── README.md             # Jelen dokumentáció

---

## ⚙️ Telepítés és konfiguráció

**1. Klónozd a repót és lépj be a könyvtárba:**
```bash
git clone git@github.com:felhasznaloneved/piaci_elemzo_rendszer.git
cd piaci_elemzo_rendszer
python3.12 -m venv venv
```
**2. Python környezet beállítása:**
```bash
source venv/bin/activate
```
**3. Függőségek telepítése:**
```bash
pip install openai google-api-python-client requests pyyaml mkdocs mkdocs-material
```
**4. Konfigurációs fájlok kitöltése (config/credentials.yaml):**
```bash
openai_api_key: "TE_API_KULCSOD"
google_search_api_key: "TE_API_KULCSOD"
google_cse_id: "TE_CUSTOM_SEARCH_ID"
brave_search_api_key: "TE_API_KULCSOD"
alpha_vantage_api_key: "TE_API_KULCSOD"
```
**5. Első futtatás tesztelése:**
```bash
python scripts/generate_report.py
```

## 🌐 Weboldal generálása MkDocs segítségével

**Helyi tesztelés:**
```bash
mkdocs serve
```
Ezután nyisd meg böngésződben:
http://127.0.0.1:8000

## 📅 Automatizált napi futtatás (cron job)

A rendszer minden hétköznap délután 18:00 órakor automatikusan generálja a jelentést.
**Cron példa (Linux/MacOS):**
```bash
0 18 * * 1-5 /teljes/utvonal/venv/bin/python /teljes/utvonal/scripts/generate_report.py >> /teljes/utvonal/data/report_generation.log 2>&1
```

## 📌 Fejlesztési folyamat (Git)

A fejlesztés a következő fő lépésekben zajlott, tiszta commit-loggal dokumentálva:
	•	Könyvtárstruktúra és alapfájlok létrehozása
	•	YAML-alapú konfiguráció
	•	OpenAI GPT-4.1 integrációja
	•	Google és Brave kereső API integráció
	•	Tematikus keresések automatizálása
	•	Dinamikus lekérdezésgenerálás kialakítása
	•	Kétlépcsős promptolás (vázlat + elemzés)
	•	Markdown jelentésgenerálás és MkDocs integráció
	•	Cron automatizálás napi szinten

## 📈 Jövőbeli fejlesztési ötletek

	•	Heti és havi összefoglaló jelentések generálása
	•	Grafikonok és további vizualizáció integrációja
	•	GitHub Actions alapú automatikus deployment (CI/CD pipeline)

## 🧑‍💻 Kapcsolat és támogatás

Ha kérdésed vagy javaslatod van, fordulj hozzám bizalommal:
	•	Fejlesztő: (helyettesítsd saját neveddel)
	•	E-mail: (helyettesítsd saját email címeddel)
	•	GitHub: https://github.com/felhasznaloneved

## 📜 Licenc és felhasználási feltételek

Ez a projekt non-profit célra készült. Kérjük, vedd figyelembe az egyes használt API-k felhasználási feltételeit is.

```bash
MIT License
Copyright (c) 2025
```

🎉 Köszönjük, hogy használod és támogatod a projektet! 🎉