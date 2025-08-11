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
  bodies = []
  
  for o in part.Group:
    root = getRoot(o)
    
    if not isBody(root):
      continue

    bodies.append(o)

  return bodies

def add_to_values(values, body):
  new_value = 0

  match values['kind']:
    case 'lfm':
      new_value = body.Laenge.Value / 1000
    case 'm2':
      new_value = body.Laenge.Value / 1000 * body.Breite.Value / 1000
    case 'm3':
      new_value = body.Laenge.Value / 1000 * body.Breite.Value / 1000 * body.Staerke.Value / 1000
  
  values['amount'] += new_value

def print_bom(groups):
  overal_price = 0

  for group, values in groups.items():
    # + 10% verschnitt
    amount = round(values['amount'] * 1.1, 2)
    kind = values['kind']
    price = round(values['einzelpreis'] * amount, 2)

    overal_price += price
    
    print(f'{group}: {amount} {kind}, {price}€')
  
  print(f'Gesamtpreis: {round(overal_price)}€')

# Start of script
parts = FreeCAD.ActiveDocument.findObjects('App::Part')
for part in parts:
  bodies = getBodies(part)

  if len(bodies) == 0:
    print('No obects found')
    continue

  groups = {}
  
  for body in bodies:
    typ = body.Typ

    if typ not in groups:
      groups[typ] = {'amount': 0, 'einzelpreis': body.Einzelpreis, 'kind': body.Abrechnung_Art}
    
    add_to_values(groups[typ], body)
  
  print_bom(groups)