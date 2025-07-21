import pandas as pd

def txtToArray(path: str) -> list:
    """Loads a .txt file into an array.

    Args:
        path (string): path of .txt file
    
    Returns:
        data (list): an embedded array of the fetched information of the .txt file (data[line][tab]) 
    """
    print(f"Fetching data from {path}...")
    try:
        with open('data/Results.txt', 'r') as file:
            lines = file.readlines()
            data = [line.strip().split('\t') for line in lines]
        data[4], data[5] = data[4][1:], data[5][1:] 
    except:
        print("no data found. creating empty data array...")
        data = []
    return data

def getXYZ(data: list) -> list:
    newData = [[data[i][j] for j in range(0, len(data[0]), 3)] for i in range(2)]

    coords = data[5] # get coord data
    xyzArr = [[],[],[]] # X,Y,Z coord lists
    for i in range(0, len(coords), 3):
        xyzArr[0].append(coords[i]) # X coordinate
        xyzArr[1].append(coords[i+1]) # Y coordinate
        xyzArr[2].append(coords[i+2]) # Z coordinate
    
    return newData + xyzArr

def pathToST(path: str) -> tuple[str, str]:
    parts = path.split("\\")
    return parts[-4], parts[-3] # get subject, type from parts

def getSubjectAndType(data: list) -> list:
    newData = data[1:]

    paths = data[0]
    subTypeArr = [[], []] # subject, type lists
    
    for path in paths:
        s, t = pathToST(path)
        subTypeArr[0].append(s)
        subTypeArr[1].append(t)
    
    return subTypeArr + newData

def getSideAndPart(data: list) -> list:
    sections = data[1]
    
    parts, sides = [], []
    for section in sections:
        if section.startswith("R_") or section.startswith("L_"):
            sides.append(section[0])
            parts.append(section[2:])
            continue
        sides.append("AXIAL")
        parts.append(section)
    
    return data[:1] + [parts] + [sides] + data[2:]


def arrToDF(data: list) -> pd.DataFrame:
    df = pd.DataFrame({"Subject": data[0], "Type": data[1], "Part": data[2], "Side": data[3], "X": data[4], "Y": data[5], "Z": data[6]})
    return df

def txtToCleanDf(path: str) -> pd.DataFrame:
    data = txtToArray(path="data/Results.txt")
    data = getXYZ(data)
    data = getSideAndPart(data)
    data = getSubjectAndType(data)
    df = arrToDF(data)
    return df

df = txtToCleanDf(path="data/Results.txt")
df.to_csv('data/CleanedResults.csv', index=False)