import os, sys

table = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "SCREEN": 16384,
    "KBD": 24576,
    "R0": 0,
    "R1": 1,
    "R2": 2,
    "R3": 3,
    "R4": 4,
    "R5": 5,
    "R6": 6,
    "R7": 7,
    "R8": 8,
    "R9": 9,
    "R10": 10,
    "R11": 11,
    "R12": 12,
    "R13": 13,
    "R14": 14,
    "R15": 15,
    }

comp = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "!D": "0001101",
    "!A": "0110001",
    "-D": "0001111",
    "-A": "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",
    "M": "1110000",
    "!M": "1110001",
    "-M": "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101"
    }


dest = {
    "null": "000",
    "M": "001",
    "D": "010",
    "A": "100",
    "MD": "011",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
    }


jump = {
    "null": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
    }

currVariable = 16
root = sys.argv[1]

def aIdentify(line):
    if line[1].isnumeric():
        origValue = int(line[1:])
    else:
        label = line[1:-1]
        origValue = table.get(label, "N/A")
        if origValue == "N/A":
            global currVariable
            table[label] = currVariable
            origValue = currVariable
            currVariable += 1
    return bin(origValue)[2:].zfill(16)



def cIdentify(line):
    line = line[:-1]
    if ";" not in line:
        line = line + ";null"
    elif "=" not in line:
        line = "null=" + line
    instruction = []
    first = line.split("=")
    print(line + "\n")
    print(first[0])
    instruction.append(dest.get(first[0], "N/A"))
    second = first[1].split(";")
    print(second[0])
    instruction.append(comp.get(second[0], "N/A"))
    print(second[1])
    instruction.append(jump.get(second[1], "N/A"))

    return instruction

def identify(line):
    first = line[0]
    instruction = []
    if first == "@":            #A Instruction
        return aIdentify(line)
    else:                       #C Instruction
        instruction = cIdentify(line)

    return "111" + instruction[1] + instruction[0] + instruction[2]

def remove(line):
    first = line[0]
    if first == "\n" or first == "/":
        return ""
    elif first == " ":
        return remove(line[1:])
    else:
        return first + remove(line[1:])

def firstPass():
    f = open(root + ".asm")
    o = open(root + ".tmp", "w")
    numLine = 0
    for line in f:
        formattedLine = remove(line)
        if formattedLine != "":
            if formattedLine[0] == "(":
                label = formattedLine[1:-1]
                table[label] = numLine
            else:
                numLine += 1
                o.write(formattedLine)
                o.write("\n")
    
    f.close()
    o.close()

def secondPass():
    f = open(root + ".tmp")
    o = open(root + ".hack", "w")

    for line in f:
        formattedLine = identify(line)
        o.write(formattedLine)
        o.write("\n")

    f.close()
    o.close()


firstPass()
secondPass()