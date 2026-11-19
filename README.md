# TeachYourself

Lernt Instrumente spielen: Theorie-Grafiken + Live-Audioerkennung zur Spielkorrektur.
Start mit Gitarre, weitere Instrumente folgen.

## Setup

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Tuner-MVP starten

```powershell
python -m src.ui.main
```

## Tests

```powershell
python -m pytest tests/
```

## Struktur

- `src/audio/` - Mikrofon-Input und Pitch-Detection (Autokorrelation, reines NumPy)
- `src/content/` - Instrumenten-Daten (Stimmung, Lektionen)
- `src/ui/` - UI (aktuell: Tuner-Fenster als MVP)
- `data/` - lokaler Nutzerfortschritt (nicht versioniert)
