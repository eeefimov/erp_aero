# erp_aero

Test task for erp.aero

**Python version**: 3.10.13

## Libraries:
- PyMuPDF==1.23.5
- pdfminer.six==20221105
  (Note: icecream==2.1.3 is not necessary and is only used for displaying function output and debugging purposes)

**template.pdf** serves as the prototype file.

## Task:
Develop a method that takes a PDF file as input (the file itself is provided as an attachment). The method should read all possible information from the file and return it as a dictionary.

Furthermore, using **template.pdf** as a reference, create a mechanism that checks incoming PDF files for the presence of all elements and verifies their compliance with the structure (placement on the sheet).
