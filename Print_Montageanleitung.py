import FreeCAD
import TechDrawGui
import os
import shutil
import sys
from functools import cmp_to_key


def getPages():
    pages = []
    group = FreeCAD.ActiveDocument.findObjects(Type = "App::DocumentObjectGroup", Label="Plan_Zeichnungen")[0]

    for o in group.Group:
        if o.TypeId == "TechDraw::DrawPage":
            pages.append(o)
    
    return sorted(pages, key=cmp_to_key(pageComparator))

def isDeckblatt(p):
    return p.Label == 'Deckblatt'

def getSchnittplanIndex(p):
    if not p.Label.startswith('Schnittplan'):
        return None
    
    indexString = p.Label[p.Label.rfind('_')+1:]

    return int(indexString)

def getPageNumber(p):
    if 'page_number' in p.PropertiesList:
        return p.getPropertyByName('page_number')
    
    return sys.maxint

def pageComparator(p1, p2):
    if isDeckblatt(p1):
        return -1
    
    if isDeckblatt(p2):
        return 1
    
    p1Schnittplan = getSchnittplanIndex(p1)
    p2Schnittplan = getSchnittplanIndex(p2)

    if p1Schnittplan is not None and p2Schnittplan is not None:
        return p1Schnittplan - p2Schnittplan
    
    if p1Schnittplan is not None:
        return -1
    
    if p2Schnittplan is not None:
        return 1
    
    return getPageNumber(p1) - getPageNumber(p2)


documentDir = os.path.dirname(FreeCAD.ActiveDocument.FileName)
baseDir = os.path.join(documentDir, "Plaene")
tmpDir = os.path.join(baseDir, "tmp")

if os.path.exists(tmpDir):
    shutil.rmtree(tmpDir)

os.makedirs(tmpDir)

pages = getPages()
page_locations = []

print("exporting pages")
for page in pages:
    file = os.path.join(tmpDir, page.Label + ".pdf")
    page_locations.append(file)
    page.ViewObject.Visibility = True
    TechDrawGui.exportPageAsPdf(page, file)

outputFile = os.path.join(baseDir, FreeCAD.ActiveDocument.Name + "_Montage.pdf")
cmd = 'pdfunite '

for loc in page_locations:
    cmd += f' "{loc}"'

cmd += f' {outputFile}'

print("Execute the following command to merge the pages")
print(cmd)
