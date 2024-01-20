import FreeCAD

doc = FreeCAD.ActiveDocument
objectSize = 20
textSize = 58
pageHeight = 297
cellSize = 60

def isLink(o):
  return o.TypeId == 'App::Link'

def isBody(o):
  return o.TypeId == 'PartDesign::Body'

def getRoot(o):
  root = o
  
  while isLink(root):
   root = root.LinkedObject
  
  return root

def getBodies(part):
  bodies = {}
  
  for o in part.Group:
    root = getRoot(o)
    
    if not isBody(root):
      continue

    name = root.Planname

    if not name in bodies:
      bodies[name] = {"name": name, "body": root}
    
  return dict(sorted(bodies.items()))

def getDimensions(body):
  bb = body.Shape.BoundBox
  
  return (round(bb.XLength, 1), round(bb.YLength, 1), round(bb.ZLength, 1))

def calculateScale(dimensions):
  biggestLength = max(dimensions)
  
  return objectSize / biggestLength

class BomPage:
  def __init__(self, name):
    template = doc.addObject('TechDraw::DrawSVGTemplate', 'BOMTemplate_' + name)
    template.Template = FreeCAD.getHomePath(
        ) + "/data/Mod/TechDraw/Templates/A4_Portrait_blank.svg"
    self.page = doc.addObject('TechDraw::DrawPage', 'BOM_' + name)
    self.page.Template = template
    self.column = 0
    self.row = 0
  
  def addView(self, bodyData):
    body = bodyData['body']
    name = bodyData['name']

    dimensions = getDimensions(body)
    view = self.createView(body, dimensions)
    cellDimensions = self.nextCellDimensions()
    self.alignView(view, cellDimensions)
    self.printInfo(body, cellDimensions, dimensions)
    self.printCountAndName(body, name, cellDimensions)
  
  def createView(self, body, dimensions):
    view = doc.addObject('TechDraw::DrawViewPart', body.Label + '_View')
    self.page.addView(view)
    
    view.XSource = body
    view.Direction = FreeCAD.Vector(0.577,-0.577,0.577)
    view.XDirection = FreeCAD.Vector(1,0,0)
  
    view.ScaleType = u"Custom"
    view.Scale = calculateScale(dimensions)
    view.CoarseView = True
    view.Perspective = True
    
    view.ViewObject.LineWidth = '0.2 mm'
    
    view.recompute()

    return view
  
  def alignView(self, view, cellDimensions):
    view.X = '{} mm'.format(cellDimensions[0] - objectSize)
    view.Y = '{} mm'.format(cellDimensions[1] - objectSize / 2)
    
    view.recompute()
  
  def printInfo(self, body, cellDimensions, dimensions):
    text = []
    
    if hasattr(body, 'Typ'):
      text.append(body.Typ)
    
    text.append('{} mm x {} mm x {} mm'.format(dimensions[0], dimensions[1], dimensions[2]))

    if hasattr(body, 'Url'):
      text.append(body.Url)

    annotation = doc.addObject('TechDraw::DrawViewAnnotation', body.Label + '_Text')
    self.page.addView(annotation)

    annotation.TextSize = '3 mm'
    annotation.MaxWidth = 58
    annotation.X = '{} mm'.format(cellDimensions[0])
    annotation.Y = '{} mm'.format(cellDimensions[1] - objectSize - 10)
    annotation.Text = text
    
    doc.recompute()

  def printCountAndName(self, body, name, cellDimensions):
    text = ['x {}'.format(body.Anzahl)]
    
    nameAnnotation = doc.addObject('TechDraw::DrawViewAnnotation', body.Label + '_Name')
    self.page.addView(nameAnnotation)

    nameAnnotation.TextSize = '5 mm'
    nameAnnotation.MaxWidth = 20
    nameAnnotation.X = '{} mm'.format(cellDimensions[0] + 20)
    nameAnnotation.Y = '{} mm'.format(cellDimensions[1] - objectSize / 2)
    nameAnnotation.Text = name
    nameAnnotation.TextStyle = "Bold"

    countAnnotation = doc.addObject('TechDraw::DrawViewAnnotation', body.Label + '_Count')
    self.page.addView(countAnnotation)

    countAnnotation.TextSize = '5 mm'
    countAnnotation.MaxWidth = 20
    countAnnotation.X = '{} mm'.format(cellDimensions[0] + 20)
    countAnnotation.Y = '{} mm'.format(cellDimensions[1] - objectSize / 2 - 5)
    countAnnotation.Text = text
    
    doc.recompute()
  
  # (x, y)
  # x = Midpoint of the cell
  # y = top of the cell
  def nextCellDimensions(self):
    # 1. We want to have a 15mm offset from the edges of the page
    # 2. Each cell is 60 mm wide
    # 3. So the midpoint of the cell is the offset + the half cell width
    x = 15 + self.column * cellSize + cellSize / 2
    y = 297 - (15 + self.row * 60)
    
    self.nextColumnAndRow()
    
    return (x, y)

  def nextColumnAndRow(self):
    self.column += 1
    
    if self.column >= 3:
      self.column = 0
      self.row += 1

# Start of script
parts = FreeCAD.ActiveDocument.findObjects('App::Part')
for part in parts:
  bodies = getBodies(part)

  if len(bodies) == 0:
    continue
  
  #sheet = FreeCAD.ActiveDocument.addObject('Spreadsheet::Sheet', 'Materialliste')
  page = BomPage(part.Label)
  
  for bodyData in bodies.values():
    page.addView(bodyData)
  
  page.page.KeepUpdated = False
  #  typ = part.Typ
  #  url = part.Url