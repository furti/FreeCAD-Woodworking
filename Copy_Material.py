import FreeCAD
import FreeCADGui

selection = FreeCADGui.Selection.getSelection()
source_object = selection[0].LinkedObject
source_view_object = source_object.ViewObject
others = selection[1:]



for o in others:
  object = o.LinkedObject
  view_object = object.ViewObject
  
  object.Typ = source_object.Typ
  object.Url = source_object.Url

  view_object.ShapeColor = source_view_object.ShapeColor
  view_object.Transparency = source_view_object.Transparency
