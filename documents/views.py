from django.shortcuts import get_object_or_404, render, redirect  
from .models import Document  
from .forms import DocumentForm  
from django.http import HttpResponseRedirect  
from django.contrib.auth.decorators import login_required  
from django.core.files.storage import default_storage  

@login_required 
def document_list(request):
    documents = Document.objects.filter(user=request.user).order_by('-uploaded_at')  
    for document in documents:
        document.file_exists = default_storage.exists(document.file.name)  
    return render(request, 'document_list.html', {'documents': documents}) 
    
@login_required  
def upload_document(request):
    if request.method == 'POST':  
        form = DocumentForm(request.POST, request.FILES)  
        if form.is_valid():  
            document = form.save(commit=False) 
            document.user = request.user  
            document.save()  
            return redirect('document_list')  
    else:  
        form = DocumentForm()
   
    return render(request, 'upload_document.html', {'form': form})  

@login_required  
def delete_document(request, document_id):
    document = get_object_or_404(Document, id=document_id, user=request.user)  
    document.delete()  
    return redirect('document_list')  


