# Brak funkcjonalności przycisku "Wyczyść" (sortowanie) na podstronie `/filmy`


### **Setup**
- **OS:** Windows 11 24H2 (comp: 26 100.6899)  
- **Przeglądarka:** Brave 1.84.139 | MS Edge 142.0.3595.53  
- **Częstotliwość występowania:** 100%  
- **URL:** [https://vod-tv.pl/filmy](https://vod-tv.pl/filmy)

---

### **Kroki do odtworzenia**
1. Otworzyć stronę `https://vod-tv.pl/filmy`  
2. Wybrać dowolne sortowanie  
3. Kliknąć przycisk **„Wyczyść”**

---

### **Oczekiwany wynik**
Cofnięcie wybranego sposobu sortowania lub przywrócenie sortowania domyślnego (o ile jest jakieś domyślne).

---

### **Uzyskany wynik**
Brak jakiejkolwiek akcji po kliknięciu przycisku.

---

### **Kroki podjęte w celu diagnozy**
1. Otworzenie narzędzi deweloperskich  
2. Zaznaczenie przycisku **„Wyczyść”**  
3. Dodanie monitora eventów:
   ```js
   monitorEvents($0, 'click')
   ```
4. Kliknięcie przycisku „Wyczyść”
5. Obserwacje logu w konsoli  ()
    ```js
    click PointerEvent{()...)}
    ```
6. Sprawdzenie funkcji podpiętych pod zdarzenie kliknięcia:
```js
getEventListeners($0).click
```
7. Podejrzenie definicji obu zwróconych funkcji
- 1. Odwołuje się do pustej funkcji th (prawdopodobnie placeholder lub funkcja domyślna frameworka)
- 2. Odnosi się do funkcji logującej event (dodanej w kroku 3.)

---

**Zdiagnozowany problem**

Przycisk „Wyczyść” nie ma przypisanej żadnej funkcji obsługującej jego działanie.

---

**Dodatkowe obserwacje**

- Wybór sortowania powoduje pełne przeładowanie strony, dodając do adresu parametry (np. ?popularity=asc) — brak dynamicznej aktualizacji listy.

- Brak możliwości cofnięcia sortowania poprzez ponowne kliknięcie tego samego typu sortowania.

---

**Severity**
Minor (funkcja pomocnicza, nie wpływa istotnie działanie serwisu)

---

**Priorytet**
Medium (funkcjonalność niekrytyczna, ale jej brak może być irytujący dla użytkownika.)