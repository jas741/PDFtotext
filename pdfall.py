import os
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
# From PDFInterpreter import both PDFResourceManager and PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
# Import this to raise exception whenever text extraction from PDF is not allowed
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.layout import LAParams, LTTextBox, LTTextLine
from pdfminer.converter import PDFPageAggregator
import textract

#intended to be run from the folder you want the new text files to save to, a sibling of the pdf_folder

pdflist = [x for x in os.listdir("../pdf_folder") if x.endswith(".pdf")==True]

for essay in pdflist:
    
    #if distinct pdfs have distinct passwords, `password` should be a list, given before the loop begins.
    password = ""
    extracted_text = ""
        
    # Open and read the pdf file in binary mode
    fp = open(os.path.join("../pdf_folder/" + essay), "rb")

    # Create parser object to parse the pdf content
    parser = PDFParser(fp)
    
    # Store the parsed content in PDFDocument object
    document = PDFDocument(parser, password)
    
    # Check if document is extractable, if not abort
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed

    # Create PDFResourceManager object that stores shared resources such as fonts or images
    rsrcmgr = PDFResourceManager()
    
    # set parameters for analysis
    laparams = LAParams()
    
    # Create a PDFDevice object which translates interpreted information into desired format
    # Device needs to be connected to resource manager to store shared resources
    # device = PDFDevice(rsrcmgr)
    # Extract the decive to page aggregator to get LT object elements
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    
    # Create interpreter object to process page content from PDFDocument
    # Interpreter needs to be connected to resource manager for shared resources and device
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    
    # Ok now that we have everything to process a pdf document, lets process it page by page
    for page in PDFPage.create_pages(document):
        # As the interpreter processes the page stored in PDFDocument object
        interpreter.process_page(page)
        # The device renders the layout from interpreter
        layout = device.get_result()
        # Out of the many LT objects within layout, we are interested in LTTextBox and LTTextLine
        for lt_obj in layout:
            if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                extracted_text += lt_obj.get_text()
    
    if extracted_text != "":
        
        
        #close the pdf file
        fp.close()
        
        # print (extracted_text.encode("utf-8"))  os.path.join("../splitpom2files/" + essay)
        
        with open(essay.replace(".pdf",".txt"), "wb") as my_log:
            my_log.write(extracted_text.encode("utf-8"))
            print(essay + "  Done !!")


    else:
        text = textract.process(os.path.join("../pdf_folder/" + essay), method='tesseract', language='eng')
        
        #this is an incomplete list and can probably be done more elegantly
        text0 = str(text).replace('\n',' ')
        text1 = text0.replace('\xe2\x80\x99','\'')
        text2 = text1.replace('\xef\xac\x81','fi')
        text3 = text2.replace('\xef\xac\x82','fl')
        text4 = text3.replace('\xe2\x80\x94','-')
        text5 = text4.replace('\xe2\x80\x98','\'')
        
        file = open(essay.replace(".pdf",".txt"),"w", encoding='utf8')
        file.write(str(text5))
        file.close()
        print(essay + "  Done !!")





