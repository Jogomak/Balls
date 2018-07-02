# -*- coding: utf-8 -*-
import random
import gi

# wymagamy biblioteki w wersji min 3.0
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from gi.repository import GdkPixbuf


class Kulki():
    """Klasa tworząca iterfejs i będąca silnikiem gry kulki.

    Gra polega na przesuwaniu kul na puste miejsca tak aby utworzyć rząd (poziomy, pionowy, na ukos) składający się
    z co najmniej 5 kul takiego samego koloru, które następnie zostaną usunięte. Punkty zdobywamy za każdy ruch.
    Po każdym ruchu w polowych miejscach pojawiają się trzy losowe kule.
    """
    def __init__(self, ):
        """Konstuktor klasy. Torzy elementy interfejsu graficznego i ustawia domyślne wartości elementów i pól klasy.

        Na początek tworzy pola:
        czyPierwszyWybrany - określa czy zostało już kliknięte pole na planszy, -1 oznacza że nie zostało jeszcze
            wybrane pierwsze pole, liczbą większa od -1 oznacza numer wybranego pola.,
        liczbaPustychPol - liczba pustych pól na planszy, na początku równe 100,
        listaRankingowa - lista pięciu najlepszych wyników.
        Następnie tworzy główno okno - Gtk.Window, potem kontenery składające się na interfejs graficzny - pola z
        prefixem 'box'. Kolejne to przycisk buttonGrajOdPoczątku (ustawiając od razu tekst znajdujący się na nim)
        znajdujący się u dołu okna gry i jego uchwyt do sygnału 'clicked' metody nowa_gra, postyObraz zawierający pusty
        Gtk.Image używany do usuwania kul z pól planszy, następnie dwie listy listaZawartosciPol i
        listaPrzyciskowPlanszy, następnie pierwsza wypełniona zostaje zerami, a druga Gtk.ToggleButton'ami z uchwytami
        do sygnału 'pressed' metody button_clicked. Następnie etykiety (pola z prefixem 'label') wyświetlające po lewej
        ranking, i na górze aktualne punkty. Następnie wszystkie elementy są dodawane do odpowiednich kontenerów,
        uchwyt głównego okna do sygnału 'delete-event' metody Gtk.main_quit (aby po kliknięciu x w prawym górnym rogu
        program zakończył się), ustawienie wielkości głównego okna, wyświetlnie wszystkich elementów i wylosowanie
        50 początkowych kul metoda losuj_kule.
        """
        self.czyPierwszyWybrany = -1
        self.liczbaPustychPol = 100
        self.listaRankingowa = []

        self.window = Gtk.Window()

        self.boxOkno = Gtk.VBox()
        self.boxLiczbaPunktow = Gtk.HBox()
        self.boxRankingPlansza = Gtk.HBox()
        self.boxRanking = Gtk.VBox()
        self.boxPlansza = Gtk.VBox()
        self.boxPlanszaRzad0 = Gtk.HBox()
        self.boxPlanszaRzad1 = Gtk.HBox()
        self.boxPlanszaRzad2 = Gtk.HBox()
        self.boxPlanszaRzad3 = Gtk.HBox()
        self.boxPlanszaRzad4 = Gtk.HBox()
        self.boxPlanszaRzad5 = Gtk.HBox()
        self.boxPlanszaRzad6 = Gtk.HBox()
        self.boxPlanszaRzad7 = Gtk.HBox()
        self.boxPlanszaRzad8 = Gtk.HBox()
        self.boxPlanszaRzad9 = Gtk.HBox()

        self.buttonGrajOdPoczatku = Gtk.Button.new_with_label('Graj od początku')
        self.buttonGrajOdPoczatku.connect('clicked', self.nowa_gra)

        self.pustyObraz = Gtk.Image()

        self.listaPrzyciskowPlanszy = []
        self.listaZawartosciPol = []
        for i in xrange(100):
            self.listaZawartosciPol += [0]
            self.listaPrzyciskowPlanszy += [Gtk.ToggleButton()]
            self.listaPrzyciskowPlanszy[i].set_size_request(50, 50)
            self.listaPrzyciskowPlanszy[i].connect('pressed', self.button_clicked, i)

        self.labelLiczbaPunktow = Gtk.Label('Liczba punktów: ')
        self.labelAktualnePunkty = Gtk.Label('0')
        self.labelRanking = Gtk.Label('Ranking:')
        self.labelRanking.set_size_request(100, 20)
        self.labelRanking.set_xalign(0)
        self.labelWynik1 = Gtk.Label()
        self.labelWynik1.set_xalign(0)
        self.labelWynik2 = Gtk.Label()
        self.labelWynik2.set_xalign(0)
        self.labelWynik3 = Gtk.Label()
        self.labelWynik3.set_xalign(0)
        self.labelWynik4 = Gtk.Label()
        self.labelWynik4.set_xalign(0)
        self.labelWynik5 = Gtk.Label()
        self.labelWynik5.set_xalign(0)

        self.window.add(self.boxOkno)
        self.boxOkno.pack_start(self.boxLiczbaPunktow, False, False, 0)
        self.boxOkno.pack_start(self.boxRankingPlansza, False, False, 0)
        self.boxOkno.pack_start(self.buttonGrajOdPoczatku, False, False, 0)
        self.boxLiczbaPunktow.pack_start(self.labelLiczbaPunktow, False, False, 0)
        self.boxLiczbaPunktow.pack_start(self.labelAktualnePunkty, False, False, 0)
        self.boxRankingPlansza.pack_start(self.boxRanking, False, False, 0)
        self.boxRankingPlansza.pack_start(self.boxPlansza, False, False, 0)
        self.boxRanking.pack_start(self.labelRanking, False, False, 0)
        self.boxRanking.pack_start(self.labelWynik1, False, False, 0)
        self.boxRanking.pack_start(self.labelWynik2, False, False, 0)
        self.boxRanking.pack_start(self.labelWynik3, False, False, 0)
        self.boxRanking.pack_start(self.labelWynik4, False, False, 0)
        self.boxRanking.pack_start(self.labelWynik5, False, False, 0)
        self.boxPlansza.pack_start(self.boxPlanszaRzad0, False, False, 0)
        self.boxPlansza.pack_start(self.boxPlanszaRzad1, False, False, 0)
        self.boxPlansza.pack_start(self.boxPlanszaRzad2, False, False, 0)
        self.boxPlansza.pack_start(self.boxPlanszaRzad3, False, False, 0)
        self.boxPlansza.pack_start(self.boxPlanszaRzad4, False, False, 0)
        self.boxPlansza.pack_start(self.boxPlanszaRzad5, False, False, 0)
        self.boxPlansza.pack_start(self.boxPlanszaRzad6, False, False, 0)
        self.boxPlansza.pack_start(self.boxPlanszaRzad7, False, False, 0)
        self.boxPlansza.pack_start(self.boxPlanszaRzad8, False, False, 0)
        self.boxPlansza.pack_start(self.boxPlanszaRzad9, False, False, 0)
        for i in xrange(10):
            self.boxPlanszaRzad0.pack_start(self.listaPrzyciskowPlanszy[i], False, False, 0)
            self.boxPlanszaRzad1.pack_start(self.listaPrzyciskowPlanszy[i + 10], False, False, 0)
            self.boxPlanszaRzad2.pack_start(self.listaPrzyciskowPlanszy[i + 20], False, False, 0)
            self.boxPlanszaRzad3.pack_start(self.listaPrzyciskowPlanszy[i + 30], False, False, 0)
            self.boxPlanszaRzad4.pack_start(self.listaPrzyciskowPlanszy[i + 40], False, False, 0)
            self.boxPlanszaRzad5.pack_start(self.listaPrzyciskowPlanszy[i + 50], False, False, 0)
            self.boxPlanszaRzad6.pack_start(self.listaPrzyciskowPlanszy[i + 60], False, False, 0)
            self.boxPlanszaRzad7.pack_start(self.listaPrzyciskowPlanszy[i + 70], False, False, 0)
            self.boxPlanszaRzad8.pack_start(self.listaPrzyciskowPlanszy[i + 80], False, False, 0)
            self.boxPlanszaRzad9.pack_start(self.listaPrzyciskowPlanszy[i + 90], False, False, 0)

        self.window.connect("delete-event", Gtk.main_quit)

        self.window.set_default_size(615, 455)
        self.window.show_all()

        self.losuj_kule(50)
        Gtk.main()

    def nowa_gra(self, button):
        """Metoda czyści plansze, resetuje pola na wartości początkowe, losuje i umieszcza 50 kul na planszy.

        Argument metody: button - przycisk który wysłał sygnał.
        """
        self.wyczysc_plansze()
        self.losuj_kule(50)

    def uaktualnij_ranking(self):
        """Metoda uaktualniająca po zakończeniu gry ranking znajdujący się po lewej stronie.

        Jeśli w aktualnym rankingu jest mniej niż 5 wyników to dodaje aktualny wynik do listy listaRankingowa, w przeciwnym
        przypadku zastępuje najniższy (ostatni wynik) jeśli jest on niższy niż aktualny. Następnie sortuje listę
        listaRankingowa i wspisuje jej wartości do wigetów kolejno od labelWynik1 do labelWynik5 (lub mniej jeśli nie ma tylu
        pozycji w liście)
        """
        if len(self.listaRankingowa) < 5:
            self.listaRankingowa += [self.labelAktualnePunkty.get_label()]
        elif self.listaRankingowa[4] < self.labelAktualnePunkty.get_label():
            self.listaRankingowa[4] = self.labelAktualnePunkty.get_label()
        else:
            return

        self.listaRankingowa.sort(reverse=True)

        #jeśli wyników jest mniej niż 5 to odniesienie się do olementu którego nie ma zwróci wyjątek który zignorujemy
        try:
            self.labelWynik1.set_label('1. ' + self.listaRankingowa[0])
            self.labelWynik2.set_label('2. ' + self.listaRankingowa[1])
            self.labelWynik3.set_label('3. ' + self.listaRankingowa[2])
            self.labelWynik4.set_label('4. ' + self.listaRankingowa[3])
            self.labelWynik5.set_label('5. ' + self.listaRankingowa[4])
        except:
            pass

    def wyczysc_plansze(self):
        """Metoda usuwająca wszystkie kule z planszy, resetująca aktualny wynik.

        Ustawia wszystkie pola na wolne, czyli zmienną liczbaPustychPol na 100. Wczytuje każdemu polu planszy
        (listaPrzyciskowPlanszy) pusty obraz. Ustawia zawartość pól na pustą, ustawiając wszystkie elementy
        listaZawartosciPol na 0. Ustawia aktualny wynik na 0.
        """
        self.liczbaPustychPol = 100
        for i in xrange(100):
            self.listaPrzyciskowPlanszy[i].set_image(self.pustyObraz)
            self.listaZawartosciPol[i] = 0

        self.labelAktualnePunkty.set_label('0')
        self.czyPierwszyWybrany = -1

    def losuj_kule(self, liczbaLosowanychKul):
        """Metoda losuje i wstawia kule na plansze w ilosci podanej jako argument.

        Na poczatku sprawdza czy ilosc wolnych pól planszy (liczbaPustychPol) jest większa od żądanej ilości kul do
        wylosowania (argument funkcji - liczbaLosowanychKul), jeśli jest mniejsza to losujemy tylko tyle kul ile jest
        wolnych mniejsc. Zmniejszamy ilośc wolnych pól o kule które za chwile wylosujemy. Zmienna i zlicza ilość
        wylosowanych już kul, dopóki jest mniejsza od liczbaLosowanychKul losujemy pozycje od 0 do 99, jeśli pole
        na wylosowanej pozycji jest puste, to losujemy kulę i ją tam wstawiamy i zwiększamy i, w p.p. losujemy kolejną
        pozycję.
        """
        if liczbaLosowanychKul > self.liczbaPustychPol:
            liczbaLosowanychKul = self.liczbaPustychPol
        self.liczbaPustychPol = self.liczbaPustychPol - liczbaLosowanychKul

        i = 0
        while i < liczbaLosowanychKul:
            pozycja = random.randint(0, 99)
            if self.listaZawartosciPol[pozycja] == 0:
                self.listaZawartosciPol[pozycja] = random.randint(1, 5)
                self.listaPrzyciskowPlanszy[pozycja].set_image(Gtk.Image.new_from_pixbuf(GdkPixbuf.Pixbuf.new_from_file_at_size(
                    'kulka' + str(self.listaZawartosciPol[pozycja]) + '.svg', 35, 35)))
                i += 1

    def button_clicked(self, button, pozycja):
        """Metoda obsługująca sygnał 'pressed'.

        Argumenty metody:
        -button - przycisk który wysłał sygnał,
        -pozycja - indeks na którym znajduję się button.
        Sprawdzamy czy zostało wybrane już 'pierwsze pole', jeśli nie:
        -sprawdzamy czy na polu z którego przyszedł sygnał stoi kula, jeśli tak to zostaje ono 'pierwszym polem' -
            przypisujemy jego pozycję do czyPierwszyWybrany, jeśli nie to odznaczamy przycisk i nic nie robimy,
        jeśli tak:
        -sprawdzamy czy pole z którego przyszedł sygnał jest puste, jeśli nie to odznaczamy przyciski i ustawiamy
            czyPierwszyWybrany na -1, a jeśli tak to: zamieniamy wartości w listaZawartosciPol, wstawiamy do
            pierwszego pola pusty obrazek, a do drugiego obraz odpowiedniej kulki. Następnie zwiększamy punktację o 1,
            wywołujemy metody usun_kule, losuj_kule, usun_kule.
        """
        if self.czyPierwszyWybrany < 0:
            if self.listaZawartosciPol[pozycja]:
                self.czyPierwszyWybrany = pozycja
            else:
                self.listaPrzyciskowPlanszy[pozycja].set_active(True)
        else:
            if not self.listaZawartosciPol[pozycja]:
                #zamiana wartości
                self.listaZawartosciPol[pozycja] = self.listaZawartosciPol[self.czyPierwszyWybrany]
                self.listaZawartosciPol[self.czyPierwszyWybrany] = 0
                #przypisanie nowych obrazów przycisków
                self.listaPrzyciskowPlanszy[pozycja].set_image(Gtk.Image.new_from_pixbuf(
                    GdkPixbuf.Pixbuf.new_from_file_at_size('kulka' + str(self.listaZawartosciPol[pozycja]) + '.svg', 35, 35)))
                self.listaPrzyciskowPlanszy[self.czyPierwszyWybrany].set_image(self.pustyObraz)
                #uwypuklenie przycisków
                self.listaPrzyciskowPlanszy[pozycja].set_active(True)
                self.listaPrzyciskowPlanszy[self.czyPierwszyWybrany].set_active(False)
                self.czyPierwszyWybrany = -1

                self.labelAktualnePunkty.set_label(str(int(self.labelAktualnePunkty.get_label()) + 1))
                self.usun_kule()
                self.losuj_kule(3)
                self.usun_kule()
                if not self.liczbaPustychPol:
                    self.uaktualnij_ranking()
            else:
                self.listaPrzyciskowPlanszy[self.czyPierwszyWybrany].set_active(False)
                self.listaPrzyciskowPlanszy[pozycja].set_active(True)
                self.czyPierwszyWybrany = -1

    def usun_kule(self):
        """Metoda usuwająca kule z planszy ktore znajdują się w jednokolorowym rzędzie składającym się z co najmniej 5 kul.

        Tworzymy zbiór kuleDoUsuniecia w którym będziemy przechowywać wszystkie indeksy pól na których znajdują się kule
        które na końcu metody usuniemy. Dla indeksów od 0 do 95 sprawdzamy po kolei czy w rzędzie na prawo, w dół, na
        ukos w prawo-dół i na ukos w lewo-dół znajdują się co najmniej 4 kule w kolorze kuli znajdującej się na polu o
        aktualnie badanym indeksie (pomijamy puste pola), jeśli tak do dodajemy je wszystkie do zbioru kuleDoUsuniecia.
        Na koniec usuwamy wszystkie kule znajdujące się na polach o indeksach znajdujących się w kuleDoUsunięcia i
        zwiększamy zmienną liczbaPustychPol o długość zbioru kuleDoUsuniecia.
        """
        kuleDoUsuniecia = set([])
        for i in xrange(96):
            if self.listaZawartosciPol[i]:
                kolorKuli = self.listaZawartosciPol[i]
                #sprawdzenie czy w rządzie na prawo znajdują się kule w kolorze ten na pozycji i
                aktualnaPozycja = i + 1
                kuleWRzedzie = 1
                while aktualnaPozycja < (i / 10 + 1) * 10 and self.listaZawartosciPol[aktualnaPozycja] == kolorKuli:
                    aktualnaPozycja += 1
                    kuleWRzedzie += 1
                if kuleWRzedzie > 4:
                    kuleDoUsuniecia = kuleDoUsuniecia | set(range(i, i + kuleWRzedzie))

                # sprawdzenie czy w rządzie na dół znajdują się kule w kolorze ten na pozycji i
                aktualnaPozycja = i + 10
                kuleWRzedzie = 1
                while aktualnaPozycja < 100 and self.listaZawartosciPol[aktualnaPozycja] == kolorKuli:
                    aktualnaPozycja += 10
                    kuleWRzedzie += 1
                if kuleWRzedzie > 4:
                    kuleDoUsuniecia = kuleDoUsuniecia | set(range(i, i + 10 * kuleWRzedzie, 10))

                # sprawdzenie czy na ukos prawo-dół znajdują się kule w kolorze ten na pozycji i
                aktualnaPozycja = i + 11
                kuleWRzedzie = 1
                while aktualnaPozycja < 100 and aktualnaPozycja % 10 >= i % 10 and self.listaZawartosciPol[aktualnaPozycja] == kolorKuli:
                    aktualnaPozycja += 11
                    kuleWRzedzie += 1
                if kuleWRzedzie > 4:
                    kuleDoUsuniecia = kuleDoUsuniecia | set(range(i, i + 11 * kuleWRzedzie, 11))

                # sprawdzenie czy na ukos lewo-dół znajdują się kule w kolorze ten na pozycji i
                aktualnaPozycja = i + 9
                kuleWRzedzie = 1
                while aktualnaPozycja < 100 and aktualnaPozycja % 10 <= i % 10 and self.listaZawartosciPol[aktualnaPozycja] == kolorKuli:
                    aktualnaPozycja += 9
                    kuleWRzedzie += 1
                if kuleWRzedzie > 4:
                    kuleDoUsuniecia = kuleDoUsuniecia | set(range(i, i + 9 * kuleWRzedzie, 9))

        #usunieciu kul
        for pozycja in kuleDoUsuniecia:
            self.listaZawartosciPol[pozycja] = 0
            self.listaPrzyciskowPlanszy[pozycja].set_image(self.pustyObraz)

        self.liczbaPustychPol += len(kuleDoUsuniecia)


def main():
    """Inicjuje gre pooprzez wywołanie konstruktora klasy Kulki."""
    Kulki()

if __name__ == '__main__':
    main()