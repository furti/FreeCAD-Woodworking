import FreeCAD
import math

spreadsheet = FreeCAD.ActiveDocument.findObjects(Label="Kosten")[0]

def isLink(o):
    return o.TypeId == "App::Link"


def isBody(o):
    return o.TypeId == "PartDesign::Body"

def isPart(o):
    return o.TypeId == "App::Part"

def getRoot(o):
    root = o

    while isLink(root):
        root = root.LinkedObject

    return root

def getBodies(part):
    bodies = []

    for o in part.Group:
        root = getRoot(o)
        if isPart(root):
            bodies.extend(getBodies(root))
        elif isBody(root):
            bodies.append(root)

    return bodies

# Berechnet wie viele teile der einzelLaenge gebraucht werden, um all laengen zu schneiden
def calculateNumber(laengen, einzelLaenge):
    rests = []
    pieces = 0

    for laenge in laengen:
        restMatches = False
        # Prüfen ob ein reststueck lang genug ist
        for i in range(len(rests)):
            rest = rests[i]

            if rest >= laenge:
                rests[i] = rest - laenge
                restMatches = True
                break
        
        # ansonsten neues reststück erzeugen
        if not restMatches:
            pieces += 1
            newRest = einzelLaenge - laenge
            rests.append(newRest)

    return pieces


# Start of script
parentDoc = FreeCAD.ActiveDocument
parts = parentDoc.findObjects('App::Part')
allTypes = []
staffel58Laenge = []
lattenLaenge = []
bretterLaenge = []
steherLaenge = []

for part in parts:
    bodies = getBodies(part)
  
    for body in bodies:
        if not body.Typ:
            print(body.Label + ' hat keinen typ')
        elif body.Typ == 'Staffel':
            print(body.Label + ' ist Staffel')
        elif body.Typ == 'Staffel 5x8':
            staffel58Laenge.append(body.Laenge.Value)
        elif body.Typ == 'Latte':
            lattenLaenge.append(body.Laenge.Value)
        elif body.Typ == 'Brett':
            bretterLaenge.append(body.Laenge.Value)
        elif body.Typ == 'Steher':
            steherLaenge.append(body.Laenge.Value)
        elif body.Typ == 'Brett_Flaeche':
            anzahl = math.ceil(body.Breite.Value / 700)
            bretterLaenge.extend([body.Laenge.Value] * anzahl)
        else:
            print(body.Typ + ' Unmatched type')
        
        allTypes.append(body.Typ)

#Latten für Dach
lattenLaenge.extend([741, 741, 1900, 799, 799])

# Schmuckbretter
bretterLaenge.extend([1747, 1747, 1700, 1700, 1060, 1060, 1060, 1060, 1060, 1060, 1240, 1240, 1398, 1398, 1160, 1160, 1398])

print(set(allTypes))
staffel58Anzahl4m = calculateNumber(staffel58Laenge, 4000) + 1
staffel58Anzahl5m = calculateNumber(staffel58Laenge, 5000) + 1
lattenAnzahl4m = calculateNumber(lattenLaenge, 4000) + 2
lattenAnzahl5m = calculateNumber(lattenLaenge, 5000) + 2
bretterAnzahl = calculateNumber(bretterLaenge, 4000) + 5
steherAnzahl = calculateNumber(steherLaenge, 5000)
fallschutmatteAnzahl = 5
teichfolieAnzahl = 1


spreadsheet.set("B1", "'4m")
spreadsheet.set("C1", "'Kosten 4m")
spreadsheet.set("D1", "'5m")
spreadsheet.set("E1", "'Kosten 5m")

spreadsheet.set("A2", "'Staffel 5x8")
spreadsheet.set("B2", str(staffel58Anzahl4m))
spreadsheet.set("C2", str(staffel58Anzahl4m * 9.42))
spreadsheet.set("D2", str(staffel58Anzahl5m))
spreadsheet.set("E2", str(staffel58Anzahl5m * 11.78))

spreadsheet.set("A3", "'Latte")
spreadsheet.set("B3", str(lattenAnzahl4m))
spreadsheet.set("C3", str(lattenAnzahl4m * 5.65))
spreadsheet.set("D3", str(lattenAnzahl5m))
spreadsheet.set("E3", str(lattenAnzahl5m * 7.07))

spreadsheet.set("A4", "'Bretter")
spreadsheet.set("B4", str(bretterAnzahl))
spreadsheet.set("C4", str(bretterAnzahl * 3.7))

spreadsheet.set("A5", "'Fallschutzmatte")
spreadsheet.set("B5", str(fallschutmatteAnzahl))
spreadsheet.set("C5", str(fallschutmatteAnzahl * 9.99))

spreadsheet.set("A6", "'Teichfolie")
spreadsheet.set("B6", str(teichfolieAnzahl))
spreadsheet.set("C6", str(teichfolieAnzahl * 26.99))

spreadsheet.set("A7", "'Steher 8x8")
spreadsheet.set("D7", str(steherAnzahl))
spreadsheet.set("E7", str(steherAnzahl * 27.84))

# Better einzeln + Bretter fläche
# Dachpappe von Dachfläche
# Teichfolie Fläche Fallschutzmatte + 20%