import FreeCAD
import math

doc = FreeCAD.ActiveDocument
# objectSize = 20
# textSize = 58
# pageHeight = 297
cellWidth = 90
cellHeight = 87
border = 10
overviewConfig = {"dir": (FreeCAD.Vector(
    0.577, -0.577, 0.577), FreeCAD.Vector(0.707, 0.707, 0)), "cell": (0, 0)}
topConfig = {"dir": (FreeCAD.Vector(0, 0, 1),
                     FreeCAD.Vector(1, 0, 0)), "cell": None}
bottomConfig = {"dir": (FreeCAD.Vector(0, 0, -1),
                        FreeCAD.Vector(1, 0, 0)), "cell": None}
rightConfig = {"dir": (FreeCAD.Vector(
    1, 0, 0), FreeCAD.Vector(0, 1, 0)), "cell": None}
leftConfig = {"dir": (FreeCAD.Vector(-1, 0, 0),
                      FreeCAD.Vector(0, -1, 0)), "cell": None}
frontConfig = {"dir": (FreeCAD.Vector(0, -1, 0),
                       FreeCAD.Vector(1, 0, 0)), "cell": None}
viewOrder = ["Top", "Right", "Left", "Front", "Back", "Bottom"]


def getDimensions(body):
    bb = body.Shape.BoundBox

    return (bb.XLength, bb.YLength, bb.ZLength)


def calculateScale(dimensions, viewName):
    xScale = None
    yScale = None

    if viewName in ["Top", "Bottom"]:
        xScale = cellWidth / dimensions[0]
        yScale = cellHeight / dimensions[1]
    elif viewName in ["Front", "Back"]:
        xScale = cellWidth / dimensions[0]
        yScale = cellHeight / dimensions[2]
    elif viewName in ["Right", "Left"]:
        xScale = cellWidth / dimensions[1]
        yScale = cellHeight / dimensions[2]
    else:
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

    raise "View " + viewName + " does not exist"


def nextCell(cell):
    newCell = list(cell)

    if newCell[1] == 1:
        newCell[0] += 1
        newCell[1] = 0
    else:
        newCell[1] += 1

    return tuple(newCell)


class CutPage:
    def __init__(self, body):
        template = doc.addObject(
            'TechDraw::DrawSVGTemplate', body.Name + '_ZuschnittTemplate')
        template.Template = FreeCAD.getHomePath(
        ) + "/data/Mod/TechDraw/Templates/A4_Portrait_blank.svg"

        self.page = doc.addObject('TechDraw::DrawPage', body.Name+'_Zuschnitt')
        self.page.Template = template
        self.body = body
        self.basename = body.Name
        self.dimensions = getDimensions(body)

    def addOverview(self):
        scale = calculateScale(self.dimensions, "Overview")

        view = self.createView(
            self.body, overviewConfig["dir"], scale)
        view.Label = 'Übersicht'
        cellDimensions = self.cellDimensions(overviewConfig["cell"])
        self.alignView(view, cellDimensions)
        self.printCountAndName(
            self.body.Anzahl, self.body.Planname, (view.X.Value, view.Y.Value))

    def addViews(self, viewNames):
        sortedViews = viewNames.copy()
        sortedViews.sort(key=lambda v: viewOrder.index(v))

        cell = (0, 0)

        for viewName in sortedViews:
            config, label = getViewData(viewName)
            cell = nextCell(cell)
            scale = calculateScale(self.dimensions, viewName)

            view = self.createView(
                self.body, config["dir"], scale)
            view.Label = label
            view.ViewObject.KeepLabel = True
            cellDimensions = self.cellDimensions(cell)
            self.alignView(view, cellDimensions)

    def createView(self, body, direction, scale, perspective = False):
        view = doc.addObject('TechDraw::DrawViewPart',
                             self.basename + '_Overview')
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

    def printCountAndName(self, count, name, cellDimensions):
        text = [name, 'x {}'.format(count)]
        print(cellDimensions)

        annotation = doc.addObject(
            'TechDraw::DrawViewAnnotation', self.basename + '_CountAndName')
        self.page.addView(annotation)

        annotation.TextSize = '5 mm'
        annotation.MaxWidth = '20 mm'
        annotation.X = '{} mm'.format(cellDimensions[0] + 40)
        annotation.Y = '{} mm'.format(cellDimensions[1] + 15)
        annotation.Text = text
        annotation.TextStyle = "Bold"

        doc.recompute()

    # (x, y)
    # x = Midpoint of the cell
    # y = top of the cell
    def cellDimensions(self, cellData):
        row = cellData[0]
        column = cellData[1]
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


# Start of script
body = doc.findObjects('PartDesign::Body')[0]
page = CutPage(body)
page.addOverview()
page.addViews(body.Schnittliste_Ansichten)
page.page.KeepUpdated = False
