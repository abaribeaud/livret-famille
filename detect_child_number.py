import os
import pytesseract
import numpy as np
import sys

from spellchecker import SpellChecker
from pdf2image import convert_from_path
from sklearn.model_selection import cross_val_score
from pytesseract import Output
from PIL import Image
from clean_images import get_gray_scale, remove_noise, deskew
from deskew import determine_skew
from skimage.transform import rotate

# Chemin du fichier
pathname = os.path.dirname(sys.argv[0])

# .exe de pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

CASE_NUMBER = ["n", "ne", "n*"]


def __run__():
    # Retrieve all used files
    for file in os.listdir("PDF"):
        print("[INFO]   Openning %s file for data preparation" % file)

        count_child_final = 0

        # Load pdf images
        images = convert_from_path("PDF/" + file, use_pdftocairo=True, strict=False,
                                   poppler_path=pathname + "/poppler-21.03.0/Library/bin")

        # For each images of each documents
        for image in images[1:]:
            count_child = 0
            image = np.array(image)

            # Converting image in gray scale
            image_gs = get_gray_scale(image)

            custom_config = r"--oem 3 --psm 6"

            # Convert image to string
            print("[INFO]      Converting %s images to string" % file)
            result_txt = pytesseract.image_to_string(image_gs, config=custom_config, lang='fra')

            # Clean string retrieved
            print("[INFO]      Cleaning %s text representation" % file)
            result_txt_cleaned = clean_text(result_txt)

            count_child += detect_child(result_txt_cleaned)
            if count_child == 0:
                try:
                    print("[INFO]      Cleaning %s text representation [blur]" % file)
                    image_blur = remove_noise(image_gs)

                    print("[INFO]      Converting %s images to string [blur]" % file)
                    result_txt = pytesseract.image_to_string(image_blur, config=custom_config, lang='fra')

                    # Clean string retrieved
                    print("[INFO]      Cleaning %s text representation [blur]" % file)
                    result_txt_cleaned = clean_text(result_txt)

                    count_child += detect_child(result_txt_cleaned)
                except:
                    pass

            if count_child == 0:
                try:
                    image_deskew = deskew(image)
                    print("[INFO]      Cleaning %s text representation [deskew]" % file)
                    image_blur = remove_noise(image_deskew)

                    print("[INFO]      Converting %s images to string [blur]" % file)
                    result_txt = pytesseract.image_to_string(image_blur, config=custom_config, lang='fra')

                    # Clean string retrieved
                    print("[INFO]      Cleaning %s text representation [deskew]" % file)
                    result_txt_cleaned = clean_text(result_txt)

                    count_child += detect_child(result_txt_cleaned)

                except:
                    pass

            count_child_final += count_child
        print("[INFO]      %s count %s childs after process" % (file, count_child_final))

def clean_text(text):
    text_split = text.split(sep="\n")

    spell = SpellChecker(language="fr", distance=2)  # fix distance to 1 for shorter run times

    text_output = []

    for text in text_split:
        word_output = ""
        text = text.lower()

        for word in text.split():
            # Check if the word is misspell
            word = spell.correction(word) if spell.unknown([word]) else word

            word_output += " " + word

        text_output.append(word_output)

    return text_output


def detect_child(text):
    count_child = 0

    print(text)
    for sentence in text[:7]:
        words = sentence.split()
        for word in words:
            try:
                # Case : "naissance + CASE_NUMBER + noise
                if word == "naissance" and words[words.index(word) + 1] in CASE_NUMBER and len(
                        words[words.index(word) + 2]) >= 1:
                    count_child += 1
                elif word == "naissance" and words[words.index(word) + 1] not in CASE_NUMBER and len(
                        words[words.index(word) + 1]) > 1:
                    count_child += 1
            except:
                pass
    print("[INFO]      %s child count for this image" % count_child)
    return count_child


if __name__ == '__main__':
    __run__()
