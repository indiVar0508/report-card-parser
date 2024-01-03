import cv2
import os
import re
import pytesseract
from text_parser import BaseTextParser
from text_parser.utility import get_grayscale, thresholding, dilate

class PytesseractTextParser(BaseTextParser):

    def __init__(self, system_teseract_path=os.environ.get("TESSARACT_PATH", None)) -> None:
        super().__init__()
        if system_teseract_path is not None:
            pytesseract.pytesseract.tesseract_cmd = system_teseract_path

    def _get_image_orientation_angle(self, image):
        osd = pytesseract.image_to_osd(image)
        return int(re.search('(?<=Rotate: )\d+', osd).group(0))

    
    def pre_process_image(self, image_obj, *args, **kwargs):
        """
        Method to do some preprocessing of image
        """
        image_orientation_angle = self._get_image_orientation_angle(image_obj)
        if image_orientation_angle != 0:
            # FIXME: This gets stuck for sometimes??
            # FIXME: Bad assumption of rotated images at 90 degrees.
            assert image_orientation_angle % 90 == 0
            number_of_turns = (360-image_orientation_angle) // 90
            print(f"Detected imaage rotated at {image_orientation_angle}, rotating {number_of_turns} times in counter-clock-wise direction at 90 degree")
            # image_obj = cv2.rotate(image_obj, number_of_turns * cv2.ROTATE_90_COUNTERCLOCKWISE)
            for i in range(number_of_turns):
                image_obj = cv2.rotate(image_obj, number_of_turns * cv2.ROTATE_90_COUNTERCLOCKWISE)

        gray_img = get_grayscale(image_obj)
        threshold_img = thresholding(gray_img)
        return threshold_img

    def extract_text(self, image_obj, *args, **kwargs):
        """
        Method responsible to parse the given cv2.imread object.
        """
        contours, _hierarchy = cv2.findContours(image_obj, cv2.RETR_EXTERNAL, 
												cv2.CHAIN_APPROX_NONE)
        
        extracted_text_blob = ""
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            
            # Drawing a rectangle on copied image
            rect = cv2.rectangle(image_obj, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Cropping the text block for giving input to OCR
            cropped = image_obj[y:y + h, x:x + w]

            text = pytesseract.image_to_string(cropped)
            extracted_text_blob += text

        return extracted_text_blob
