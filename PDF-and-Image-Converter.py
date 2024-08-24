"""
This version splits pdf into jpg first

Try combine search into single function using single=True - Done
Add intereface to select to sort instead of typing for file ordering - WTF how
Add loading bar if possible - Done (pdf to image cannot. Tried editing code in Popen but idk how)


pip install PyPDF2
pip install Pillow
pip install pdf2image  (https://www.youtube.com/watch?v=IDu46GjahDs    - Save poppler to Program Files (x86)
"""

import os
import shutil

from tkinter import filedialog, Tk
from pdf2image import convert_from_path
from PIL import Image
from PyPDF2 import PdfMerger

#Before converting using pyinstaller change this
poppler_path = r'C:\Program Files (x86)\poppler\Library\bin'
#poppler_path = r'_internal\poppler\bin'

allowed_ext = ['jpg', 'jpeg','png','bmp'] #Have not tried otheer extension
Image.MAX_IMAGE_PIXELS = None   #Remove warning message from working with large image

def get_files(size, filetypes = [('All files','*.*')]):
    global current_folder_dir   #Allows the access of temp file my main() to delete in case need
    root = Tk()
    currdir = os.getcwd()

    if size == 'multiple':
        file_dir = filedialog.askopenfiles(filetypes=filetypes, parent=root, initialdir='shell:MyComputerFolder', title='Select your files (PDF/JPG)')
        if file_dir == '':      #filedialog returns '' for multiple selection
            return [],[],[],[]
        current_folder_dir = '/'.join(file_dir[0].name.split('/')[:-1])  #get folder of where files is stored
    elif size == 'single':
        file_dir = filedialog.askopenfile(filetypes=filetypes, parent=root, initialdir='shell:MyComputerFolder', title='Select a file (PDF)')
        if file_dir == None:    #filedialog returns NoneType for single selection
            return [],[],[],[]
        current_folder_dir = '/'.join(file_dir.name.split('/')[:-1])
    else:
        print('def search_for_file_path size not set properly')
        file_dir, current_folder_dir = [], []
    try:
        root.destroy()
    except:
        next    #if popup close without selecting

    dir_list, name_list, ext_list = [], [], []

    if size == 'single':
        file_name_ext = file_dir.name.split('/')[-1]
        file_ext = file_name_ext.split('.')[-1]
        if file_ext in allowed_ext or file_ext == "pdf":
            dir_list.append(file_dir.name)     #name property of the class contains the dir
            name_list.append(file_name_ext)
            ext_list.append(file_ext)
        else:
            print('{} not used as extension is not allowed'.format(file_name_ext))
            
        
    else:
        for each_file in file_dir:
            file_name_ext = each_file.name.split('/')[-1]    #gets the file_name.file_ext from a full dir
            file_ext = file_name_ext.split('.')[-1]
            if file_ext in allowed_ext or file_ext == "pdf":
                dir_list.append(each_file.name)     #name property of the class contains the dir
                name_list.append(file_name_ext)
                ext_list.append(file_ext)
            else:
                print('{} not used as extension is not allowed'.format(file_name_ext))
    print()
    return dir_list, name_list, ext_list
    #Returns list of dir of files, name.ext of file, dir of folder
    #The base for getting code for all the functions

def file_ordering(dir_list, name_list):
    length = len(dir_list)
    aval_choices = list(range(1, length+1 + 1)) #list of choice avaliable including exit

    text = 'Select no. to order\n'
    new_dir_list, new_name_list, new_ext_list = [],[],[]
    for i in range(length):
        text += """\t{}) {}\n""".format(i+1, name_list[i])
    text += "{}) End your ordering\n".format(length+1)

    while True:
        print(text)
        choice = input('Select a file:')
        if (choice.isdigit() == True) and (int(choice) in aval_choices):
            choice = int(choice)
            if choice == length+1: #exit ordering
                break
            
            new_dir_list.append(dir_list[choice-1])
            new_name_list.append(name_list[choice-1])
            new_ext_list.append(name_list[choice-1].split('.')[-1])
            print("\nNew order: " + ', '.join(new_name_list) + '\n')
        else:
            print('\nNot an option\n')
    return new_dir_list, new_name_list, new_ext_list
    #Returns the sorted dir list and the sorted list of name.ext
    #See of can do an interactivee one using images

def jpg_to_pdf_only(jpg_list, new_pdf_dir): 
    image_list= []
    temp = 0
    for each in jpg_list:
        print_percent_done(temp,len(jpg_list),title="Combining files")
        temp += 1
        #print(each)
        image_list.append( Image.open(r'{}'.format(each)).convert('RGB') )
    image_list[0].save(r'{}.pdf'.format(new_pdf_dir), save_all=True, append_images=image_list[1:])
    return new_pdf_dir+'.pdf'
    #convert a list of dir of jpg into pdf

def pdf_converter(resize=False):
    try:
        dir_list, name_list, ext_list = get_files('multiple')
    except:
        print("Invalid Option")
        return

    if dir_list == []:    
        print('No file selected')
        print('Exiting program')
        return
    
    #Reorder files to combine
    print("Current order = \n\t{}".format('\n\t'.join(name_list)))
    if input("Reorder? (y/not y): ") == 'y':
        temp_dir_list, temp_name_list, new_ext_list = file_ordering(dir_list, name_list)
        if temp_dir_list != []:
            dir_list, name_list, ext_list = temp_dir_list, temp_name_list, new_ext_list
        else:
            print('No ordering done')
            print('Using original order')
#need do change to pdf if just 1 jpg or end if 1 jpg/pdf? idk prob no issue

    while True:
        name = input("Input name for new pdf: ")
        if name+'.pdf' in name_list:
            print('File name already exists in folder, choose a new name')
            continue
        else:
            break

    temp_path = current_folder_dir + '/Temp_Folder (Do not remove during operation)'
    while True:
        if os.path.exists(temp_path):
            input("Please delete temp folder and press Enter")
            continue
        os.makedirs(temp_path)
        break

    if resize:
        del_list = convert_and_resize_into_pdf(dir_list, name_list, ext_list, temp_path, name)
    else:
        del_list = convert_to_pdf(dir_list, name_list, ext_list, temp_path, name)

    print('Deleting temp folder')
    for each in del_list:
        try:
            os.remove('{}'.format(each)) #remove temp file
        except:
            continue
    try:
        if temp_path != None:
            shutil.rmtree(temp_path) #remove temp folder
    except Exception as e:
        print(e)
        print ("Error occured, temp file not found. Some issue may occur")
    return


def convert_and_resize_into_pdf(dir_list, name_list, ext_list, temp_path, name):
    new_dir_list = []
    print()

    temp_no = 0
    for i in range(len(name_list)):
        if ext_list[i] in allowed_ext:
            curr_ext = ext_list[i]
            print('Copying file {}'.format(name_list[i]))
            shutil.copyfile(dir_list[i], temp_path+'/{}.'.format(temp_no) + curr_ext)
            new_dir_list.append(temp_path+'/{}.'.format(temp_no) + curr_ext)
            temp_no += 1
        else:
            curr_ext = "bmp"
            print('\nReading and converting {} to images'.format(name_list[i]))
            print('Warning, large number/high resolution pages will take longer, up to ~2s/page')
            images = convert_from_path(dir_list[i], poppler_path=poppler_path)
            print('{} images found in {}\n'.format(len(images), name_list[i]))
            for j in range(len(images)):
                images[j].save(temp_path+ '/{}.'.format(temp_no) + curr_ext, 'bmp')
                new_dir_list.append(temp_path+'/{}.'.format(temp_no) + curr_ext)
                temp_no += 1

    size1, size2 = [], []
    for i in range(len(new_dir_list)):
        image = Image.open(new_dir_list[i])
        size1.append(image.size[0])
        size2.append(image.size[1])
    size1.sort()
    size2.sort()
    #print("Resizing to {}, {}".format(size1[0], size2[0]))
    resize = (size1[0], size2[0])
    print('Resizing images')
    
    for i in range(len(new_dir_list)):
        image = Image.open(new_dir_list[i])
        new = image.resize(resize)
        new.save(temp_path+ '/{}.'.format(i) + curr_ext) 
    
    print('Converting resized images into pdf\n')
    new_pdf_dir = current_folder_dir + '/' + name
    saved_dir = jpg_to_pdf_only(new_dir_list, new_pdf_dir)
    print('File is saved to ({})'.format(saved_dir))
    return new_dir_list
    #Convert pdf into multiple jpg into temp folder, copy normal jpg into temp folder
    #Resize all jpg into the smallest width and length
    #Combine resized jpg into pdf and save to same dir

def pdf_to_jpg():
    try:
        dir_list, name_list, ext_list = get_files('single', [('PDF Files', '*.pdf')])
    except:
        print("Invalid Option")
        return
    #print(dir_list, name_list, ext_list)
    if dir_list == []:    
        print('No file selected')
        print('Exiting program')
        return

    file_dir = dir_list[0]
    file_name = ( file_dir.split('/')[-1] ).split('.')[0]

    path = current_folder_dir + '/' + file_name
    while True:
        if not os.path.exists(path):
            os.makedirs(path)
            break
        else:
            print('Folder name of {} exists. Remove it to continue'.format(file_name))
            input('Press enter to continue')

    print('Warning, large number/high resolution pages will take longer, up to ~2s/page')
    print('Do not close the program')
    images = convert_from_path(file_dir, poppler_path=poppler_path)
    print('{} pages can be found in {}.pdf'.format(len(images), file_name))
    
    for i in range(len(images)):
        images[i].save(path+ '/{} page '.format(file_name)+ str(i+1) +'.bmp', 'BMP')
    print('Images saved in folder named: {}'.format(file_name))
    return
    #Saves complied folder of images into the same dir 

def convert_to_pdf(dir_list, name_list, ext_list, temp_path, name):           
    current = 0     #current pointer
    pdf_list, jpg_list, files_to_be_deleted_list = [],[],[]
    
    while current != len(dir_list):
        if current == 0 and ext_list[current] == 'pdf': 
            #if first file is pdf, add to pdf list and continue
            pdf_list.append(dir_list[current])
            current += 1
            continue
        if ext_list[current] in allowed_ext: 
            #if file is jpg, add to jpg list and loop for the next consecutive jpg
            jpg_list.append(dir_list[current])
            current += 1
            if current == len(dir_list):
            #reach the end of list and is jpg
                new_pdf_dir = temp_path + '/temporary ' + (jpg_list[0].split('/')[-1]).split('.')[0]
                temp_pdf_dir = jpg_to_pdf_only(jpg_list, new_pdf_dir)
                files_to_be_deleted_list.append(temp_pdf_dir)
                pdf_list.append(temp_pdf_dir)
                break
            continue
        else:   
            if jpg_list == []: 
                #if prevous also pdf then continue
                pdf_list.append(dir_list[current])
                current += 1
                continue
            #if current is pdf, convert previous jpg into new pdf 
            #Add the new pdf and current pdf into pdf list
            new_pdf_dir = temp_path + '/temporary ' + (jpg_list[0].split('/')[-1]).split('.')[0]
            temp_pdf_dir = jpg_to_pdf_only(jpg_list, new_pdf_dir)
            files_to_be_deleted_list.append(temp_pdf_dir)   #files to be deleted later
            jpg_list = []
            pdf_list.append(temp_pdf_dir)
            pdf_list.append(dir_list[current])
            current += 1

##    print(pdf_list)
    merger = PdfMerger()
    for pdf in pdf_list:
        merger.append(pdf)

    dir_to_write = current_folder_dir + "/{}.pdf".format(name)
    merger.write(dir_to_write)
    print('File is saved at\n{}'.format(dir_to_write))
    merger.close()  
    return files_to_be_deleted_list
    #Iterate thru list and combine jpg into pdf until hit another pdf
    #At the end combine all the pdf together and save to same dir


def print_percent_done(index, total, bar_len=50, title='Please wait'):
    '''
    index is expected to be 0 based index. 
    0 <= index < total
    '''
    percent_done = (index+1)/total*100
    percent_done = round(percent_done, 1)

    done = round(percent_done/(100/bar_len))
    togo = bar_len-done

    done_str = '█'*int(done)
    togo_str = '░'*int(togo)

    print(f'\t⏳{title}: [{done_str}{togo_str}] {percent_done}% done', end='\r')

    if percent_done >= 100:
        print('\t✅\n')


def main():
    while True:
        option = input("""1) Convert img/pdf into single pdf (Resize)
2) Convert img/pdf into single pdf (No resize)
3) Convert pdf into img
4) Exit
Input your choice: """)
        option = int(option)
        if option == 1:
            pdf_converter(resize=True)
            break
        elif option == 2:
            pdf_converter(resize=False)
            break
        elif option == 3:
            pdf_to_jpg()
            break
        elif option == 4:
            break
        else:
            print('Not an option')
    input("Press Enter to quit")   
       

main()
