from django.shortcuts import render, redirect
from .forms import DocumentForm
from .models import Document
import pytesseract
from PIL import Image
import openai
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY

# Create your views here.

def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save()
            img = Image.open(document.image.path)
            text = pytesseract.image_to_string(img, lang='jpn')

            response = openai.Completion.create(
                engine="gpt-4o",
                prompt=f"以下のテキストを解析してください:\n\n{text}",
                max_tokens=500
            )
            analysis = response.choices[0].text.strip()

            return render(request, 'ocr_app/result.html', {'text': text, 'analysis': analysis})
    else:
        form = DocumentForm()
    return render(request, 'ocr_app/upload.html', {'form': form})