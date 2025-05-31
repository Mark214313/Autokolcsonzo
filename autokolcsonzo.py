from abc import ABC, abstractmethod

class Auto(ABC):
    def __init__(self, rendszam, tipus, berleti_dij):
        self.rendszam = rendszam
        self.tipus = tipus
        self.berleti_dij = berleti_dij
        self.foglalt = False

    @abstractmethod
    def auto_info(self):
        pass


class Szemelyauto(Auto):
    def __init__(self, rendszam, tipus, berleti_dij, ajtok_szama):
        super().__init__(rendszam, tipus, berleti_dij)
        self.ajtok_szama = ajtok_szama

    def auto_info(self):
        return f"Személyautó - Rendszám: {self.rendszam}, Típus: {self.tipus}, Ajtók: {self.ajtok_szama}, Díj: {self.berleti_dij}Ft/nap"


class Teherauto(Auto):
    def __init__(self, rendszam, tipus, berleti_dij, teherbiras):
        super().__init__(rendszam, tipus, berleti_dij)
        self.teherbiras = teherbiras

    def auto_info(self):
        return f"Teherautó - Rendszám: {self.rendszam}, Típus: {self.tipus}, Teherbírás: {self.teherbiras}kg, Díj: {self.berleti_dij}Ft/nap"


class Berles:
    def __init__(self, auto, datum):
        self.auto = auto
        self.datum = datum

    def ar(self):
        return self.auto.berleti_dij

    def __str__(self):
        return f"{self.auto.rendszam} ({self.auto.tipus}) - Dátum: {self.datum}, Ár: {self.ar()}Ft"


class Autokolcsonzo:
    def __init__(self, nev):
        self.nev = nev
        self.autok = []
        self.berlesek = []

    def auto_hozzaadas(self, auto):
        self.autok.append(auto)

    def berles_hozzaadas(self, rendszam, datum):
        auto = self._keres_auto(rendszam)
        if not auto:
            print(" Nem található ilyen rendszámú autó.")
            return
        if auto.foglalt:
            print(" Az autó már foglalt.")
            return
        berles = Berles(auto, datum)
        auto.foglalt = True
        self.berlesek.append(berles)
        print(f" Sikeres bérlés! Ár: {berles.ar()}Ft")

    def berles_lemondas(self, rendszam):
        for berles in self.berlesek:
            if berles.auto.rendszam == rendszam:
                berles.auto.foglalt = False
                self.berlesek.remove(berles)
                print(f" A(z) {rendszam} rendszámú autó bérlése törölve.")
                return
        print(" Nem található ilyen bérlés.")

    def listaz_berlesek(self):
        if not self.berlesek:
            print(" Nincs aktív bérlés.")
        for berles in self.berlesek:
            print(berles)

    def listaz_autok(self):
        for auto in self.autok:
            status = "Foglalt" if auto.foglalt else "Szabad"
            print(f"{auto.auto_info()} - {status}")

    def _keres_auto(self, rendszam):
        for auto in self.autok:
            if auto.rendszam == rendszam:
                return auto
        return None


def rendszer_inditasa():
    kolcsonzo = Autokolcsonzo("CityRent")

    # 3 autó hozzáadása
    auto1 = Szemelyauto("ABC-123", "Toyota Corolla", 10000, 4)
    auto2 = Teherauto("DEF-456", "Ford Transit", 15000, 2000)
    auto3 = Szemelyauto("GHI-789", "Volkswagen Golf", 12000, 5)

    kolcsonzo.auto_hozzaadas(auto1)
    kolcsonzo.auto_hozzaadas(auto2)
    kolcsonzo.auto_hozzaadas(auto3)

    # 4 bérlés (egy autó újra bérlés után lemondható lesz)
    kolcsonzo.berles_hozzaadas("ABC-123", "2025-05-30")
    kolcsonzo.berles_hozzaadas("DEF-456", "2025-05-30")
    kolcsonzo.berles_hozzaadas("GHI-789", "2025-05-31")
    kolcsonzo.berles_lemondas("DEF-456")  # egy lemondás
    kolcsonzo.berles_hozzaadas("DEF-456", "2025-06-01")

    return kolcsonzo


def menu(kolcsonzo):
    while True:
        print("\n--- Autókölcsönző Menü ---")
        print("1. Autók listázása")
        print("2. Autó bérlése")
        print("3. Bérlés lemondása")
        print("4. Bérlések listázása")
        print("0. Kilépés")

        valasztas = input("Válassz műveletet: ")

        if valasztas == "1":
            kolcsonzo.listaz_autok()
        elif valasztas == "2":
            rendszam = input("Add meg az autó rendszámát: ")
            datum = input("Add meg a bérlés dátumát (YYYY-MM-DD): ")
            kolcsonzo.berles_hozzaadas(rendszam, datum)
        elif valasztas == "3":
            rendszam = input("Add meg a lemondani kívánt autó rendszámát: ")
            kolcsonzo.berles_lemondas(rendszam)
        elif valasztas == "4":
            kolcsonzo.listaz_berlesek()
        elif valasztas == "0":
            print("Kilépés...")
            break
        else:
            print(" Hibás választás!")


if __name__ == "__main__":
    kolcsonzo = rendszer_inditasa()
    menu(kolcsonzo)
