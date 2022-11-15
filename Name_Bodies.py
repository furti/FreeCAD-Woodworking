import FreeCAD

doc = FreeCAD.ActiveDocument
availableChars = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
iterationCount = 1
actualIndex = 0

def calculateNextName():
  global availableChars, iterationCount, actualIndex

  name = availableChars[actualIndex] * iterationCount

  actualIndex += 1

  if actualIndex >= len(availableChars):
    actualIndex = 0
    iterationCount += 1
  
  return name

def isLink(o):
  return o.TypeId == 'App::Link'

def isBody(o):
  return o.TypeId == 'PartDesign::Body'

def getRoot(o):
  root = o
  
  while isLink(root):
   root = root.LinkedObject
  
  return root

def findMatchingBody(body, existingBodies):
  if body in existingBodies:
    return body
  
  bodyShape = body.Shape
  bodyBoundBox = bodyShape.BoundBox

  # We compare certain properties of both the shapes. If they match, we can be pretty sure, that both objects are equal
  for existingBody in existingBodies:
    existingShape = existingBody.Shape

    # Volume
    if round(existingShape.Volume, 3) != round(bodyShape.Volume, 3):
      continue
    
    # Bounding Box -> Length, Thickness, Width
    existingBoundBox = existingShape.BoundBox
    if round(existingBoundBox.XLength, 3) != round(bodyBoundBox.XLength, 3):
      continue
    
    if round(existingBoundBox.YLength, 3) != round(bodyBoundBox.YLength, 3):
      continue
    
    if round(existingBoundBox.ZLength, 3) != round(bodyBoundBox.ZLength, 3):
      continue

    # Center Of Mass
    if not existingShape.CenterOfMass.normalize().isEqual(bodyShape.CenterOfMass.normalize(), 5):
      continue
    
    # Geometry
    if len(existingShape.Edges) != len(bodyShape.Edges):
      continue
    
    if len(existingShape.Faces) != len(bodyShape.Faces):
      continue

    return existingBody

  return None

def getBodies():
  bodies = []
  part = doc.findObjects('App::Part')[0]
  roots = [getRoot(entry) for entry in part.Group]
  bodies = [root for root in roots if isBody(root)]

  bodies.sort(key=lambda b : b.Name)
  
  return bodies

def groupBodies(bodies):
  groups = {}

  for body in bodies:
    matchingBody = findMatchingBody(body, groups)

    if matchingBody is None:
      groups[body] = [body]
    else:
      groups[matchingBody].append(body)
  
  return list(groups.values())

def nameBodies(groups):
  for group in groups:
    name = calculateNextName()

    for body in group:
      if not 'Planname' in body.PropertiesList:
        body.addProperty("App::PropertyString", "Planname", "Info", "Name des Teils in Plänen")
      
      if not 'Anzahl' in body.PropertiesList:
        body.addProperty("App::PropertyInteger", "Anzahl", "Info", "Die Menge der Teile die benötigt werden")
      
      body.Planname = name
      body.Anzahl = len(group)

# Start of script
bodies = getBodies()
groupedBodies = groupBodies(bodies)
nameBodies(groupedBodies)

