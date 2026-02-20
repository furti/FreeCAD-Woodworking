import FreeCAD
import math

# objectSize = 20
# textSize = 58
# pageHeight = 297
cellWidth = 90
cellHeight = 87
border = 10
overviewConfig = {"dir": (FreeCAD.Vector(
    0.577, -0.577, 0.577), FreeCAD.Vector(0.707, 0.707, 0))}
body_numbers = []

def isLink(o):
    return o.TypeId == "App::Link"


def isBody(o):
    return o.TypeId == "PartDesign::Body"


def getRoot(o):
    root = o

    while isLink(root):
        root = root.LinkedObject

    return root

def getBodies(part):
    bodies = []

    for o in part.Group:
        root = getRoot(o)

        if not isBody(root):
            continue
        
        body_number = root.Planname

        if not body_number in body_numbers:
            bodies.append(root)
            body_numbers.append(body_number)

    return bodies

def getDimensions(body):
    bb = body.Shape.BoundBox

    return (bb.XLength, bb.YLength, bb.ZLength)


def calculateScale(dimensions):
    diagonalX = math.sqrt(pow(dimensions[0], 2) + pow(dimensions[1], 2))
    diagonalY = diagonalX + dimensions[2]
    xScale = cellWidth / diagonalX
    yScale = cellHeight / diagonalY

    return min(xScale, yScale)


def getViewData(viewName):
    if viewName == "Top":
        return (topConfig.copy(), "Oben")
    elif viewName == "Right":
        return (rightConfig.copy(), "Rechts")
    elif viewName == "Left":
        return (leftConfig.copy(), "Links")
    elif viewName == "Front":
        return (frontConfig.copy(), "Vorne")
    elif viewName == "Bottom":
        return (bottomConfig.copy(), "Unten")
    elif viewName == "Back":
        return (backConfig.copy(), "Hinten")

    raise ValueError("View " + viewName + " does not exist")


def nextCell(cell):
    newCell = list(cell)

    if newCell[1] == 1:
        newCell[0] += 1
        newCell[1] = 0
    else:
        newCell[1] += 1

    return tuple(newCell)


class CutPage:
    def __init__(self, doc, page_name):
        self.doc = doc

        template = self.doc.addObject(
            'TechDraw::DrawSVGTemplate', page_name + '_ZuschnittTemplate')
        template.Template = FreeCAD.getHomePath(
        ) + "/share/Mod/TechDraw/Templates/A4_Portrait_blank.svg"

        self.page = self.doc.addObject('TechDraw::DrawPage', page_name)
        self.page.Template = template
        self.cell = [0, 0]
    
    def is_full(self):
        return self.cell[0] >= 3

    def addBody(self, body):
        dimensions = getDimensions(body)
        scale = calculateScale(dimensions)

        view = self.createView(
            body, overviewConfig["dir"], scale)
        view.Label = body.Name
        cellDimensions = self.cellDimensions()
        self.incrementCell()
        self.alignView(view, cellDimensions)
        self.printData(body, (view.X.Value, view.Y.Value))

    def createView(self, body, direction, scale, perspective = False):
        view = self.doc.addObject('TechDraw::DrawViewPart',
                             body.Name + '_Overview')
        self.page.addView(view)

        view.XSource = body
        view.Direction = direction[0]
        view.XDirection = direction[1]

        view.ScaleType = u"Custom"
        view.Scale = scale
        view.CoarseView = False
        view.Perspective = perspective

        view.ViewObject.LineWidth = '0.2 mm'

        view.recompute()

        return view

    def alignView(self, view, cellDimensions):
        view.X = '{} mm'.format(cellDimensions[0])
        view.Y = '{} mm'.format(cellDimensions[1] - cellHeight / 2)

        view.recompute()

    def printData(self, body, cellDimensions):
        base_name = body.Name
        count = body.Anzahl
        name = body.Planname

        text = [f'{name} x {count}']

        if hasattr(body, 'Laenge') and hasattr(body, 'Breite') and hasattr(body, 'Staerke'):
            text.append(f'{body.Laenge}x{body.Breite}x{body.Staerke}')

        annotation = self.doc.addObject(
            'TechDraw::DrawViewAnnotation', base_name + '_CountAndName')
        self.page.addView(annotation)

        annotation.TextSize = '5 mm'
        annotation.MaxWidth = 85
        annotation.X = '{} mm'.format(cellDimensions[0])
        annotation.Y = '{} mm'.format(cellDimensions[1] - 20)
        annotation.Text = text
        annotation.TextStyle = "Bold"

        self.doc.recompute()
    
    # (x, y)
    # x = Midpoint of the cell
    # y = top of the cell
    def cellDimensions(self):
        row = self.cell[0]
        column = self.cell[1]
        # 1. We want to have a offset from the edges of the page
        # 2. So the midpoint of the cell is the offset + the half cell width
        x = border + column * cellWidth + cellWidth / 2
        y = 297 - (border + row * cellHeight)

        # 3. We add an additional border between cells for every cell > 0
        if column > 0:
            x += border

        if row > 0:
            y += border

        return (x, y)
    
    def incrementCell(self):
        c = self.cell
        
        c[1] += 1

        if c[1] > 1:
            c[0] += 1
            c[1] = 0

def ensure_group(doc):
    group_name = 'Plan_Zeichnungen'
    groups = doc.findObjects('App::DocumentObjectGroup')

    for group in groups:
        if group.Name == group_name:
            return group
    
    return doc.addObject('App::DocumentObjectGroup', group_name)

def ensure_page(doc, index, group):
    page_name = 'Schnittplan_Einfach_' + str(index)

    if doc.getObject(page_name) is not None:
        print('Schnittplan already exists')
        return None
    
    page = CutPage(doc, page_name)
    group.addObject(page.page)

    return page

# Start of script
doc = FreeCAD.ActiveDocument
parts = doc.findObjects('App::Part')
group = ensure_group(doc)
page_number = 0
page = ensure_page(doc, page_number, group)

if page:
    for part in parts:
        bodies = getBodies(part)
    
        for body in bodies:
            if page.is_full():
                page_number += 1
                page = ensure_page(doc, page_number, group)

            page.addBody(body)
            page.page.KeepUpdated = True
            
