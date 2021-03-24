import pdfminer.high_level as ph 
import os
from os.path import join
import pytesseract
from PIL import Image
from wand.image import Image as wandimage
import glob 
import pandas as pd 

def get_text(law):
    ## given a law file, extract the text.  
    text = ''

    ## if it's a PDF we use pdfminer. 
    if law.endswith('pdf'):
       #print('pdf document')
       text = ph.extract_text(law)

       ## If not a lot of text is found, let's try converting the PDF to an image, 
       ## and try extracting text from the image file 
       if len(text) < 50:
          pdf_file =  law
          full_file_name = os.path.splitext(pdf_file)
          base = os.path.basename(full_file_name[0]+full_file_name[1])
          low_res_path = full_file_name[0] + full_file_name[1] 
          low_res_path = low_res_path.replace(base,'')
          print("LOW RESOLUTION PDF FILE:",law)
          mfile = open(low_res_path+'low_resolution_pdfs.txt', 'a+')
          mfile.write(law)
          mfile.write('\n')
          mfile.write(' \n')
          mfile.close()
          files = []
          with(wandimage(filename=pdf_file,resolution = 500)) as conn: 
              for index, image in enumerate(conn.sequence):
                  basename = os.path.basename(full_file_name[0]+full_file_name[1])
                  new_path = full_file_name[0] + full_file_name[1] + 'temp_images/'
                  new_path = new_path.replace(basename,'')
                  basename = os.path.splitext(basename)[0]
                  if not os.path.exists(new_path):
                     os.makedirs(new_path)
                  image_name = new_path+basename + "__" + str(index + 1) + '.png'
                  wandimage(image).save(filename = image_name) 
                  files.append(image_name) 
          all_text = [] 
          for f in files:
              text = pytesseract.image_to_string(Image.open(f).convert("RGBA"))
              all_text.append(text) 
          text = ' '.join(map(str,all_text))
       #print(len(text),text[0:10])
    ## if it's a Word doc, well...I don't know what to do. 
    elif law.endswith('doc'):
        print('Word doc. Not sure what to do with these yet')
    return(text)

def scan_pdfs(download_path):
    law_files = []
    for ext in ('*.doc','*.docx','*.pdf'):
      law_files.extend(glob.glob(join(download_path,ext)))

    df = pd.DataFrame()
    i = 0 
 
    if len(law_files) > 0:
       for law in law_files:
         print('**********'+law+'*********')
         text = get_text(law)
         df.loc[i,'Legislation'] = text
         df.loc[i,'Example_number'] = i + 1
         df.loc[i,'File_name'] = law
         i += 1

    return(df)
