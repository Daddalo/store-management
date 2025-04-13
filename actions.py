from operation import *

def insert():
    """
    Richiama la funzione presente in operation.py per inserire un prodotto
    """
    insert_product()

def products():
    """
    Richiama la funzione list_products presente in operation.py per visualizzare i prodotti rimanenti
    """
    list_products("products")
    
def sales():
    """
    Richiama la funzione list_products presente in operation.py per visualizzare i prodotti venduti
    """
    list_products("sold_products")
    
def reset():
    """
    Richiama la funzione reset_inventory presente in operation.py per resettare il file json 'new_inventory'
    """
    reset_inventory()

def command_help():
    """
    Stampa i comandi disponibili che il cliente può utilizzare
    """
    print("I comandi disponibili sono i seguenti: \n",
        "(aiuto): mostra i possibili comandi\n",
        "(elenca): elenca i prodotto in magazzino\n",
        "(aggiungi): aggiungi un prodotto al magazzino\n",
        "(profitti): mostra i profitti totali\n",
        "(vendita): registra una vendita effettuata\n",
        "(vendite): elenca lo storico dei prodotti venduti\n",
        "(svuota): resetta il file json\n",
        "(chiudi): esci dal programma\n")

def profits():
    """
    Richiama la funzione see_profits presente in operation.py per visualizzare i profitti lordi e netti
    """
    see_profits()
    
def sell():
    """
    Richiama la funzione sell_profits presente in operation.py per visualizzare i prodotti venduti
    """
    sell_product()