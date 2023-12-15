def readClass (filename):
    with open(filename) as file:
        lines = [line.rstrip() for line in file]
    classNum = [int(line.split(': ')[0][1:]) for line in lines]
    className = [line.split(': ')[1] for line in lines]
    return classNum, className

if __name__ == "__main__":
    a, b = readClass ('COCO-Classes_Filtered.txt')
