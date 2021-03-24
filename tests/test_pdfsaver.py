import glob 
from legiscrapor import nlpIE
from legiscrapor import pdf_saver as ps 
import pandas as pd 
import os
from os.path import join 
import shutil


#@pytest.fixture
#def text_example():
#    ''' Returns the text for a legal aid document exerpt.''' 
#    with open('./src/legiscrapor/data/legal_aid_examples/legal_aid_example_1.txt', 'r') as f:
#        text = f.read()
#    return text

def test_get_pdf():
    ''' Test that pdf_saver.get_text() works correctly for a nice, high-resolution PDF'''
    text = ps.get_text('./src/legiscrapor/data/pdfsaver_docs/Bangladesh_2000_Legal_Aid_Services_Act_eng.pdf')
    
    # make sure we get all the text. There are 21441 characters expected.
    assert len(text) == 21441

def test_get_doc():
    ''' Test that pdf_saver.get_text() correctly doesn't know what to do with a .doc file'''
    text = ps.get_text('./src/legiscrapor/data/pdfsaver_docs/Pakistan_1999_Bar_Council_Free_Legal_Aid_Rules.doc')
    assert text == ''

def test_get_lowres_pdf():
    ''' Test that pdf_saver.get_text() works correctly for a low-resolution PDF'''
    text = ps.get_text('./src/legiscrapor/data/pdfsaver_docs/Ghana_2018_Legal_Aid_Commission_Act_eng_1.pdf')
   
    # test that this is, indeed, marked as a low-resolution PDF. 
    # Easiest way: check that the low_resolution_pdfs.txt file was created
    assert os.path.isfile('./src/legiscrapor/data/pdfsaver_docs/low_resolution_pdfs.txt')     
   
    # remove temporary files created in processing low-resolution PDFS
    os.remove('./src/legiscrapor/data/pdfsaver_docs/low_resolution_pdfs.txt')
    shutil.rmtree('./src/legiscrapor/data/pdfsaver_docs/temp_images')

    # make sure we get all the text. There are 1164 characters expected.
    assert len(text) == 1164

def test_scan_no_pdfs():
    ''' Test that scan_pdfs() correctly outputs empty DataFrame if there are no PDFs or docs there''' 
    df = ps.scan_pdfs('./src/legiscrapor/data/legal_aid_examples/') 
    assert len(df) == 0

def test_scan_pdfs():
    df = ps.scan_pdfs('./src/legiscrapor/data/pdfsaver_docs/') # expect 5 files -- 4 .pdf, 1 .doc

    # remove temporary files created in processing low-resolution PDFS
    os.remove('./src/legiscrapor/data/pdfsaver_docs/low_resolution_pdfs.txt')
    shutil.rmtree('./src/legiscrapor/data/pdfsaver_docs/temp_images')

    assert len(df) == 5 # there are 5 files 
    assert list(df.columns) == ['Legislation','Example_number','File_name']
    assert list(df['Example_number']) == [1.0,2.0,3.0,4.0,5.0]
