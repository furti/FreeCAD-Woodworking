import FreeCAD
import TechDrawGui
from os import path

documentDir = path.dirname(FreeCAD.ActiveDocument.FileName)
boms = [drawing for drawing in FreeCAD.ActiveDocument.findObjects(Type="TechDraw::DrawPage") if drawing.Label.startswith("BOM")]

for bom in boms:
  partName = bom.Label[4:]
  bomFile = path.join(documentDir, 'Plaene', 'Stueckliste_' + partName + '.pdf')

  TechDrawGui.exportPageAsPdf(bom, bomFile)
