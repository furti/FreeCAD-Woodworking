import FreeCAD
import FreeCADGui
import os
from pathlib import Path
from PySide2 import QtWidgets
from Platte_Erzeugen import create_board

def createBody(doc, part, name):
  #1. Create the folder that holds all boards
  documentLocation = doc.FileName
  boardFolder = Path(os.path.join(os.path.dirname(documentLocation), 'Teile', name))

  if not boardFolder.is_dir():
    boardFolder.mkdir(parents=True)
  
  # 2. Create the bottom board
  bottomName = name + '_Boden'
  bottomLocation = boardFolder.joinpath(bottomName + '.FCStd')
  bottom = create_board(str(bottomLocation), bottomName, doc)
  bottom.setExpression('.Placement.Base.x', u'Staerke')

  # 2. Create the left board
  leftName = name + '_Seitenwand_Links'
  leftLocation = boardFolder.joinpath(leftName + '.FCStd')
  left = create_board(str(leftLocation), leftName, doc)
  left.setExpression('.Placement.Base.y', u'Breite')
  left.Placement.Rotation = FreeCAD.Rotation(FreeCAD.Vector(0.707, 0.000, 0.707), 180.000)

  # 2. Create the right board
  rightName = name + '_Seitenwand_Rechts'
  rightLocation = boardFolder.joinpath(rightName + '.FCStd')
  right = create_board(str(rightLocation), rightName, doc)
  right.setExpression('.Placement.Base.x', u'Staerke * 2 + ' + bottomName + '.Laenge')
  right.Placement.Rotation = FreeCAD.Rotation(FreeCAD.Vector(0., 1.000, 0), 270.000)

  # 2. Create the top board
  topName = name + '_Deckel'
  topLocation = boardFolder.joinpath(topName + '.FCStd')
  top = create_board(str(topLocation), topName, doc)
  top.setExpression('.Placement.Base.x', u'Staerke')
  top.setExpression('.Placement.Base.z', leftName + '.Laenge - Staerke')

  return None

currentDoc = FreeCAD.ActiveDocument

# 1. Document Location
documentLocation = QtWidgets.QFileDialog.getSaveFileName(QtWidgets.QApplication.activeWindow(), 'Save as', '', 'Freecad Files (*.FCStd)')[0]
name = os.path.splitext(os.path.basename(documentLocation))[0]

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
createBody(doc, part, name)

#6. Link Part
currentDoc.addObject('App::Link', name).setLink(part)
currentDoc.recompute(None,True,True)
