import FreeCAD
import FreeCADGui
import math


for o in FreeCADGui.Selection.getSelection():
  o.Placement.Rotation.Axis = FreeCAD.Vector(0.577, 0.577, 0.577)
  o.Placement.Rotation.Angle = math.radians(120)
  