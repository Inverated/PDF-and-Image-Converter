# PDF-and-Image-Converter

Created this a few years back when i couldnt find a free and reliable way to convert files between PDFs and images.
##
2 Functions avaliable:
-  Convert PDF to JPG
-  Convert JPGs and/or PDFs to a single PDF file (With option to resize all the pages to be the same)


## Download Options
-  Executable file in executable …
-  Python file if you want to see the badly written code from when i just started


## Executable
Download the folder and run the executable, leave the _internal folder alone
- Trying to run it after a few months, the exe does not work. idk help
## OR
## Python
The following packages must be installed first

```cmd
pip install PyPDF2
pip install Pillow
pip install pdf2image
```
Download [Poppler](https://poppler.freedesktop.org/) and unzip it in your C:\Program Files (x86)\
or\
Replace the poppler_path in line 22


## How to Use
Select the option you want
### Converting PDF to JPG
-  One PDF at a time
-  Outputs all the images into a folder with the same name as the PDF

### Converting to PDF
-  Can select multiple files at once (Will exclude files with wrong extension)
  -  Extensions recognised -> jpg, jpeg, png, bmp, pdf
-  You can reorder the files (Finish ordering without selecting any option will revert to original)
-  Resize option will cconvert the PDF to image first, which is slower

## Issues
- IDK how add loading when converting from PDF to images
  - Tried editing the convert_from_path method and Popen but no idea how
-  Large PDF files sometimes takes really long randomly

## Note
-  No UI, everything is in cmd. Will try to learn for other projects but not this for now.
-  Maybe add option to choose output format for image when i get to it
-  For Windows only
