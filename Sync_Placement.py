import FreeCAD
import FreeCADGui

selection = FreeCADGui.Selection.getSelection()
first = selection[0]
others = selection[1:]

def syncExpression(o, expression):
  print('<<' + first.Label + '>>.' + expression)
  o.setExpression('.' +expression, '<<' + first.Label + '>>.' + expression)

for o in others:
  syncExpression(o, 'Placement.Rotation.Angle')
  syncExpression(o, 'Placement.Rotation.Axis.x')
  syncExpression(o, 'Placement.Rotation.Axis.y')
  syncExpression(o, 'Placement.Rotation.Axis.z')
  syncExpression(o, 'Placement.Base.x')
  syncExpression(o, 'Placement.Base.y')
  syncExpression(o, 'Placement.Base.z')
