import FreeCAD
import FreeCADGui

def isLink(o):
  return o.TypeId == 'App::Link'

def getRoot(o):
  root = o
  
  while isLink(root):
   root = root.LinkedObject
  
  return root

selection = FreeCADGui.Selection.getSelection()
source_object = getRoot(selection[0])
source_view_object = source_object.ViewObject
others = selection[1:]

for o in others:
  object = getRoot(o)

  if object == source_object:
    continue

  view_object = object.ViewObject
  
  object.Typ = source_object.Typ
  object.Url = source_object.Url
  object.Abrechnung_Art = source_object.Abrechnung_Art
  object.Einzelpreis = source_object.Einzelpreis

  view_object.ShapeColor = source_view_object.ShapeColor
  view_object.Transparency = source_view_object.Transparency
