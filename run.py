from waitress import serve  
from rocnikovy_projekt.wsgi import application  

serve(application, host='0.0.0.0', port=8000)  








