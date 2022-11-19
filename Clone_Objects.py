import FreeCAD
import FreeCADGui
import Draft

for o in FreeCADGui.Selection.getSelection():
    c = Draft.make_clone(o)
    c.Label += "_Clone"

    c.setExpression('.Placement.Base.x', o.Name + '.Placement.Base.x')
    c.setExpression('.Placement.Base.y', o.Name + '.Placement.Base.y')
    c.setExpression('.Placement.Base.z', o.Name + '.Placement.Base.z')

FreeCAD.ActiveDocument.recompute()