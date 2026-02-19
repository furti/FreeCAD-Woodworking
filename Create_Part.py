import FreeCAD
import FreeCADGui
import os
from pathlib import Path
from PySide2 import QtWidgets
from Korups_Erzeugen import createCorpus

currentDoc = FreeCAD.ActiveDocument

# 1. Settings
documentLocation = QtWidgets.QFileDialog.getSaveFileName(QtWidgets.QApplication.activeWindow(), 'Save as', '', 'Freecad Files (*.FCStd)')[0]
name = os.path.splitext(os.path.basename(documentLocation))[0]
corpusEnabled = QtWidgets.QMessageBox.question(QtWidgets.QApplication.activeWindow(), "Korpus erzeugen", "Willst du einen Korpus erzeugen?",
    QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
    QtWidgets.QMessageBox.StandardButton.Yes)

# 2. Create Document and save it
FreeCAD.newDocument(name)
doc = FreeCAD.getDocument(name)
guidoc = FreeCADGui.getDocument(name)
doc.saveAs(documentLocation)

# 3. Link masse spreadsheet
try:
  doc.addObject('App::Link', 'Masse').setLink(FreeCAD.getDocument('Masse').Spreadsheet)
  doc.recompute(None,True,True)
except NameError:
  print('Masse Spreadsheet not linked. Document not found')

# 4. Create Part
doc.addObject('App::Part', name)
part = doc.getObject(name)
part.Label = name
doc.recompute()

#5. Create Body
if corpusEnabled == QtWidgets.QMessageBox.StandardButton.Yes:
  createCorpus(doc, name)

#6. Link Part
currentDoc.addObject('App::Link', name).setLink(part)
currentDoc.recompute(None,True,True)
