import FreeCAD
import FreeCADGui


o = FreeCADGui.Selection.getSelection()[0]

if not hasattr(o, "Breite"):
    o.addProperty("App::PropertyLength", "Breite", "Info", "Breite").Breite=1.0
    o.setExpression('Breite', u'Sketch.Constraints.Breite')

if not hasattr(o, "Laenge"):
    o.addProperty("App::PropertyLength", "Laenge", "Info", "Laenge").Laenge=1.0
    o.setExpression('Laenge', u'Sketch.Constraints.Laenge')

if not hasattr(o, "Staerke"):
    o.addProperty("App::PropertyLength", "Staerke", "Info", "Staerke").Staerke=1.0
    o.setExpression('Staerke', u'Pad.Length')

if not hasattr(o, "Schnittliste_Ansichten"):
    o.addProperty("App::PropertyStringList", "Schnittliste_Ansichten", "Drawing", "Schnittliste_Ansichten")