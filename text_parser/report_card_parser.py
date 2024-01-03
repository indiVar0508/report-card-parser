import re
from text_parser.pytesseract_parser import PytesseractTextParser

class ReportCardParser(PytesseractTextParser):

    def _massage_value_based_on_key(self, key, extract_text):
        if key == "Name":
            return ' '.join(extract_text.replace("Name of Student", "").strip().split(" ")[:2])
        elif key == "Roll No.":
            return extract_text.replace("Roll No.", "").strip().split(" ")[0]
        elif key in ("English", "Hindi", "Maths", "Science"):
            score = float(extract_text.split(" ")[-4])
            if score > 100:
                # Sometimes decimal is missed
                score /= 100
            return str(score)
        elif key == "Percentage":
            normalise_marks = lambda x: x / 1_000 if x > 1_000 else x
            numbers = re.findall(r'\d+\.\d+|\d+', extract_text)
            scored = normalise_marks(float(numbers[0])) + normalise_marks(float(numbers[1]))
            out_of = normalise_marks(float(numbers[2]))
            return str(round((scored / out_of)*100, 2)) + ' %'

    def post_process_output(self, output, *args, **kwargs):
        """
        Method to do output massaging on top of extracted text.
        """
        result = {}
        for key, expr in [
            ("Name", r"Name of Student .*"),
            ("Roll No.", r"Roll No\. .*"),
            ("English", r"ENGLISH .*"),
            ("Hindi", r"HINDI .*"),
            ("Maths", r"MATHEMATICS(,?) .*"),  # Sometimes picks comma
            ("Science", r"SCIENCE .*"),
            ("Percentage", r"Total \d.*"),
        ]:
            temp = re.search(expr, output)
            if temp is not None:
                result[key] = self._massage_value_based_on_key(key, temp.group())
            else:
                result[key] = "Failed to parse"
        return result
    