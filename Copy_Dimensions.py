import FreeCAD
import FreeCADGui
from PySide2 import QtWidgets

selection = FreeCADGui.Selection.getSelection()
source_object = selection[0].LinkedObject
source_doc = source_object.Document
others = selection[1:]

# source_pad =
# source_sketch = 
copy_string, ok = QtWidgets.QInputDialog.getText(QtWidgets.QApplication.activeWindow(), "Sync Dimensions",
                                     f"L={source_object.Laenge}; B={source_object.Breite}; D={source_object.Staerke};", QtWidgets.QLineEdit.Normal,
                                     "LL BB DD")

def getExpression(o, expression_name):
  if o.ExpressionEngine is None:
    return None
  
  for name, value in o.ExpressionEngine:
    if name == expression_name:
      return value
  
  return None

def extract_property(doc, copy_property):
  match copy_property:
    case 'L':
      return (doc.getObject('Sketch'), '.Constraints.Laenge', 'Laenge')
    case 'B':
      return (doc.getObject('Sketch'), '.Constraints.Breite', 'Breite')
    case 'D':
      return (doc.getObject('Pad'), 'Length', 'Staerke')

def get_source_value(copy_part):
  expression_and_property = extract_property(source_doc, copy_part[0])
  
  expression = getExpression(expression_and_property[0], expression_and_property[1])

  if expression is None:
    return ('static', source_object[expression_and_property[2]])
  else:
    return ('expression', expression)


def sync(doc, parts):
  for copy_part in parts:
    source_value = get_source_value(copy_part)
    target_property = extract_property(doc, copy_part[1])
    
    if source_value[0] == 'expression':
      target_property[0].setExpression(target_property[1], source_value[1])
    else:
      raise ValueError(f'{source_value[0]} not supported yet')

if copy_string and ok:
  parts = copy_string.split(" ")

  for o in others:
    object_doc = o.LinkedObject.Document
    sync(object_doc, parts)


