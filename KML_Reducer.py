# Script reduces number of coordinates in .kml files
import xml.dom.minidom as md

file = md.parse('data/plz.kml')
areas = []

# iterate over every polygon circle
for coordinate in file.getElementsByTagName("coordinates"):
    text = ''
    # convert to list
    cList = coordinate.childNodes[0].nodeValue.split(",")

    # remove last three elements
    del cList[-1]
    del cList[-1]
    del cList[-1]

    # save first two elements
    firstC = cList.pop(0)
    secondC = cList.pop(0)

    # delete every second coordinate [length, width]
    del cList[::4]
    del cList[::3]

    # build start and end of polygon circle
    cList.insert(0, firstC)
    cList.insert(1, secondC)
    cList.append('0 ' + firstC)
    cList.append(secondC)
    cList.append('0')

    # convert back to string
    for element in cList:
        text += element + ','

    # build new reduced string
    text = text[:-1]
    areas.append(text)

areas.reverse()

# update <coordinates> tags in kml file
for element in file.getElementsByTagName("coordinates"):
    element.childNodes[0].nodeValue = areas.pop()

# write to xml file
with open("data/newPlz.kml", "wb") as fs:
    fs.write(file.toxml("utf-8"))
    fs.close()
