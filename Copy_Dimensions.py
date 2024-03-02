import FreeCAD
import FreeCADGui

selection = FreeCADGui.Selection.getSelection()
first_doc = selection[0].LinkedObject.Document
others = selection[1:]

def getExpression(o, expression_name):
  if o.ExpressionEngine is None:
    return None
  
  for name, value in o.ExpressionEngine:
    if name == expression_name:
      return value
  
  return None

def syncProperty(source, target, property_name):
  expression = getExpression(source, property_name)

  if expression is None:
    target[property_name] = source[property_name]
  else:
    target.setExpression(property_name, expression)

def syncPad(doc):
  source_pad = first_doc.getObject('Pad')
  target_pad = doc.getObject('Pad')

  syncProperty(source_pad, target_pad, 'Length')

def syncSketch(doc):
  source_sketch = first_doc.getObject('Sketch')
  target_sketch = doc.getObject('Sketch')

  syncProperty(source_sketch, target_sketch, '.Constraints.Laenge')
  syncProperty(source_sketch, target_sketch, '.Constraints.Breite')

for o in others:
  object_doc = o.LinkedObject.Document
  syncPad(object_doc)
  syncSketch(object_doc)
