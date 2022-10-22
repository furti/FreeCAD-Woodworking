import FreeCAD
import TechDrawGui
from os import path

documentDir = path.dirname(FreeCAD.ActiveDocument.FileName)
bomFile = path.join(documentDir, 'Plaene', 'Stueckliste.pdf')

TechDrawGui.exportPageAsPdf(FreeCAD.ActiveDocument.BOM, bomFile)
