import FreeCAD
import TechDrawGui
import os
import shutil


def getPages():
    pages = []
    group = FreeCAD.ActiveDocument.findObjects("App::DocumentObjectGroup")[0]

    for o in group.Group:
        if o.TypeId == "TechDraw::DrawPage":
            pages.append(o)

    return pages


documentDir = os.path.dirname(FreeCAD.ActiveDocument.FileName)
baseDir = os.path.join(documentDir, "Plaene")
tmpDir = os.path.join(baseDir, "tmp")

if os.path.exists(tmpDir):
    shutil.rmtree(tmpDir)

os.makedirs(tmpDir)

pages = getPages()

print("exporting pages")
for page in pages:
    file = os.path.join(tmpDir, page.Label + ".pdf")
    TechDrawGui.exportPageAsPdf(page, file)

wildcard = os.path.join(tmpDir, "*.pdf")
outputFile = os.path.join(baseDir, "Montageanleitung.pdf")
cmd = 'pdftk "' + wildcard + '" cat output "' + outputFile + '"'
print("Execute the following command to merge the pages")
print(cmd)
