from django.shortcuts import render
from .forms import DocumentForm

# from PIL import Image
from django.conf import settings
import base64

from openai import OpenAI
client = OpenAI(api_key = settings.OPENAI_API_KEY)

# Function to encode the image
def encode_image(image_path):
	with open(image_path, "rb") as image_file:
		return base64.b64encode(image_file.read()).decode('utf-8')

def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save()
			# Getting the base64 string
            base64_image = encode_image(document.image.path)

            response = client.chat.completions.create(
				model="gpt-4o",
				max_tokens=1024,
				messages=[
					{
						"role": "system",
						"content": "You are an Optical Character Recognition (OCR) machine. \
									You will extract all the characters from the image file in the URL provided by the user, \
									and you will only privide the extracted text in your response. \
									As an OCR machine, You can only respond with the extracted text."
					},
					{
						"role": "user",
						"content": [
							{
								"type": "text",
								"text": "Please extract all characters within the image. Return the only extacted characters. \
										 The output should be in Japanese."
							},
							{
								"type": "image_url",
								"image_url": {
									"url": f"data:image/jpeg;base64,{base64_image}"
								}
							},
						]
					},
				],
			)
            analysis = response.choices[0].message.content

            return render(request, 'ocr_app/result.html', {'analysis': analysis,})
    else:
        form = DocumentForm()
    return render(request, 'ocr_app/upload.html', {'form': form})
