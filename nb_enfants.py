# -*- coding: utf-8 -*-

#Import des librairies"import numpy as np
import sys
import os
import pytesseract
import numpy as np
import re
from cv2 import cv2
from pytesseract.pytesseract import image_to_string, image_to_osd #OSD pour gérer l'inclinaison de l'image
from spellchecker import SpellChecker
from pdf2image import convert_from_path

#Chemin du fichier
pathname = os.path.dirname(sys.argv[0])

#.exe de pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

#paramètes de pytesseract
custom_config = r'--oem 3 --psm 6'

#paramètre de spellchecker
spell = SpellChecker(language='fr', distance=1)

#Chargement des stopwords
stopwords = open(pathname + "/stopwords.txt",'r', encoding= 'utf-8').read().split('\n')

#Fonction pour mettre les images en gris
def get_grayscale(image) :
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


#for i in os.listdir(pathname + "/PDF"):

#Conversion du pdf en image
images = convert_from_path(pathname + "/PDF/livret famille 1.pdf", dpi=300, use_pdftocairo=True, strict=False, poppler_path=pathname + "/poppler-21.03.0/Library/bin")

## TU VEUX CETTE PARTIE

l = len(images)

if l == 1 : #Seulement la page de mariage
    nb_enfants = 0

elif l <= 3 : # la page mariage + premier enfant (+ page 2e et 3e enfant)
    nb_enfants = 1

else :
    nb_enfants = (l-3)*2 + 1 #(nb de pages - 2 premières pages - dernière page)*2 + (enfant 2e page)

####
"""
Traitement de ML

nb_enfants_estimés

nb_enfants = nb_enfants + nb_enfants_estimés
"""
