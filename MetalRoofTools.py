

__title__ = "MetalRoof Workbench"
__author__ = "Roknabadi"
__url__ = "https://www.freecadweb.org"


from PySide.QtCore import QT_TRANSLATE_NOOP
import FreeCADGui
import FreeCAD
import DraftTools
import os
from pathlib import Path


class ImportPdfAsImage:
    def GetResources(self):
        return {
        "Pixmap": os.path.split(os.path.abspath(__file__))[0]
        + "/resources/icons/pdf.svg",
        "MenuText": QT_TRANSLATE_NOOP(
            "open pdf",
            "Open the pdf file as image",
            ),
        }

    def IsActive(self):
        return True if FreeCADGui.ActiveDocument else False

    def Activated(self):
        convert_pdf_to_image()


class Block(DraftTools.Rectangle):

    def __init__(self):
        super(Block, self).__init__()


def updateLocale():
    FreeCADGui.addLanguagePath(
        os.path.join(os.path.dirname(__file__), "translations")
    )
    FreeCADGui.updateLocale()

def get_save_filename(ext):
    from PySide2.QtWidgets import QFileDialog
    filters = f"{ext[1:]} (*{ext})"
    filename, _ = QFileDialog.getOpenFileName(None, 'select file',
                                              None, filters)
    if not filename:
        return
    if not ext in filename:
        filename += ext
    return filename


def convert_pdf_to_image():
    from pdf2image import convert_from_path
    filename = get_save_filename('.pdf')
    pages = convert_from_path(filename, 500)
    page = pages[0]
    image_path = filename.rstrip("pdf") + "jpg"
    page.save(image_path, "JPEG")
    del(pages)
    name = os.path.basename(filename).rstrip(".pdf")
    image = FreeCAD.ActiveDocument.addObject('Image::ImagePlane',name)
    image.ImageFile = image_path
    string = page.fromstring.__str__()
    i = string.find("size=") + 5
    j = string.find(" at")
    x, y = string[i:j].split("x")
    image.XSize = x
    image.YSize = y
    image.Placement = FreeCAD.Placement(FreeCAD.Vector(0, 0, -1),FreeCAD.Rotation(0, 0, 0, 1))
    FreeCAD.ActiveDocument.recompute()
    FreeCADGui.ActiveDocument.activeView().viewTop()
    FreeCADGui.SendMsgToActiveView("ViewFit")

FreeCADGui.addCommand("import_pdf_as_image", ImportPdfAsImage())
FreeCADGui.addCommand("metal_roof_block", Block())

# List of all metal roof commands
MetalRoofCommands = [
    "import_pdf_as_image",
    "metal_roof_block"
]
