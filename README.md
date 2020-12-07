# Projekt 1 - edytor wielokątów

## Instrukcja obsługi

* **dodawanie wielokąta** - rysowanie przy pomocy myszki: każde kliknięcie LPM powoduje dodanie wierzchołka, a kliknięcie na pierwszy wierzchołek powoduje "zamknięcie" i zapisanie wielokąta. Tworzenie figury można anulować klikając RPM.
* **usuwanie wielokąta** - kliknięcie RPM po najechaniu kursorem na wielokąt (powierzchnia figury powinna podświetlić się na fioletowo) powoduje usunięcie wielokąta.
* **usuwanie wierzchołka** - kliknięcie RPM po najechaniu kursorem na wierzchołek (powinien podświetlić się na zielono) powoduje usunięcie wierzchołka i połączenie sąsiadujących z nim krawędzi wielokąta. Jeśli wielokąt jest trójkątem, operacja nie powiedzie się i użytkownik otrzyma stosowny komunikat.
* **przesuwanie wielokąta, krawędzi lub wierzchołka** - przyciśnięcie LPM po najechaniu kursorem na wielokąt lub jego element pozwala na jego przesuwanie. Należy w tym celu poruszać myszką nie przyciskając ciągle LPM.
* **edycja krawędzi** - kliknięcie RPM po najechaniu kursorem na krawędź (która powinna podświetlić się na żółto) powoduje pokazanie dialogu edycji krawędzi. Następnie użytkownik może wybrać jedną z opcji:
  * dodanie wierzchołka w połowie krawędzi,
  * ustawienie krawędzi jako pionowej,
  * ustawienie krawędzi jako poziomej,
  * nadanie krawędzi stałej długości i wybranie wartości,
  * usunięcie ograniczenia (relacji) aktualnie przypisanego do krawędzi.
 
## Predefiniowany wielokąt

Aby otworzyć w aplikacji przygotowany wielokąt, należy z menu _File_ wybrać opcję _Load_ i otworzyć plik _predefined01_ znajdujący się w katalogu z projektem.
Projekt powinien działać zarówno na Windowsie jak i na Linuxach, jednak predefiniowany wielokąt został zapisany binarnie na Windowsie i pradopodobnie nie otworzy się na Linuksie.

Aby otworzyć w aplikacji przygotowany wielokąt, należy z menu _File_ wybrać opcję _Load_ i otworzyć plik _predefined01_ znajdujący się w katalogu z projektem.

## Algorytmy relacji

Nałożenie na krawędź danego ograniczenia (czyli ustalenie pewnej relacji między jej wierzchołkami) składa się z dwóch etapów:

1. Sprawdzania czy wprowadzenie wymaganych ograniczeń jest możliwe
2. Przesuwanie wierzchołków

Szkic algorytmu dla 1. etapu wygląda następująco:

1. Spośród wierzchołków krawędzi, `v1` i `v2` wybierany jest arbitralnie `v1`.
2. `if v2.relations:`
   1. `r` := relacja dotycząca wierzchołka `v2`
   2. `if not r.can_allow_move(v1.x, v1.y):`
      1. `return False`
   3. `return True`

Metoda `can_allow_move` ma postać zależną od relacji.

Szkic algorytmu dla 2. etapu nakładania relacji wygląda następująco:

1. `r` := nakładana relacja
2. `r.correct(v1)`,

gdzie metoda `correct` składa się z poniższych instrukcji:

1. `v2` := wierzchołek będący w relacji `r` z `v1`
2. `(x, y)` := współrzędne wyliczone dla `v2` przez relację `r`
3. `v2.move(x, y)`
4. `r2` := druga relacja wierzchołka `v2` (lub `None`)
5. `if r2:`
   1. `r2.correct(v2)`

Dodatkowo każda relacja przed przystąpieniem do 2. kroku powyższej metody sprawdza, czy rozważane wierzchołki już nie spełniają żądanych ograniczeń - jeśli tak, funkcja kończy działanie, co zapobiega nieskończonym wywołaniom rekurencyjnym. Metoda `correct`, w przeciwieństwie do `can_allow_move`, jest wykorzystywana również do utrzymania relacji przy przesuwaniu wierzchołków i krawędzi przez użytkownika. 

Poniżej przedstawiono schematy działania operacji `can_allow_move` oraz `correct` dla poszczególnych relacji.

### Krawędź pionowa

Obie metody przyjmują za cel przesunięcie rozważanego wierzchołka tak, aby jego współrzędna `x` była równa współrzędnej `x` wierzchołka "zlecającego" operację, a współrzędna `y` pozostała niezmieniona.

Metoda `can_allow_move` zwraca na koniec wynik wywołania metody wierzchołka `can_move`, której przybliżone działanie ilustruje szkic algorytmu 1. kroku nakładania relacji. W celu uniknięcia nieskończonej rekurencji, jeśli wierzchołek "inicjujący" nakładanie relacji (patrz wyżej `v1`) będzie rozważany przez metodę `can_allow_move` jakiejś relacji, to cały łańcuch wywołań `can_allow_move` i `can_move` zwróci `False`.

### Krawędź pozioma

Operacje są analogiczne jak dla krawędzi pionowej, współrzędne punktów rozważane są odwrotnie.

### Stała długość krawędzi

W przypadku tej relacji zachowanie przy jej nakładaniu różni się od zachowania przy przesuwaniu elementów wielokąta przez użytkownika. W związku z tym, przy inicjowaniu relacji, metoda `correct` korzysta z wyników metody `can_allow_move` przechowywanych przez obiekt relacji. 

Metoda `can_allow_move` sprawdza, czy rozważany wierzchołek należy do innej krawędzi o stałej długości. Jeśli tak, jego punkt docelowy jest wyliczany jako punkt przecięcia okręgów wyznaczonych przez obie relacje, bliższy aktualnej pozycji rozważanego punktu. Jeśli okręgi nie mają punktów wspólnych, oznacza to że relacji nie da się zastosować w danym przypadku.

W przeciwnym wypadku, punktem decelowym jest najbliższy aktualnej pozycji rozważanego punktu punkt taki, że relacja jest spełniona.

Jeśli obiekt relacji posiada informację o punkcie docelowym wybranym przez metodę `can_allow_move`, funkcja `correct` przesuwa rozważany wierzchołek do tego punktu i kasuje informację (ustawia zmienną na `None`).  W przeciwnym wypadku, wierzchołek przesuwany jest o taki sam wektor, o jaki ostatnio został przesunięty wierzchołek będący z nim w relacji.

## Uwagi

Ikonki wykorzystane w programie zostały pobrane ze strony [Icons8](https://icons8.com/).