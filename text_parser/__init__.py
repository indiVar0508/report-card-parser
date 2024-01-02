import cv2

class BaseTextParser:
    """
    BaseParser BluePrint that defines high level structural Blueprint for parser
    """

    def __init__(self) -> None:
        """
        Add Init logic to initialize a library to be used by the parser.
        """
        ...

    @classmethod
    def read_image(cls, img_path, **imread_kwargs):
        return cv2.imread(img_path, **imread_kwargs)
    
    def pre_process_image(self, image_obj, *args, **kwargs):
        """
        Method to do some preprocessing of image
        """
        return image_obj

    def extract_text(self, *args, **kwargs):
        """
        Method responsible to parse the given cv2.imread object.
        """
        raise NotImplementedError()
    
    def post_process_output(self, output, *args, **kwargs):
        """
        Method to do output massaging on top of extracted text.
        """
        return output
    
    def parse(self, image_path, *args, **kwargs):
        image_obj = self.read_image(image_path, **kwargs)
        processed_image = self.pre_process_image(image_obj, *args, **kwargs)
        extracted_text = self.extract_text(processed_image, *args, **kwargs)
        return self.post_process_output(extracted_text, *args, **kwargs)
