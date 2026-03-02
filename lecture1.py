# Scriviamo un codice python che modelli un semplice
# gestionale aziendale. Dovremo prvedere la possibilità di
# definire entità che modellano i prodotti, i clienti,
# offrire interfacce per calcolare i prezzi, eventualmente
# scontati, ...

class Prodotto:
    aliquota_iva = 0.22 #variabile di classe -- ovvero è la stessa per tutte le istanze che verranno create.

    def __init__(self, name: str, price: float, quantity: int, supplier = None):
        self.name = name
        self._price = None
        self.price = price
        self.quantity = quantity
        self.supplier = supplier

    def valore_netto(self):
        return self._price*self.quantity

    def valore_lordo(self):
        netto = self.valore_netto()
        lordo = netto*(1+self.aliquota_iva)
        return lordo

    @classmethod
    def costruttore_con_quantità_uno(cls, name: str, price: float, supplier: str):
        cls(name, price, 1, supplier)

    @staticmethod
    def applica_sconto(prezzo, percentuale):
        return prezzo*(1-percentuale)

    @property
    def price(self): # eq. getter
        return self._price
    @price.setter
    def price(self, valore):
        if valore < 0:
            raise ValueError("Attenzione, il prezzo non può essere negativo.")
        self._price = valore

    def __str__(self):
        return f"{self.name} - disponibilità {self.quantity} pezzi a {self.price} euro."

    def __repr__(self):
        return f"Prodotto(name = {self.name}, price = {self.price}, quantity = {self.quantity}, supplier = {self.supplier})"

    def __eq__(self, other: object):

        if not isinstance(other, Prodotto):
            return NotImplemented
        return (self.name == other.name
            and self.price == other.price
            and self.quantity == other.quantity
            and self.supplier == other.supplier)
        pass

    def __lt__(self, other: "Prodotto") -> bool:
        return self.price < other.price

    def prezzo_finale (self) -> float:
        return self.price * (1+ self.aliquota_iva)

class ProdottoScontato(Prodotto):
    def __init__(self, name: str, price: float, quantity: int, supplier :None, sconto_percento: float):
        # Prodotto.__init__() primo metodo per chiamare la classe prodotto
        super().__init__(name, price, quantity, supplier) # secondo metodo
        self.sconto_percento = sconto_percento

    def prezzo_finale(self) -> float:
        return self.valore_lordo() * (1-self.sconto_percento/100)

class Servizio(Prodotto):
    def __init__(self, name: str, tariffa_oraria: float, ore: int):
        super().__init__(name= name, price= tariffa_oraria, quantity=1, supplier= None)
        self.ore = ore

    def prezzo_finale(self) -> float:
        return self.price * self.ore


myproduct1 = Prodotto(name = "Laptop", price = 1200.0, quantity=12, supplier="ABC")

print(f"Nome prodotto: {myproduct1.name} - prezzo: {myproduct1.price}")

print(f"Il totale lordo di myproduct1 è {myproduct1.valore_lordo()}") #uso un metodo di istanza
p3 = Prodotto.costruttore_con_quantità_uno("Auricolari", 200.0, "ABC") #Modo per chiamare un metodo di classe.
print(f"Prezzo scontato di myproduct1 {Prodotto.applica_sconto(myproduct1.price, 0.15)}")#Modo per chiamare un metodo statico.

myproduct2 = Prodotto("Mouse", 10, 25, "CDE")
print(f"Nome prodotto: {myproduct2.name} - prezzo: {myproduct2.price}")

print(f"Valore lordo di myproduct1: {myproduct1.valore_lordo()}")
Prodotto.aliquota_iva = 0.24
print(f"Valore lordo di myproduct1: {myproduct1.valore_lordo()}")

print(myproduct1)

p_a = Prodotto( name = "Laptop", price = 1200.0, quantity = 12, supplier="ABC")
p_b = Prodotto(name ="Mouse", price = 10, quantity = 14, supplier = "CDE")

print("myproduct1 == p_a?", myproduct1 == p_a) #va a chiamare il metodo __eq__ appena implementato. Mi aspetto TRUE
print("p_a == p_b?", p_a == p_b)  #FALSE

mylist = [p_a, p_b, myproduct1]
mylist.sort(reverse=True)

print("lista di prodotti ordinata")
for p in mylist:
    print(f"- {p}")

my_product_scontato = ProdottoScontato(name= "Auricolari", price = 320, quantity= 1, supplier = "ABC", sconto_percento=10)
my_service = Servizio(name= "Consulenza", tariffa_oraria= 100, ore= 3)

mylist.append(my_product_scontato)
mylist.append(my_service)

mylist.sort(reverse=True)

for elem in mylist:
    print(elem.name, "->", elem.prezzo_finale())

# Definire una classe abbonamento che abbia come attributi: "nome, prezzo mensile, mesi". Abbondamento dovrà avere un metodo
# per calcolare il prezzo finale ottenuto come prezzo_mensile * mesi
class Abbonamento:
    def __init__(self, nome: str, prezzo_mensile: float, mesi: int):
        self.name = nome
        self.prezzo_mensile = prezzo_mensile
        self.mesi = mesi

    def prezzo_finale(self) -> float:
        return self.prezzo_mensile * self.mesi

abb = Abbonamento ("Software gestionale", 30.0, 24)

mylist.append(abb)
for elem in mylist:
    print(elem.name, "->", elem.prezzo_finale())



def calcola_totale (elementi):
    tot = 0
    for e in elementi:
        tot += e.prezzo_finale()   #implementazione del duck-typing
    return tot

print(f"Il totale è: {calcola_totale(mylist)}")

from typing import Protocol

class HaPrezzoFinale(Protocol):
    def prezzo_finale(self) -> float:
        ... # i tre puntini sono equivalenti al pass. tre puntini sono un placeholder e serve per indicare che io non dovrò
    #scrivere più niente sul protocollo, ma lo farà qualcun altro.

def calcola_totale (elementi: list[HaPrezzoFinale]) -> float:
    return sum(e.prezzo_finale() for e in elementi)

print(f"Il totale è: {calcola_totale(mylist)}")

print("---------------------------------------------------------------------------")
print("Sperimentiamo con dataclass")

from dataclasses import dataclass

@dataclass
class ProdottoRecord:
    name: str
    prezzo_unitario: float

@dataclass
class ClienteRecord:
    name: str
    email: str
    categoria: str

@dataclass
class RigaOrdine:
    prodotto: ProdottoRecord
    quantita: int

    def totale_riga(self):
        return self.prodotto.prezzo_unitario * self.quantita

@dataclass
class Ordine:
    righe: list[RigaOrdine]
    cliente: ClienteRecord

    def totale_netto(self):
        return sum(r.totale_riga() for r in self.righe)

    def totale_lordo(self, aliquota_iva):
        return self.totale_netto() * (1+ aliquota_iva)

    def numero_righe(self):
        return len(self.righe)

@dataclass
class OrdineConSconto(Ordine):
    sconto_percentuale : float

    def totale_scontato(self):
        self.totale_lordo() * (1- self.sconto_percentuale)

    def totale_netto(self):
        netto_base = super().totale_netto()
        return netto_base * (1 - self.sconto_percentuale)

cliente1 = ClienteRecord(name="Mario Rossi", email="mariorossi@example.com", categoria="Gold")
p1 = ProdottoRecord("Laptop", 1200.0)
p2 = ProdottoRecord("Mouse", 20)

ordine = Ordine([RigaOrdine(p1,2), RigaOrdine(p2,10)], cliente1)
ordine_scontato = OrdineConSconto([RigaOrdine(p1,2), RigaOrdine(p2,10)], cliente1, 0.1)

print (ordine)
print ("Numero di righe nell'ordine: ", ordine.numero_righe())
print ("Totale netto: ", ordine.totale_netto())
print ("Totale lordo (IVA 22%): ", ordine.totale_lordo(0.22))

print (ordine_scontato)
print("Totale netto sconto: ", ordine_scontato.totale_netto())
print("Totale lordo scontato: ", ordine_scontato.totale_lordo(0.22))

print("---------------------------------------------------------------------------")



#Scrivere una classe Cliente che abbia i campi "nome", "email", "categoria" ("Gold", "Silver", "Bronze").
#vorremmo che questa classe avesse un metodo che chiamiamo "descrizione"
# che deve restituire una stringa formattata ad esempio
#"Cliente Fulvio Bianchi (Gold) - fulvio@google.com"

#Si modifichi la classe cliente in maniera tale che la proprietà categoria sia "protetta"
# e accetti solo ("Gold", "Silver", "Bronze")

class Cliente:
    def __init__(self, nome, mail, categoria):
        self.nome = nome
        self.mail = mail
        self._categoria = None
        self.categoria = categoria

    @property
    def categoria(self):
        return self._categoria

    @categoria.setter
    def categoria(self, categoria):
        categorie_valide = {"Gold", "Silver", "Bronze"}
        if categoria not in categorie_valide:
            raise ValueError("Attenzione, categoria non valida. Scegliere fra Gold, Silver, Bronze")
        self._categoria = categoria

    def descrizione(self): #to_string
        # "Cliente Fulvio Bianchi (Gold) - fulvio@google.com"
        return f"Cliente {self.nome} ({self.categoria}) - {self.mail}"

c1 = Cliente("Mario Bianchi", "mario.bianchi@polito.it", "Gold")
#c2 = Cliente("Carlo Masone", "carlo.masone@polito.it", "Platinum") errore voluto da noi
print(c1.descrizione())