# codice python che modelli un semplice gestionale aziendale.
# Dovremmo prevederre la possibilità di definire entità che modellano i prdototti,
# i clienti, offrire interfacce per calcolare i prezzi, eventualmente scontati

prodotto1_nome = "Laptop"
prodotto1_prezzo = 1200.0
prodotto1_quantità = 5

prodotto2_nome = "Mouse"
prodotto2_prezzo = 12.0
prodotto2_quantità = 15

valore_magazzino = prodotto1_prezzo * prodotto1_quantità + prodotto2_prezzo * prodotto2_quantità

# print (f"Valore totale del mio magazzino {valore_magazzino}")

# così è scomodo, meglio definire una classe

from unicodedata import name


class Prodotto:
    aliquota_iva = 0.22  # variabile di classe -- ovvero è la stessa per tutte le istanze che verrano create.

    def __init__(self, name: str, price: float, quantity: int,
                 supplier: str):  # posso trovare anche "=None" in particolari condizioni
        self.name = name
        self.price = price
        self.quantity = quantity
        self.supplier = supplier

    def valore_netto(self):
        return self.price * self.quantity

    def valore_lordo(self):
        netto = self.valore_netto()
        lordo = netto * (1 + self.aliquota_iva)
        return lordo

    @classmethod
    def costruttore_con_quantità_1(cls, name: str, price: float,
                                   supplier: str):  # i metodi di classe prendono come inupt il cls e non il self
        return cls(name, price, 1, supplier)

    @staticmethod  # essendo un metodo statico, non devo passare ne self ne cls
    def applica_sconto(prezzo, percentuale):
        return prezzo * (1 - percentuale)


myproduct1 = Prodotto(name="Laptop", price=1200.0, quantity=5,
                      supplier="ABC")  # con "=" non è necessario ricordare l'ordine, con ":" si

print(f"Nome prodotto: {myproduct1.name} - prezzo: {myproduct1.price}")

myproduct2 = Prodotto(name="Mouse", price=10, quantity=15, supplier="CDE")
print(f"Nome prodotto: {myproduct2.name} - prezzo: {myproduct2.price}")

print(f"Il totale lordo di myproduct1 è {myproduct1.valore_lordo()}")  # uso un metodo di istanza

p3 = Prodotto.costruttore_con_quantità_1(name="Auricolari", price=200.0,
                                         supplier="ABC")  # modo per chiamare un metodo di classe

print(
    f"Prezzo scontato di myproduct1 {Prodotto.applica_sconto(myproduct1.price, percentuale=0.15)}")  # modo per chiamare un metodo statico


# scriviamo una classe cliente che abbia i campi "nome", "email", "categoria", ("Gold, Silver, Bronze")
# vorremmo che questa classe avesse un metodo che chiamiamo "descrizione" che deve restituire
# stringa formattata ad esempio
# "Cliente Fulvio Bianchi (Gold) - fulvio@google.com"


class Cliente:

    def __init__(self, nome, email, categoria):
        self.nome = nome
        self.email = email
        self.categoria = categoria

    def descrizione(self):
        return f"Cliente {self.nome} ({self.categoria}) - {self.email} "


c1 = Cliente(nome=": Mario Bianchi", email="mario.bianchia@polito.it", categoria="Gold")
print(c1.descrizione())