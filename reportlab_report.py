#!/usr/bin/env python2

"""
Module to create a PDF report with ReportLab.
"""

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Frame
# from reportlab.pdfbase.ttfonts import TTFont  # other fonts
import os.path
import time
from tkinter.filedialog import asksaveasfilename


########## COLORS FROM LOGO ##########
# divide by 256
# (70, 165, 66) - green
# (31, 79, 116) - blue

#################### REPORT ######################
def make_pdf(saved_list, title="SATAlytics Report"):
    """ Creates a PDF from a HTML template with date of today.

    saved_list -- list of tuples (strings), saved images from GUI (title, figpath)
    title -- string, title of report, default: SAVI Analytics Report 
    """   

    # # give unique report name:
    # version = 0
    # report_name = "{} {}.pdf".format(title, time.strftime("%Y%m%d"))
    # while os.path.isfile(report_name):
    #     version += 1
    #     report_name = "{} {} ({}).pdf".format(title, time.strftime("%Y%m%d"), version)

    report_name = asksaveasfilename(title = "Save file", defaultextension = ".pdf")

    c = canvas.Canvas(report_name)
    c.setAuthor("Marijke Thijssen, Giorgos Giatrakis, Mariola Ferreras") # what use
    c.setTitle(title)
    title_page(c, title)
    c.showPage()
    toc_page(c, saved_list)
    c.showPage()
    for i in range(len(saved_list)):
        regular_page(c, saved_list[i][0], saved_list[i][1])
        c.showPage()
    c.save()
    os.startfile(report_name)


def make_manual(title="SATAlytics Manual"):
    """ Creates manual as a PDF.

    title -- string, name of PDF - default: "SATAlytics Manual"
    """
    manual_name = "{}.pdf".format(title)
    c = canvas.Canvas(manual_name)
    c.setAuthor("Marijke Thijssen") # what use
    c.setTitle(title)
    title_page(c, title)
    c.showPage()

    c.save()
    os.startfile(manual_name)    


def title_page(c, title, logo="Logo.png"):
    """ Creates title page. 

    c -- canvas
    logo -- string, path to logo - default: "Logo.png"
    """

    # code for title page
    ## HERE ##
    # code for image
    c.drawImage(resource_path(logo), 60, 580, width=525, height=187.5, mask=None)

    # code for colored block:
    # c.setStrokeColorRGB(0.4, 0.5, 0.3)
    # c.setFillColorRGB(0.4, 0.5, 0.3) #lighter darkgreen)   
    # c.rect(0, 0, 600, 300, stroke=1, fill=1)

    # code colored band with text:
    c.setFillColorRGB(70/256, 165/256, 66/256)  
    c.rect(0, 300, 600, 100, stroke=0, fill=1)
    c.setFont("Times-BoldItalic", 40, leading=None)
    c.setFillGray(1.0) # white text
    c.drawString(50, 335, title)


def toc_page(c, saved_list):
    """ Creates table of contents page. 

    saved_list -- list of tuples (strings), (title, fig)
    c -- canvas
    """
    watermark(c)

    styles = getSampleStyleSheet()
    info = []
    # styles["ToC_info"] = ParagraphStyle("Normal", 
    #     parent=styles["Normal"],
    #     fontSize=12,
    #     fontName="Times-Roman")

    INFO_TXT = "This report was generated by SATAlytics on {}. The software tool SATAlytics summarizes, analyzes and visualizes chemical analysis data.".format(time.strftime("%B %d, %Y"))

    # display title of page
    c.setFont("Helvetica-Bold", 20, leading=None)
    c.drawCentredString(325, 750, "Table of Contents")

    # display table of contents
    ## if using drawString():
    c.setFont("Helvetica-Oblique", 16, leading=None)
    # c.setLineWidth(1)
    # c.setDash(1, 2) #dots
    y = 700
    saved_text = []
    for i in range(len(saved_list)):
        # # if using paragraphs:
        saved_text.append(Paragraph("<i>" + saved_list[i][0] + "</i>", 
            styles["Heading2"]))
        saved_text.append(Paragraph("<para align=\"RIGHT\">{}".format(i+3),
            styles["Heading2"]))

    fr = Frame(65, 150, 515, 550, leftPadding=0, bottomPadding=0,
                rightPadding=0, topPadding=0, id=None, showBoundary=0)
    side_bar(c)
    footer(c)    
    c.setFont("Helvetica-Bold", 20, leading=None) # otherwise green printing  
    for para in saved_text:
        while fr.add(para, c) == 0:
            fr.split(para, c)
            # new page
            c.showPage()
            watermark(c)

            # display title of page
            c.setFont("Helvetica-Bold", 20, leading=None)
            c.drawCentredString(325, 750, "Table of Contents")

            # display table of contents
            c.setFont("Helvetica-Oblique", 16, leading=None)

            fr = Frame(65, 150, 515, 550, leftPadding=0, bottomPadding=0,
                rightPadding=0, topPadding=0, id=None, showBoundary=0)

    # draw line
    c.setLineWidth(1)
    c.setStrokeColorRGB(0, 0, 0)
    c.line(65, 60, 565, 60)   

    info.append(Paragraph(INFO_TXT, styles["Normal"]))
    f = Frame(65, 50, 515, 50, leftPadding=0, bottomPadding=0,
        rightPadding=0, topPadding=0, id=None, showBoundary=0)
    f.addFromList(info, c)
    ## use text object for that

    side_bar(c)
    footer(c)


def regular_page(c, title, fig_path):
    """ Creates regular page. 

    title -- string, title of figure
    fig_path -- string, path to figure
    c -- canvas
    """   
    
    # display title
    # c.setFont("Helvetica-Bold", 20, leading=None)

    styles = getSampleStyleSheet()
    info = []
    info.append(Paragraph(title, styles["Title"]))
    f = Frame(65, 670, 515, 100, leftPadding=0, bottomPadding=0,
    rightPadding=0, topPadding=0, id=None, showBoundary=0)
    f.addFromList(info, c)

    # c.drawCentredString(325, 700, title)

    #display box with image
    c.setStrokeColorRGB(0.3, 0.4, 0.2)
    c.setFillColorRGB(0.3, 0.4, 0.2)
    c.rect(120, 270, 400, 400, stroke=0, fill=0)
    c.drawImage(fig_path, 120, 280, width=390, height=390, mask=None,
        preserveAspectRatio=True)   
   
    # ## check if this is faster for func images: 
    # ## c.drawInlineImage(self, image, x, y, width=None, height=None) 
   
    watermark(c)
    footer(c, 0)
    side_bar(c)


def watermark(c, watermark="watermark.png"):
    """ Sets watermark.

    c -- canvas
    watermark -- string, path to watermark
    """
    c.drawImage(resource_path(watermark), 380, 10, width=200, height=200, mask=None) 
    

def footer(c, pages=1):
    """ Sets footer. Displays copyright and optional page number.
    
    c -- canvas
    pages -- integer, displays page number (True=0, False=1) - default: 1
    """

    # display copyright
    c.setStrokeColorRGB(70/256, 165/256, 66/256)
    c.setFillColorRGB(70/256, 165/256, 66/256)
    c.setFont("Courier", 9, leading=None)
    page = c.getPageNumber()
    c.drawString(65, 20, 
        "(c) SATAlytics by SATA s.l.r.")

    # display page numers
    if pages == 0:
        c.drawRightString(580, 20, "{}".format(page))


def side_bar(c):
    """Sets side_bar.

    c -- canvas
    """
    c.setFillColorRGB(70/256, 165/256, 66/256)
    c.setStrokeColorRGB(70/256, 165/256, 66/256)
    c.rect(20, 0, 25, 850, stroke=1, fill=1)


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)