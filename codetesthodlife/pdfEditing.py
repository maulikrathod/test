import os
from reportlab.pdfgen.canvas import Canvas
from pdfrw import PdfReader
from pdfrw.toreportlab import makerl
from pdfrw.buildxobj import pagexobj


def SetHeaderFooter(inputFile, outputFile, logoFile):
    try:
        ## Read Pdf
        reader = PdfReader(inputFile)
        pages = [pagexobj(p) for p in reader.pages] ## Total Pages

        # compose new pdf
        canvas = Canvas(outputFile)

        for page_num, page in enumerate(pages, start=1):
            # Add page
            canvas.setPageSize((page.BBox[2], page.BBox[3]))
            canvas.doForm(makerl(canvas, page))
            # Draw Header-Footer
            footer_text = "It’s easy to play any musical instrument:"
            footer_text1 = "all you have to do is touch the right key at the right time and the instrument will play itself."
            header_text = "Jhon institute"
            x = 540
            y = 50
            hw = 120
            ## Canvas properties
            canvas.saveState()
            canvas.setStrokeColorRGB(0, 0, 0)
            canvas.setLineWidth(0.5)
            canvas.setFont('Helvetica-Bold', 11)
            canvas.drawString(page.BBox[2] - x, 35, footer_text)
            canvas.drawString(page.BBox[2] - x, 20, footer_text1)
            canvas.drawString(page.BBox[2] - 150, page.BBox[3] - y, header_text)
            canvas.drawImage(logoFile, page.BBox[2] - x, page.BBox[3] - 100, width=hw, height=hw, preserveAspectRatio=True)
            canvas.restoreState()

            canvas.showPage()
        canvas.save()
        return True
    except:
        return False
