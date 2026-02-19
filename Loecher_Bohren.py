import FreeCAD
import FreeCADGui
import Part
import PartDesign
import PartDesignGui
import Sketcher


def getPlane(direction):
  if direction == 0 or direction == 2:
    return document.getObject('XZ_Plane')
  if direction == 1 or direction == 3:
    return document.getObject('YZ_Plane')
  
  return document.getObject('XY_Plane')

def helperLineLengh(direction):
  baseExpression = None

  if direction == 0 or direction == 2:
    baseExpression = 'Sketch.Constraints.Laenge'
  else:
    baseExpression = 'Sketch.Constraints.Breite'
  
  return baseExpression + " - 40 mm"

def configurePocketAndSketch(pocket, sketch, direction):
  if direction == 0:
    pocket.Reversed = True
    sketch.setExpression('.AttachmentOffset.Base.z', u'-Sketch.Constraints.Breite')
  
  if direction == 1:
    sketch.setExpression('.AttachmentOffset.Base.z', u'Sketch.Constraints.Laenge')
  
  if direction == 3:
    pocket.Reversed = True
  
  if direction == 4:
    sketch.setExpression('.AttachmentOffset.Base.z', u'Pad.Length')
  
  if direction == 5:
    pocket.Reversed = True

def configureConstraints(sketch, direction):
  constraints = []
  # Circles
  constraints.append(Sketcher.Constraint('Diameter', 0, 6))
  constraints.append(Sketcher.Constraint('Diameter', 1, 6))
  # Helper Line
  if direction in [4, 5]:
    constraints.append(Sketcher.Constraint('Vertical', 2))
  else:
    constraints.append(Sketcher.Constraint('Horizontal', 2))
  constraints.append(Sketcher.Constraint('DistanceY', -1, 1, 2, 1, 20))
  constraints.append(Sketcher.Constraint('DistanceX', -1, 1, 2, 1, 20))
  if direction in [4, 5]:
    constraints.append(Sketcher.Constraint('DistanceY', 2, 1, 2, 2, 1000))
  else:
    constraints.append(Sketcher.Constraint('DistanceX', 2, 1, 2, 2, 1000))
  # Attach circles to helper line
  constraints.append(Sketcher.Constraint('Coincident', 0, 3, 2, 1))
  constraints.append(Sketcher.Constraint('Coincident', 1, 3, 2, 2))
  sketch.addConstraint(constraints)

def configureExpressions(sketch, direction):
  sketch.setExpression('Constraints[5]', helperLineLengh(direction)) # Lengh of helper line

  if direction in [4, 5]:
    sketch.setExpression('Constraints[4]', u'Pad.Length / 2') # Move helper line up half the thickness
  else:
    sketch.setExpression('Constraints[3]', u'Pad.Length / 2') # Move helper line up half the thickness


# 1. Setup stuff
document = FreeCAD.ActiveDocument
guidoc = FreeCADGui.ActiveDocument
selectedFace = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
normal = selectedFace.normalAt(0.5, 0.5)


# 0 -> North, 1 -> East, 2 -> South, 3 -> West, 4 -> Top, 5 -> Bottom
direction = 0

if normal.x == 1:
  direction = 1
elif normal.x == -1:
  direction = 3
elif normal.y == -1:
  direction = 2
elif normal.z == 1:
  direction = 4
elif normal.z == -1:
  direction = 5

print(direction)

#1. Create Object
body = document.findObjects(Type='PartDesign::Body')[0]
tip = body.Tip
body.newObject('Sketcher::SketchObject', 'Loecher_Sketch')
sketch = document.ActiveObject

sketch.AttachmentSupport = (getPlane(direction),[''])
sketch.MapMode = 'FlatFace'
document.recompute()

# 2. Customize Sketch
# guidoc.setEdit(body, 0, sketch.Name)

geoList = []
geoList.append(Part.Circle())
geoList.append(Part.Circle())
geoList.append(Part.LineSegment(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(1000, 0, 0)))
sketch.addGeometry(geoList,False)

# Make helper line a construction line
sketch.toggleConstruction(2) 

configureConstraints(sketch, direction)
configureExpressions(sketch, direction)

document.recompute()

# 3. Create Pocket
body.newObject('PartDesign::Pocket','Loecher')
pocket = document.ActiveObject
pocket.Profile = sketch
pocket.Length = 10
sketch.Visibility = False
tip.Visibility = False

configurePocketAndSketch(pocket, sketch, direction)

document.recompute()