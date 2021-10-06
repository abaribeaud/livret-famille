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
#stopwords = open(pathname + "/stopwords.txt",'r', encoding= 'utf-8').read().split('\n')

#Fonction pour mettre les images en gris
def get_grayscale(image) :
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


for i in os.listdir(pathname + "/PDF"):

    #Conversion du pdf en image
    imgs = convert_from_path(pathname + "/PDF/" + i, dpi=500, use_pdftocairo=True, strict=False, poppler_path=pathname + "/poppler-21.03.0/Library/bin")

    #Etapes de traitement des images , puis en texte, puis on ne garde que les mots clefs
    for page in imgs :
        
        #L'image est convetie en gris
        gray = get_grayscale(np.array(page))

        #L'image est convetie en texte
        page = image_to_string(gray, config=custom_config, lang='fra')

        #Les retours à la lignes sont retirés
        page = page.replace('\n', ' ')

        #Les chiffres sont retirés du texte
        page = re.sub(r'\d', '', page)

        #Les caractères deviennent tous minuscules
        page = page.lower()

        #Les caractères spéciaux ne sont pas conservés
        page = re.sub("[0-9]|[/\|={}:,-;]|[\*]|[\_]|[\.]|[\!]|[\?]|[\—]|[^\w\s]","",page)

        #Seul les mots français avec plus de 3 lettres sont conservés
        page = " ".join([spell.correction(mot) for mot in page.split(' ')if len(mot) > 3]) #mot.strip() not in stopwords and

        #Le texte du document est enregistré
        f=open(pathname + '/Output/' + i[0:-3] + 'txt','w', encoding='utf-8')
        f.write(page)
        f.close()


