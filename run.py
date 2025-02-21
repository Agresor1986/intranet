from waitress import serve  # Importuje funkciu `serve` z knižnice Waitress, ktorá slúži na spúšťanie WSGI aplikácií.
from rocnikovy_projekt.wsgi import application  # Importuje WSGI aplikáciu z Django projektu. 
# `rocnikovy_projekt.wsgi` je súbor, ktorý obsahuje WSGI aplikáciu potrebnú na spustenie projektu.
serve(application, host='0.0.0.0', port=8000)  # Spustí Django aplikáciu cez Waitress server.
# `application` je WSGI aplikácia, ktorú server obsluhuje.
# `host='0.0.0.0'` znamená, že aplikácia bude dostupná na všetkých sieťových rozhraniach (IP adresách) servera.
# `port=8000` nastavuje port, na ktorom bude aplikácia bežať.








