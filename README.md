### Installation
- https://techviewleo.com/how-to-install-tesseract-ocr-on-ubuntu/
```sh
sudo apt-get install Tesseract-ocr
```

```sh
# setup a virtual env
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Demo Script

Try out by activating virtual environment and then execute demo.py.
```py
python demo.py
```

### Run The App

Bring up the Backend app using
```py
uvicorn app:app --reload
```


### Refs
- https://github.com/tesseract-ocr/tesseract
- https://builtin.com/data-science/python-ocr
- https://www.geeksforgeeks.org/text-detection-and-extraction-using-opencv-and-ocr/
- https://nanonets.com/blog/ocr-with-tesseract