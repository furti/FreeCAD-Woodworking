import FreeCAD
import FreeCADGui

def isLink(o):
  return o.TypeId == 'App::Link'

def getRoot(o):
  root = o
  
  while isLink(root):
   root = root.LinkedObject
  
  return root

def copy_property(target, source,  property_name):
  if property_name in dir(source):
    setattr(target, property_name, getattr(source, property_name))

selection = FreeCADGui.Selection.getSelection()
source_object = getRoot(selection[0])
source_view_object = source_object.ViewObject
others = selection[1:]

for o in others:
  object = getRoot(o)

  if object == source_object:
    continue

  view_object = object.ViewObject
  
  copy_property(object, source_object, 'Typ')
  copy_property(object, source_object, 'Url')
  copy_property(object, source_object, 'Abrechnung_Art')
  copy_property(object, source_object, 'Einzelpreis')

  view_object.ShapeAppearance = source_view_object.ShapeAppearance
