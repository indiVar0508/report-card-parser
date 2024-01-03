import os
from text_parser.report_card_parser import ReportCardParser 

parser_obj = ReportCardParser()

report_cards = [
    "sample-reports/Sample1.png",
    "sample-reports/Sample2.png",
    "sample-reports/Sample1-rotated-180.png",
    "sample-reports/Sample1-rotated-90-clockwise.png",
    "sample-reports/Sample1-rotated-90-cc.png",
]

for report_card in report_cards:
    json_output = parser_obj.parse(report_card)
    print(json_output)