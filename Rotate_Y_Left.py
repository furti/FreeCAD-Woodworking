import FreeCAD
import FreeCADGui
import math


for o in FreeCADGui.Selection.getSelection():
  o.Placement.Rotation.Axis = FreeCAD.Vector(0, 1, 0)
  o.Placement.Rotation.Angle = math.radians(270)
  
  o.setExpression('.Placement.Base.x', u'Staerke')