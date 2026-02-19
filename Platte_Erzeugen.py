import FreeCAD
import FreeCADGui
import PartDesign
import PartDesignGui
import Sketcher
import Part
from PySide2 import QtWidgets
import os

def ensure_board_group(doc):
  name = 'Platten'
  groups = doc.findObjects('App::DocumentObjectGroup', Label=name)

  if len(groups) >= 1:
    return groups[0]
  
  doc.addObject('App::DocumentObjectGroup', name)
  group = doc.findObjects('App::DocumentObjectGroup', Name=name)[0]
  group.Label = name

  return group

def create_board(name, currentDoc):
  # 1. Create Document and save it
  doc = currentDoc
  guidoc = FreeCADGui.getDocument(doc)

  # 3. Link masse spreadsheet
  #try:
  #  doc.addObject('App::Link', 'Masse').setLink(FreeCAD.getDocument('Masse').Spreadsheet)
  #  doc.recompute(None,True,True)
  #except NameError:
  #  print('Masse Spreadsheet not linked. Document not found')

  # 4. Create Object
  print('Adding body ' + name)
  doc.addObject('PartDesign::Body', name)
  body = doc.getObject(name)

  sketchName = name +'_Sketch'
  body.newObject('Sketcher::SketchObject', sketchName)
  sketch = doc.getObject(sketchName)
  sketch.AttachmentSupport = (doc.getObject('XY_Plane'),[''])
  sketch.MapMode = 'FlatFace'
  doc.recompute()

  # 5. Customize Sketch
  guidoc.setEdit(body,0, sketchName+'.')

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
  padName=name+'_Pad'
  body.newObject('PartDesign::Pad', padName)
  pad = doc.getObject(padName)
  pad.Profile = sketch
  pad.Length = 10.0

  # Set general properties
  body.addProperty("App::PropertyString", "Typ", "Info", "Typ")
  body.addProperty("App::PropertyString", "Url", "Info", "Url")
  body.addProperty("App::PropertyLength", "Breite", "Info", "Breite")
  body.addProperty("App::PropertyLength", "Laenge", "Info", "Laenge")
  body.addProperty("App::PropertyLength", "Staerke", "Info", "Staerke")

  body.setExpression('Breite', sketchName+u'.Constraints.Breite')
  body.setExpression('Laenge', sketchName+u'.Constraints.Laenge')
  body.setExpression('Staerke', padName+u'.Length')

  # Set drawing properties
  body.addProperty("App::PropertyStringList", "Schnittliste_Ansichten", "Drawing", "Schnittliste_Ansichten")

  body.ViewObject.DisplayModeBody = 'Tip'

  doc.recompute()
  sketch.Visibility = False
  doc.recompute()

  group = ensure_board_group(doc)
  group.addObject(body)

  # Link into the parent doc
  link = currentDoc.addObject('App::Link', name)
  link.setLink(body)
  currentDoc.recompute(None,True,True)

  return link

if __name__ == '__main__':
  currentDoc = FreeCAD.ActiveDocument
  name, ok = QtWidgets.QInputDialog.getText(QtWidgets.QApplication.activeWindow(), 'Name', 'Name')

  if ok and name:
    create_board(name, currentDoc)