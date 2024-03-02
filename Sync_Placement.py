import FreeCAD
import FreeCADGui
from PySide2 import QtWidgets

selection = FreeCADGui.Selection.getSelection()
source_object = selection[0]
others = selection[1:]

# source_pad =
# source_sketch = 
copy_string, ok = QtWidgets.QInputDialog.getText(QtWidgets.QApplication.activeWindow(), "Sync Placement",
                                     f"R=Rotation; X; Y; Z;", QtWidgets.QLineEdit.Normal,
                                     "R XX YY ZZ")

def syncExpression(source, target, source_expression, target_expression):
  target.setExpression('.' + target_expression, source.Name + '.' + source_expression)

def extract_expression(copy_property):
  match copy_property:
    case 'X':
      return 'Placement.Base.x'
    case 'Y':
      return 'Placement.Base.y'
    case 'Z':
      return 'Placement.Base.z'

def sync(target, parts):
  for copy_part in parts:
    if copy_part == 'R':
      syncExpression(source_object, target, 'Placement.Rotation.Angle', 'Placement.Rotation.Angle')
      syncExpression(source_object, target, 'Placement.Rotation.Axis.x', 'Placement.Rotation.Axis.x')
      syncExpression(source_object, target, 'Placement.Rotation.Axis.y', 'Placement.Rotation.Axis.y')
      syncExpression(source_object, target, 'Placement.Rotation.Axis.z', 'Placement.Rotation.Axis.z')
    else:
      source_expression = extract_expression(copy_part[0])
      target_expression = extract_expression(copy_part[1])
      syncExpression(source_object, target, source_expression, target_expression)

if copy_string and ok:
  parts = copy_string.split(" ")

  for o in others:
    sync(o, parts)

