# README

## Opis zadania

Twoim zadaniem jest stworzenie testu automatycznego w Python (Playwright lub Selenium), który sprawdzi działanie opisanego flow użytkownika. Gotowy projekt powinien być umieszczony w publicznym repozytorium na GitHubie.

## Struktura repozytorium (proponowana)

```text
takegroup-qa/
  |-- reports/
  |    | -- task_c_report.md        # opis błędu związanego z zadaniem C
  |-- tests/
  |    |-- e2e/
  |    |    |-- test_vod_ui.py
  |    |    |-- pages/              # POMs
  |    |-- api/
  |    |    |-- test_vod_api.py
  |-- requirements.txt              # biblioteki
  |-- README.md
  |-- .github/workflows/main.yml    # CI
  |-- Dockerfile                    # konteneryzacja
  |-- .dockerignore
  |-- .gitignore
```

### **Setup**
- **OS:** Windows 11 24H2 (comp: 26 100.6899)  
- **Przeglądarka:** Brave 1.84.139 | MS Edge 142.0.3595.53  
- **Częstotliwość występowania:** 100%  
- **URL:** [https://vod-tv.pl/filmy](https://vod-tv.pl/filmy)
- **python:** 3.13

## Instalacja zależności

```bash
python -m venv .venv
.venv/bin/activate     # Linux/macOS
.venv\Scripts\activate.bat  # Windows (cmd)
pip install -r requirements.txt # lub pip install .
```

## Parametryzacja testów

Każdy z plików zawierajacych testy posiada sekcje TEST PARAMS, w której znajdują się zmienne pozwalajace edytować parametry, dla jakich zostanie test wywołany.
Poza tytułem, w przypadku testów e2e drugi parametr mówi o tym, czy oczkujemy, że dla wskazanej szukanej frazy strona zwróci wynik, czy jego brak.


## Uruchomienie testów

Uruchomienie wszystkich testów przy użyciu pytest:
```bash
pytest -q
```
Uruchomienie tylko pojedynczego katalogu z testami:
```bash
pytest -q tests/e2e
pytest -q tests/api
```

## Wybrana narzędzie do automatyzacji

**Playwright** - ponieważ ze Selenium miałem już styczność i nie było to najprzyjemniejsze środowisko do testów. Wielokrotnie musiałem kombinować z rozwiązaniami nie wprost (np. wstrzykiwanie i uruchamianie funkcji JS na stronie www), wiec postanowiłem sprawdzić cos nowego.


## Endpoint
Poniżej żądanie http w formacie, jaki przyjmuje HTTP Client (dodatek do vs code) wraz z pełnym kompletem czytelelnych danych dla przykładowej frazy.

```
POST https://vod-tv.pl/search-route
Content-Type: application/json

{
  "host": "vod-tv.pl",
  "locale": "pl",
  "searchTerm": "The Pickup"
}
```

## Założenia i uproszczenia

## Napotkane problemy

- Widget video na stronie jest dość problematyczny w obsłudze i lubi się totalnie zablokować lub wpaść w nieskończony buffor (w tej lepszej sytuacji), co pozwala zakończyć test pozytywnie. Nie mam pojęcia o co chodzi, gdyż nawet zastopowanie testu i próba ręcznego wyklikania elementów nie przynosi skutku. Możliwe, engine

## Raporty błędów

Raport wskazanego błędu został umieszczony w katalogu `reports`. 
Nie przygotowałem raportu innego błędu.

## Analiza SQL (teoretyczna)

Zapytanie w postgresql które zwraca tytuł i kategorie dla konkretnego tytułu.

```sql
select v.title, c.name
from categories c 
join video_category vc on vc.category_id = c.id
join videos v on v.id = vc.video_id
where v.title='The Pickup';
```

## CI/CD 
`.github/workflows/main.yml` zawiera polecenia reagujące na push, w tym zakomentowany krok, który w razie błędów będzie kopiował folder logs.

## Docker
Pliki związane z dockerem to `Dockerfile` i `.dockerignore`.

### Budowa kontenera
`docker build -t docker-qa .`
### Uruchamianie kontenera
Linux:
`docker run --rm -v $(pwd):/app docker-qa pytest -q tests`
Windows:
`docker run --rm -v ${PWD}:/app docker-qa pytest -q tests`
