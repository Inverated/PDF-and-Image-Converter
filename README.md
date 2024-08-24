# PDF-and-Image-Converter

Created this a few years back when i couldnt find a free and reliable way to convert files between PDFs and images.
2 Functions avaliable:
-  Convert PDF to JPG
-  Convert JPGs and/or PDFs to a single PDF file (With option to resize all the pages to be the same)


## Download
-  Python file if you want to see the badly written code
-  Executable file in executable …

## Python File
The following packages must be installed first

```bash
pip install PyPDF2
pip install Pillow
pip install pdf2image
```
Download [Poppler](https://poppler.freedesktop.org/) and unzip it in your C:\Program Files (x86)\
or\
Replace the poppler_path on line 22

## Executable
Run the executable, leave the _internal folder alone

## How to Use
Select the option you want
### Converting PDF to JPG
-  One PDF at a time
-  Outputs all the images into a folder with the same name

### Converting to PDF
-  Can select multiple files at once (Will exclude files with wrong extension)
-  Extensions recognised -> jpg, jpeg, png, bmp, pdf
-  You can reorder the files (Finish ordering without selecting any option will revert to original)
-  Resize option will cconvert the PDF to image first, which is slower

## Issues
-  IDK how add loading when converting from PDF to images
  - Tried editing the convert_from_path method and Popen but no idea how
-  Large PDF files sometimes takes really long randomly



