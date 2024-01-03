import os

from fastapi import FastAPI
from text_parser.pytesseract_parser import PytesseractTextParser
from text_parser.report_card_parser import ReportCardParser 

app = FastAPI()

@app.get("/")
def default():
    return "Welcome, add path to URL to get parsed image"

@app.get("text/{image_path}")
def parse_text(image_path: str):
    parser_obj = PytesseractTextParser()
    if not os.path.exists(image_path):
        return "Couldn't find given image path"
    return parser_obj.parse(image_path)

@app.get("report-card/{image_path}")
def parse_report_card(image_path: str):
    parser_obj = ReportCardParser()
    if not os.path.exists(image_path):
        return "Couldn't find given image path"
    return parser_obj.parse(image_path)
