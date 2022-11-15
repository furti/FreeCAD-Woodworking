import FreeCAD
import TechDrawGui
import os


def isLink(o):
    return o.TypeId == "App::Link"


def isBody(o):
    return o.TypeId == "PartDesign::Body"


def getRoot(o):
    root = o

    while isLink(root):
        root = root.LinkedObject

    return root


def getBodies():
    bodies = []
    part = FreeCAD.ActiveDocument.findObjects("App::Part")[0]

    for o in part.Group:
        root = getRoot(o)

        if not isBody(root):
            continue

        doc = root.Document
        name = root.Planname

        bodies.append({"doc": doc, "name": name})

    return bodies


def findCutlist(doc):
    for page in doc.findObjects("TechDraw::DrawPage"):
        if "_Zuschnitt" in page.Name:
            return page

    return None


def populateCutlist(bodies):
    for body in bodies:
        doc = body["doc"]

        cutlist = findCutlist(doc)

        if cutlist is not None:
            body["cutlist"] = cutlist


documentDir = os.path.dirname(FreeCAD.ActiveDocument.FileName)
baseDir = os.path.join(documentDir, "Plaene")
tmpDir = os.path.join(baseDir, "tmp")

if not os.path.exists(tmpDir):
    os.makedirs(tmpDir)

bodies = getBodies()
populateCutlist(bodies)

print("exporting pages")
for body in bodies:
    if "cutlist" in body:
        file = os.path.join(tmpDir, body["name"] + ".pdf")
        TechDrawGui.exportPageAsPdf(body["cutlist"], file)

wildcard = os.path.join(tmpDir, "*.pdf")
outputFile = os.path.join(baseDir, "Schnittliste.pdf")
cmd = 'pdftk "' + wildcard + '" cat output "' + outputFile + '"'
print("Execute the following command to merge the pages")
print(cmd)
