# Systemy wizyjne - projekt
### Zadanie do realizacji
Realizacja projektu wiązała się ze zliczaniem konkretnych kształtów klocków oraz kolorów korzystając ze zdjęcia na wejściu.

### Wykorzystano
- OpenCV
- numpy

### Działanie
Przetwarzanie zdjęcia składa się kilku etapów. Pierwszym z nich jest wczytanie i wstępna obróbka
zdjęć z klockami bazowymi do których będą porównywane kształty. Po wykonaniu szeregu operacji
otrzymywany jest obraz binarny, który następnie jest dodawany do listy ze wszystkimi bazowymi
kształtami.

Kolejnym etapem jest obróbka zdjęcia aktualnie przetwarzanego w funkcji first(img), która jako
argument przyjmuje zdjęcie, już wcześniej zmniejszone. Pierwsze działania na obrazie mają celu pozbycie
się nadmiaru szczegółów za pomocą MeanShiftFiltering oraz w kolejnych etapach wykorzystany jest
algorytm Canny’ego do znalezienia krawędzi. Dalej wykorzystywane są możliwości funkcji cv.inRange()
dla poszczególnych kolorów, cv.erode() oraz cv.dilate(), po wykonaniu tych operacji na zdjęciu dodatkowo
wykrywane są kontury, aby pozbyć się niedoskonałości i drobnych szumów. Funkcja first(img) zwraca
obraz binarny oraz obraz w przestrzeni kolorów HSV z nałożoną maską tak aby widoczne były same
klocki. Pierwszy obraz zostanie dalej wykorzystany do porównywania kształtów, natomiast drugi do
wykrywania kolorów.

W funkcji perform_processing, po stworzeniu listy z konturami bazowymi oraz wstępnej obróbce
zdjęcia, wykonywana jest operacja wykrywania konturów i wyznaczana jest z nich średnia, aby dalej
pozbyć się najmniejszych konturów. Kolejnym etapem jest właściwe porównywanie kształtów. Większość
tych operacji wykonywana jest w pętli po wszystkich konturach ze zdjęcia, następnie znajdowany
jest minimalny boundingbox otaczający dany klocek, po czym wycinany jest ten klocek z obrazu
binarnego oraz obrazu HSV z maską. Dalej dla wyciętego kształtu wyznaczane są momenty(ostatecznie
wykorzystywane są tylko cztery pierwsze), które porównywane są w pętli po wszystkich kształtach
bazowych, z momentami poszczególnych klocków bazowych. Dla każdego kształtu dobrane są osobne
parametry, które zostały wyznaczone za pomocą metody prób i błędów. Oprócz momentów porównywany
jest stosunek szerokości do wysokości boundingbox. Kształt drugi oraz trzeci zaraz po wykryciu są
dodawane do listy wykrytych kształtów oraz w tym samym miejscu wyznaczany jest kolor dla danego
klocka. Pozostałe z kształtów poddawane są dodatkowej filtracji, ze względu na liczne podobieństwa, która
ma miejsce po wykonaniu się pętli po wszystkich kształtach ze zdjęcia. W tym miejscu porównywana jest
wartość maksymalna i/lub średnia konturów zapisanych wcześniej w liście. Jeśli dany kształt zostanie
zakwalifikowany wyznaczany jest dla niego kolor i w liście wynikowej w odpowiednim miejscu zwiększana
jest wartość znalezionego kształtu.

Wyznaczanie kolorów dla danego klocka odbywa się w funkcji get_colors(hsv), która przyjmuje wycięty
klocek z obrazu HSV z maską. Na początku czyszczona jest lista before, w której zapisywane są znalezione
kolory na wyciętym klocku. Dzieje się tak ponieważ w kolejnych etapach nakładana jest maska, na wycięty
klockek, dla każdego koloru z osobna i w dodatkowej funkcji sprawdzane jest czy średnia kolorów na
wycinku jest większa od zera. Jeśli tak to znaczy że wykryto dany kolor i wartość zostaje zapisana
do listy before. Następnie wykonuje się pętla po liście before z wykrytymi kolorami. Domyślnie jest ona
wypełniana liczbami 10, jeśli nie został znaleziony kolor. Natomiast jeśli pojawi się tylko jedna inna liczba
znaczy, że klocek ma tylko jeden kolor i zwracany jest indeks tego koloru w wektorze wynikowym. W
innym przypadku, gdy jest więcej niż jeden kolor oznacza to iż mamy do czynienia z mieszanym klockiem
i zwracana jest wartość indeksu koloru mieszanego w wektorze wynikowym, czyli 10.

Repozytorium należy uruchomić w sposób przedstawiony poniżej:
```
python3 main.py path/to/photos path/to/file/with/reults
```



