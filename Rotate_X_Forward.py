import FreeCAD
import FreeCADGui
import math


for o in FreeCADGui.Selection.getSelection():
  o.Placement.Rotation.Axis = FreeCAD.Vector(1, 0, 0)
  o.Placement.Rotation.Angle = math.radians(90)

  o.setExpression('.Placement.Base.y', u'Staerke')