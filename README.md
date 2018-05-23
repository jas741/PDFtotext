# PDFtotext
Single script to convert a folder of pdfs to a folder of text files - whether they have a text layer or not.

Uses `pdfminer` for PDFs with a text layer, `textract` (`tesseract`) for image scans. Text files obtained via textract may need further processing - my initial use case was word count where some extra code strings didnt matter.

Script runs from the folder you want the text files to open into - assumes a separate folder (pdf_folder) contains the pdfs.
