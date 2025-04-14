import json
import re

PATH_FILE = "inventario_vendite.json"
TEXT_NAME = "Inserisci il nome del prodotto: ".lower()
TEXT_QUANTITY = "Inserisci la quantità: "
TEXT_SELL = "Inserisci il prezzo di vendita: "
TEXT_PURCHASE = "Inserisci il prezzo di acquisto: "
TEXT_ADD_PRODUCT = "Aggiungere un altro prodotto? (si/no): "
NUMERIC_ERROR = "Errore, deve essere un numero"
EMPTY_INVENTORY = "L'inventario è vuoto! Aggiungi un nuovo prodotto"


def load_file_data():
    """
    Carica le informazioni presenti in un file json

    Returns:
        (dict): ritorna un dizionario
    """
    with open(PATH_FILE, "r")as json_file:
        return json.load(json_file)
    
def dump_data(inventory):
    """
    Scarica le informazioni presenti in un dizionario costruendo un file json
    Args:
        inventory (dict): il dizionario da cui costruire il file json
    """
    with open(PATH_FILE, "w") as json_file:
        json.dump(inventory, json_file, indent=4)
    
def reset_inventory():
    """
    Resetta il file json
    """
    inventory = {
        "products":{},
        "sold_products":{},
        "profits":{
            "gross_profits":0.0,
            "net_profits":0.0
        }
    }
    dump_data(inventory)
    print("Inventario svuotato!\n")

def list_products(type_product): 
    """
    Lista i prodotti disponibili o i prodotti venduti

    Args:
        type_product (str): indica il tipo di prodotto da listare, se i products (prodotti disponibili) 
        o sold_products (prodotti venduti)
    """
   
    inventory = load_file_data()
        
    if(type_product == "products"):
        if(products_are_finished(inventory)):
            print(EMPTY_INVENTORY)
        else:
            print(f"{'PRODOTTO':<40}{'QUANTITÀ':<15}{'PREZZO':<15}")
            for product in inventory[type_product]:

                quantity = inventory[type_product][product]["quantity"]
                prezzo = inventory[type_product][product]["sell_price"]
                print(f"{product:<40} {quantity:<15} €{prezzo:<15.2f}")    
    elif(type_product == "sold_products"):
        if(products_are_finished(inventory, type_product)):
            print("Non ci sono ancora vendite effettuate!")
        else:
            for product in inventory[type_product]:

                quantity = inventory[type_product][product]["quantity"]
                print(f"Prodotto:{product}| Quantità:{quantity}")
    else:
        print("Errore con la funzione di list!")
        exit(0)
    
def see_profits():
    """
    Mostra i profitti lordi e i profitti netti
    """
    inventory = load_file_data()
    print("\n")
    print(f"Profitti lordi: €{inventory['profits']['gross_profits']:.2f}",
        f"| Profitti netti: €{inventory['profits']['net_profits']:.2f}")

def insert_product():
    """
    Inserisce un nuovo prodotto da vendere
    """
    inventory = load_file_data()
    product = check_validation_name(input(TEXT_NAME))
    quantity = check_validation_quantity(input(TEXT_QUANTITY))

    if check_if_present(product, "products", inventory):
        inventory["products"][product]["quantity"] += quantity
        print(f"AGGIUNTO: {quantity} X {product}")
        print("\n")
    else:
        sell_price = check_validation_value(input(TEXT_SELL), TEXT_SELL)
        purchase_price = check_validation_value(input(TEXT_PURCHASE), TEXT_PURCHASE)
        sell_price, purchase_price = check_prices(sell_price, purchase_price)
        
        sell_price = round(sell_price,2)
        purchase_price = round(purchase_price,2)
        
        print(f"AGGIUNTO: {quantity} X {product}")
        print("\n")
        inventory["products"][product] = {}
        inventory["products"][product] = {"quantity": quantity, "sell_price":sell_price, "purchase_price":purchase_price}

    dump_data(inventory)

def sell_product():
    """
    Permette di scegliere e vendere uno o più prodotti disponibili
    """
    inventory = load_file_data()
    if(products_are_finished(inventory)):
        print(EMPTY_INVENTORY)
    else:
        product_sold_list = [] #lista per mantenere le informazioni sui prodotti venduti
        while(True):
            product, quantity = check_sell(inventory)

            sell_price = inventory['products'][product]['sell_price']
            purchase_price = inventory['products'][product]['purchase_price']
            
            gross_profit = round(quantity*sell_price,2)
            net_profit = round(gross_profit - (quantity*purchase_price),2)
            insert_profits(gross_profit, net_profit, inventory)

            decrease_quantity(product, quantity, inventory)

            if(check_if_present(product, "sold_products", inventory)):
                inventory['sold_products'][product]['quantity'] += quantity
            else:
                inventory['sold_products'][product] = {}
                inventory['sold_products'][product] = {"quantity": quantity}
            
            update_sold_list(product_sold_list, product, quantity, sell_price)
            if(products_are_finished(inventory) or check_yes_no(input(TEXT_ADD_PRODUCT).lower()) == "no"):
                if(products_are_finished(inventory)):
                    print(EMPTY_INVENTORY)
                break
        print("\n")
        print("VENDITA REGISTRATA")
        tot = 0
        for sale in product_sold_list:
            tot += sale[0]*sale[2]
            print(f"{sale[0]}x {sale[1]} €{sale[2]:.2}")
            
        print(f"Totale: €{tot:.2f}")
        dump_data(inventory)
        
def update_sold_list(product_sold_list, product, quantity, sell_price):
    """
    Aggiorna la lista temporanea dei prodotti venduti 

    Args:
        product_sold_list (list): lista per mantenere le informazioni sui prodotti venduti
        product (str): prodotto venduto
        quantity (int): unità vendute del prodotto
        sell_price (float): prezzo di vendita del prodotto
    """
    not_in_list = True 
    for i,sub_list in enumerate(product_sold_list):
        if product in sub_list:
            product_sold_list[i][0] += quantity
            not_in_list = False
            break
    if(not_in_list):
        product_sold_list.append([quantity,product,sell_price])

def products_are_finished(inventory, where="products"):
    """
    Permette di capire se vi sono prodotti disponibili o meno all'interno dell'inventario

    Args:
        inventory (dict): l'inventario da esaminare

    Returns:
        bool: ritorna True se non sono presenti prodotti, ritorna False se ci sono ancora prodotti
    """
    if(len(inventory[where]) == 0): return True
    else: return False

def decrease_quantity(product, quantity, inventory):
    """
    Decrementa le unità disponibili di un prodotto che viene venduto

    Args:
        product (str): il prodotto di cui decrementare le unità disponibili
        quantity (int): numero che rappresenta quanto decrementare
        inventory (dict): dizionario da cui prendere le informazioni
    """
    inventory['products'][product]['quantity'] -= quantity
    if(inventory['products'][product]['quantity'] == 0):
        try:
            inventory['products'].pop(product)
        except KeyError as e:
            print(e)
            
def check_prices(sell_price, purchase_price):
    """
    Controlla se il prezzo di vendita è inferiore a quello di acquisto e fa reinserire i valori

    Args:
        sell_price (float): prezzo di vendita
        purchase_price (float): prezzo di acquisto
    
    Returns:
        sell_price, purchase_price (float), (float): prezzo di vendita e di acquisto validi
    """
    while(True):
        if(sell_price < purchase_price):
            print("Il prezzo di vendita deve essere maggiore di quello d'acquisto!")
            sell_price = check_validation_value(input(TEXT_SELL), TEXT_SELL)
            purchase_price = check_validation_value(input(TEXT_PURCHASE), TEXT_PURCHASE)
        else: break
    return sell_price, purchase_price

def check_sell(inventory):
    """
    Controlla all'interno di un inventario se sono validi nome e quantità del prodotto da vendere

    Args:
        inventory (dict): l'inventario in cui controllare

    Returns:
        product, quantity (str), (int): il nome del prodotto e la quantità validi
    """
    while(True):
        print("\n")
        product = check_validation_name(input(TEXT_NAME))
        if(not check_if_present(product, "products", inventory)):
            print("\n")
            print("Prodotto non presente!")
            continue
        else: break

    while(True):
        quantity = check_validation_quantity(input(TEXT_QUANTITY))
        if quantity > inventory['products'][product]['quantity']:
            print("\n")
            print(f"La quantità inserita({quantity})",
            f"supera il numero di prodotti presenti ({inventory['products'][product]['quantity']})")
            continue
        else: break
    return product, quantity

def insert_profits(gross_profit, net_profit, inventory):
    """
    Aggiorna i profitti lordi e netti dopo una vendita
    Args:
        gross_profit (float): profitto lordo di una vendita da aggiungere
        net_profit (float): profitto netto di una vendita da aggiungere
        inventory (dict): inventario in cui aggiornare i dati
    """
    inventory['profits']['gross_profits'] += gross_profit
    inventory['profits']['net_profits'] += net_profit

def check_yes_no(answer):
    """
    Controlla se il cliente inserisce una risposta valida (si o no)

    Args:
        answer (str): risposta del cliente

    Returns:
        answer (str): risposta valida
    """
    while(True):
        try:
            assert(answer == "si" or answer == "no"), "Devi rispondere con si o no!"
            break
        except AssertionError as e:
            print(e)
            answer = input("\n" + TEXT_ADD_PRODUCT)
    return answer

def check_if_present(product, where, inventory):
    """
    Controlla se un prodotto è già presente tra i prodotti disponibili o in quelli venduti

    Args:
        product (str): nome del prodotto
        where (str): prodotti disponibili ("products"), prodotti venduti ("sold_products")
        inventory (dict): l'inventario in cui controllare

    Returns:
        (bool): ritorna True se il prodotto è già presente, False se non è presente
    """
    if product in inventory[where]:
        return True
    else: return False

def check_validation_name(product):
    """
    Controlla se il nome del prodotto inserito dal cliente è valido

    Args:
        product (str): nome del prodotto

    Returns:
        product (str): nome del prodotto valido
    """
    while(True):
        try:
            assert(bool(re.match(r"^[a-zA-Z\s]+$", product))), "I nomi dei prodotti non prevedono numeri"
            break
        except AssertionError as e:
            print(e)
            product = input("\n" + TEXT_NAME)
    return product

def check_validation_quantity(quantity):
    """
    Controlla se la quantità inserita dal cliente è valida

    Args:
        quantity (str): quantità inserita dal cliente

    Returns:
        quantity (int): quantità valida
    """
    while(True):
        try:
            quantity = int(quantity)
            break
        except ValueError as e:
            quantity = input(NUMERIC_ERROR + " intero\n" + TEXT_QUANTITY)
    return quantity

def check_validation_value(value, text):
    """
    Controlla se il prezzo di vendita o di acquisto inserito dal cliente è valido

    Args:
        value (str): valore inserito dal cliente 
        text (str): testo stampato per differenziare il prezzo di vendita da quello d'acquisto 

    Returns:
        value (float): prezzo del prodotto valido
    """
    while(True):
        try:
            value = float(value)
            break
        except ValueError as e:
            value = input(NUMERIC_ERROR + " float\n" + text)
    return value