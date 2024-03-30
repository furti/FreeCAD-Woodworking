import FreeCAD
import FreeCADGui
import PartDesign
import PartDesignGui
import Sketcher
import Part
from PySide2 import QtWidgets
import os

def create_board(documentLocation, name, currentDoc):
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

  # 4. Create Object
  doc.addObject('PartDesign::Body', name)
  body = doc.getObject(name)
  body.newObject('Sketcher::SketchObject', 'Sketch')
  sketch = doc.getObject('Sketch')
  sketch.Support = (doc.getObject('XY_Plane'),[''])
  sketch.MapMode = 'FlatFace'
  doc.recompute()

  # 5. Customize Sketch
  guidoc.setEdit(body,0,'Sketch.')

  geoList = []
  geoList.append(Part.LineSegment(FreeCAD.Vector(0,0,0), FreeCAD.Vector(1000,0,0)))
  geoList.append(Part.LineSegment(FreeCAD.Vector(1000,0,0),FreeCAD.Vector(1000,1000,0)))
  geoList.append(Part.LineSegment(FreeCAD.Vector(1000,1000,0),FreeCAD.Vector(0,1000,0)))
  geoList.append(Part.LineSegment(FreeCAD.Vector(0,1000,0),FreeCAD.Vector(0,0,0)))
  sketch.addGeometry(geoList,False)

  conList = []
  conList.append(Sketcher.Constraint('Coincident',0,2,1,1))
  conList.append(Sketcher.Constraint('Coincident',1,2,2,1))
  conList.append(Sketcher.Constraint('Coincident',2,2,3,1))
  conList.append(Sketcher.Constraint('Coincident',3,2,0,1))
  conList.append(Sketcher.Constraint('Horizontal',0))
  conList.append(Sketcher.Constraint('Horizontal',2))
  conList.append(Sketcher.Constraint('Vertical',1))
  conList.append(Sketcher.Constraint('Vertical',3))
  sketch.addConstraint(conList)

  sketch.addConstraint(Sketcher.Constraint('Coincident',0,1,-1,1)) 
  sketch.addConstraint(Sketcher.Constraint('DistanceX',0,1,0,2,56.837105)) 
  sketch.setDatum(9,FreeCAD.Units.Quantity('1000 mm'))
  sketch.renameConstraint(9, u'Laenge')
  sketch.addConstraint(Sketcher.Constraint('DistanceY',1,1,1,2,42.152203)) 
  sketch.setDatum(10,FreeCAD.Units.Quantity('1000 mm'))
  sketch.renameConstraint(10, u'Breite')
  guidoc.resetEdit()
  doc.recompute()

  # 6. Pad sketch
  body.newObject('PartDesign::Pad', 'Pad')
  pad = doc.getObject('Pad')
  pad.Profile = sketch
  pad.Length = 10.0

  # Set general properties
  body.addProperty("App::PropertyString", "Typ", "Info", "Typ")
  body.addProperty("App::PropertyString", "Url", "Info", "Url")
  body.addProperty("App::PropertyLength", "Breite", "Info", "Breite")
  body.addProperty("App::PropertyLength", "Laenge", "Info", "Laenge")
  body.addProperty("App::PropertyLength", "Staerke", "Info", "Staerke")

  body.setExpression('Breite', u'Sketch.Constraints.Breite')
  body.setExpression('Laenge', u'Sketch.Constraints.Laenge')
  body.setExpression('Staerke', u'Pad.Length')

  # Set drawing properties
  body.addProperty("App::PropertyStringList", "Schnittliste_Ansichten", "Drawing", "Schnittliste_Ansichten")

  body.ViewObject.DisplayModeBody = 'Tip'

  doc.recompute()
  sketch.Visibility = False
  doc.recompute()

  # Link into the parent doc
  currentDoc.addObject('App::Link', name).setLink(body)
  currentDoc.recompute(None,True,True)

  return currentDoc.getObject(name)

if __name__ == '__main__':
  currentDoc = FreeCAD.ActiveDocument
  # 1. Document Location
  documentLocation = QtWidgets.QFileDialog.getSaveFileName(QtWidgets.QApplication.activeWindow(), 'Save as', '', 'Image Files (*.FCStd)')[0]
  name = os.path.splitext(os.path.basename(documentLocation))[0]

  create_board(documentLocation, name, currentDoc)