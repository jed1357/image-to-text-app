from __future__ import unicode_literals
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
import csv
from .forms import ImageForm
import cv2
import numpy as np
import pytesseract
from PIL import Image
from pathlib import Path


BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

def image_upload_view(request):
    """Process images uploaded by users"""
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Get the current instance object to display in the template
            
            img_obj = form.instance
            return render(request, 'uploadform.html', {'form': form, 'img_obj': img_obj})
    else:
        form = ImageForm()
    return render(request, 'uploadform.html', {'form': form})



#image

def t_tesseract():
    pytesseract.pytesseract.tesseract_cmd = "tesseract"

def resize(image):
    img = cv2.imread(image, cv2.IMREAD_UNCHANGED)
    scale_percent = 220 # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    # resize image
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    return resized

# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# noise removal
def remove_noise(image):
    return cv2.medianBlur(image,5)
 
#thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

#dilation
def dilate(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.dilate(image, kernel, iterations = 1)
    
#erosion
def erode(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.erode(image, kernel, iterations = 1)

#opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)


 #ocr definition   
def ocr_core(filename):
    """
    This function will handle the core OCR processing of images.
    """
    t_tesseract()
    cv = resize(filename)
    gray = get_grayscale(cv)
    # thresh = thresholding(gray)
    openn = opening(gray)
    text = pytesseract.image_to_string(openn, lang='eng')  # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
    return text


def convertImage(request):
	img = request.GET.get('img')
	print(img)
	module_dir =  str(BASE_DIR) + img #get current directory

	text = ocr_core(module_dir)
	# print(text)
	return render(request, 'text.html', {'text': text})


