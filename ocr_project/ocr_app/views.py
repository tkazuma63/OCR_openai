from django.shortcuts import render, redirect
from .forms import DocumentForm
from .models import Document
import pytesseract
from PIL import Image
import openai
from django.conf import settings

from openai import OpenAI
client = OpenAI(api_key = settings.OPENAI_API_KEY)

# Tesseractの実行可能ファイルパスを設定
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'  # windowsの場合

# Create your views here.

def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save()
            img = Image.open(document.image.path)
            text = pytesseract.image_to_string(img, lang='jpn')

            response = client.chat.completions.create(
				model="gpt-4o",
				messages=[
					{
						"role": "system",
						"content": "以下のテキストを解析してください:"
					},
					{
						"role": "user",
						"content": text
					}
				],
				max_tokens=500
			)
            analysis = response.choices[0].message

            return render(request, 'ocr_app/result.html', {'text': text, 'analysis': analysis})
    else:
        form = DocumentForm()
    return render(request, 'ocr_app/upload.html', {'form': form})