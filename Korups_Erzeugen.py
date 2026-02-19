import FreeCAD
import FreeCADGui
import os
from pathlib import Path
from PySide2 import QtWidgets
from Platte_Erzeugen import create_board

def createCorpus(doc, name):
  # 2. Create the bottom board
  bottomName = name + '_Boden'
  bottom = create_board(bottomName, doc)
  bottom.setExpression('.Placement.Base.x', u'Staerke')

  # 2. Create the left board
  leftName = name + '_Seitenwand_Links'
  left = create_board(leftName, doc)
  left.setExpression('.Placement.Base.y', u'Breite')
  left.Placement.Rotation = FreeCAD.Rotation(FreeCAD.Vector(0.707, 0.000, 0.707), 180.000)

  # 2. Create the right board
  rightName = name + '_Seitenwand_Rechts'
  right = create_board(rightName, doc)
  right.setExpression('.Placement.Base.x', u'Staerke * 2 + ' + bottomName + '.Laenge')
  right.Placement.Rotation = FreeCAD.Rotation(FreeCAD.Vector(0., 1.000, 0), 270.000)

  # 2. Create the top board
  topName = name + '_Deckel'
  top = create_board(topName, doc)
  top.setExpression('.Placement.Base.x', u'Staerke')
  top.setExpression('.Placement.Base.z', leftName + '.Laenge - Staerke')

  return None

if __name__ == '__main__':
  currentDoc = FreeCAD.ActiveDocument
  name, ok = QtWidgets.QInputDialog.getText(QtWidgets.QApplication.activeWindow(), 'Name', 'Name')

  if ok and name:
    createCorpus(currentDoc, name)
