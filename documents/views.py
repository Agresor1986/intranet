# Importuje pomocné funkcie na spracovanie požiadaviek
from django.shortcuts import get_object_or_404, render, redirect  
from .models import Document  # Importuje model Document
from .forms import DocumentForm  # Importuje formulár pre nahrávanie dokumentov
from django.http import HttpResponseRedirect  # Importuje triedu na presmerovanie HTTP odpovedí
# Dekorátor zabezpečujúci, že funkcie sú prístupné iba prihláseným používateľom
from django.contrib.auth.decorators import login_required  
from django.core.files.storage import default_storage  # Importuje systém na prácu so súbormi v Django
# Funkcia na zobrazenie zoznamu dokumentov prihláseného používateľa
@login_required  # Používateľ musí byť prihlásený, inak ho presmeruje na login stránku
def document_list(request):
    # Získa dokumenty aktuálneho používateľa, zoradené od najnovších
    documents = Document.objects.filter(user=request.user).order_by('-uploaded_at')  
    for document in documents:
        document.file_exists = default_storage.exists(document.file.name)  # Skontroluje, či súbor existuje
    return render(request, 'document_list.html', {'documents': documents})  # Posiela zoznam dokumentov do šablóny
# Funkcia na nahrávanie dokumentu
@login_required  
def upload_document(request):
    if request.method == 'POST':  # Ak používateľ odoslal formulár (POST požiadavka)
        form = DocumentForm(request.POST, request.FILES)  # Vytvorí formulár so zadanými údajmi a súborom
        if form.is_valid():  # Overí, či sú údaje správne
            document = form.save(commit=False)  # Vytvorí objekt, ale zatiaľ ho neuloží do databázy
            document.user = request.user  # Priradí dokument aktuálnemu používateľovi
            document.save()  # Uloží dokument do databázy
            return redirect('document_list')  # Presmeruje používateľa na zoznam dokumentov
    else:  # Ak požiadavka nie je POST, zobrazí prázdny formulár
        form = DocumentForm()
    # Vykreslí stránku s formulárom na nahrávanie dokumentov
    return render(request, 'upload_document.html', {'form': form})  
# Funkcia na odstránenie dokumentu
@login_required  
def delete_document(request, document_id):
    # Získa dokument alebo vráti 404, ak neexistuje alebo nepatrí používateľovi
    document = get_object_or_404(Document, id=document_id, user=request.user)  
    document.delete()  # Vymaže dokument (vrátane fyzického súboru)
    return redirect('document_list')  # Presmeruje používateľa späť na zoznam dokumentov


