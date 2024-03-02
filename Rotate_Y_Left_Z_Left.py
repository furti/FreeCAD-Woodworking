import FreeCAD
import FreeCADGui
import math


for o in FreeCADGui.Selection.getSelection():
  o.Placement.Rotation.Axis = FreeCAD.Vector(-0.577, 0.577, -0.577)
  o.Placement.Rotation.Angle = math.radians(240)

  o.setExpression('.Placement.Base.x', u'Breite')
  o.setExpression('.Placement.Base.y', u'Staerke')
  