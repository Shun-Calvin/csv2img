# csv2img

This is a project that save CSV file as PNG images.

## Installation 

Run the following to install: 

```python 
pip install csv2img
```


### Pre-requisite
To use csv2img, make sure that you have installed the package of csv2pdf, fitz and PyMuPDF, since this package is a combination of csv2pdf and fitz.

```python 
pip install csv2pdf
pip install fitz #please install fitz first, else it may crush with PyMuPDF
pip install PyMuPDF
```
#### Usage
``` python 
from csv2img import saveas
saveas(csv_file)
```

##### Example
``` python 
from csv2img import saveas
saveas("data.csv")
```

###### Error Handling
If the occured error is related to the packages of fitz and PyMuPDF, please uninstall these packages and install them again. 

```python 
pip uninstall fitz
pip uninstall PyMuPDF
pip install fitz #please install fitz first, else it may crush with PyMuPDF
pip install PyMuPDF
```
