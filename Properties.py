import FreeCAD
import FreeCADGui

objects = FreeCADGui.Selection.getSelection()

def isLink(o):
  return o.TypeId == 'App::Link'

def getRoot(o):
  root = o
  
  while isLink(root):
   root = root.LinkedObject
  
  return root

for o in objects:
    root_object = getRoot(o)
    if not hasattr(root_object, "Breite"):
        root_object.addProperty("App::PropertyLength", "Breite", "Info", "Breite").Breite=1.0
        root_object.setExpression('Breite', u'Sketch.Constraints.Breite')

    if not hasattr(root_object, "Laenge"):
        root_object.addProperty("App::PropertyLength", "Laenge", "Info", "Laenge").Laenge=1.0
        root_object.setExpression('Laenge', u'Sketch.Constraints.Laenge')

    if not hasattr(root_object, "Staerke"):
        root_object.addProperty("App::PropertyLength", "Staerke", "Info", "Staerke").Staerke=1.0
        root_object.setExpression('Staerke', u'Pad.Length')

    if not hasattr(root_object, "Schnittliste_Ansichten"):
        root_object.addProperty("App::PropertyStringList", "Schnittliste_Ansichten", "Drawing", "Schnittliste_Ansichten")
    
    if not hasattr(root_object, "Abrechnung_Art"):
        root_object.addProperty("App::PropertyEnumeration", "Abrechnung_Art", "Info", "Abrechnung_Art")
        root_object.Abrechnung_Art = ["lfm", "m2", "m3"]
        root_object.Abrechnung_Art = "m2"
    
    if not hasattr(root_object, "Einzelpreis"):
        root_object.addProperty("App::PropertyFloat", "Einzelpreis", "Info", "Einzelpreis")
    
    if not hasattr(root_object, "Typ"):
        root_object.addProperty("App::PropertyString", "Typ", "Info", "Typ")
    
    if not hasattr(root_object, "Url"):
        root_object.addProperty("App::PropertyString", "Url", "Info", "Url")
