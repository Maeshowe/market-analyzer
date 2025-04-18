# Napi Gazdasági Elemző Rendszer

Ez a projekt egy automatizált, napi szintű gazdasági elemzést generáló rendszer. A rendszer angol nyelvű webes forrásokból dolgozva közel Bloomberg-szintű napi gazdasági összefoglalót generál magyar nyelven, amely MkDocs segítségével publikálható webes formátumban jelenik meg.

## Projektstruktúra
piaci_elemzo_rendszer/
├── config/           # YAML konfigurációs fájlok (API-kulcsok, témák)
├── data/             # Ideiglenes adatok, keresési eredmények
├── docs/             # MkDocs dokumentumok (generált markdown fájlok)
│   ├── daily/        # Napi jelentések
│   └── weekly/       # Heti jelentések (későbbi bővítéshez)
├── prompts/          # GPT prompt sablonok
└── scripts/          # Python script fájlok

## Következő lépések
- API-k integrációja (OpenAI GPT-4.1, Google Custom Search, Brave Search API)
- Tematikus webes keresések automatizálása
- Promptok kialakítása és kétlépcsős promptolási folyamat implementálása
- Markdown output generálása és MkDocs integráció