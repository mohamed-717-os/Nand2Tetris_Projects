import re

filename = r'pong/PongL.asm'
asmfile = open(filename)
hackfile = open(filename.split('.')[0] + '.hack', 'w')

symbols = {
    'R0':'0',
    'R1':'1',
    'R2':'2',
    'R3':'3',
    'R4':'4',
    'R5':'5',
    'R6':'6',
    'R7':'7',
    'R8':'8',
    'R9':'9',
    'R10':'10',
    'R11':'11',
    'R12':'12',
    'R13':'13',
    'R14':'14',
    'R15':'15',
    'SCREEN':'16384',
    'KBD': '24576',
    'SP':'0',
    'LCL':'1',
    'ARG':'2',
    'THIS':'3',
    'THAT':'4'
}
comp_list = {
    '0': '0101010',
    '1': '0111111',
    '-1': '0111010',
    'D': '0001100',
    'A': '0110000',
    'M': '1110000',
    '!D': '0001101',
    '!A': '0110001',
    '!M': '1110001',
    '-D': '0001111',
    '-A': '0110011',
    '-M': '1110011',
    'D+1': '0011111',
    'A+1': '0110111',
    'M+1': '1110111',
    'D-1': '0001110',
    'A-1': '0110010',
    'M-1': '1110010',
    'D+A': '0000010',
    'D+M': '1000010',
    'D-A': '0010011',
    'D-M': '1010011',
    'A-D': '0000111',
    'M-D': '1000111',
    'D&A': '0000000',
    'D&M': '1000000',
    'D|A': '0010101',
    'D|M': '1010101'
}
dest_list = {
    'null': '000',
    'M': '001',
    'D': '010',
    'MD': '011',
    'A': '100',
    'AM': '101',
    'AD': '110',
    'AMD': '111'
}
jump_list = {
    'null': '000',
    'JGT': '001',
    'JEQ': '010',
    'JGE': '011',
    'JLT': '100',
    'JNE': '101',
    'JLE': '110',
    'JMP': '111'
}

reference =  16
cursor = asmfile.tell()

# first pass
line_num = 0
while True:
    line = asmfile.readline()
    
    if cursor == asmfile.tell():
        break

    # comments
    comments = re.search('//',line)
    if comments:
        line = line[:comments.start()]

    # new lines
    new_lines = re.search('^\s*(\n)?$', line)
    if new_lines:
        cursor = asmfile.tell()
        continue
    

    Lable = re.search('^\s*[(][a-zA-Z].*[)]$',line)
    if Lable:
        lable = line.strip()[1:-1]
        symbols[lable] = str(line_num)
        
        line_num -= 1
    
    line_num += 1
    cursor = asmfile.tell()

asmfile.seek(0)

# second pass
while True:
    line = asmfile.readline()
    if cursor == asmfile.tell():
        break

    # comments
    comments = re.search('//',line)
    if comments:
        line = line[:comments.start()]

    # new lines and lables
    new_lines = re.search('^\s*(\n)?$', line)
    Lable = re.search('^\s*[(][a-zA-Z].*[)]$',line)

    if new_lines or Lable:
        continue
    
    # variables  
    variables = re.search('^\s*@[a-zA-Z].*$',line)
    if variables:
        var = line.strip()[1:]
        if var in symbols.keys():
            line = '@'+ symbols[var]

        else:
            symbols[var] = str(reference)
            line = '@'+ str(reference)
            reference += 1

    # A-instruction
    A_instruction = re.search('^\s*(@\d+)$',line)
    if A_instruction:
        digits = line.strip()[1:]
        binary_digits = '{0:015b}\n'.format(int(digits))
        line = '0' + binary_digits

    else:
    # C-instruction
        if re.search('^\s*(.*=.*;.*)$',line):
            dest = line.strip().split('=')[0]
            comp = line.strip().split('=')[1].split(';')[0]
            jump = line.strip().split(';')[1]

            line = '111' + comp_list[comp] + dest_list[dest] + jump_list[jump] + '\n'

        elif re.search('^\s*(.*=.*)$',line):
            dest = line.strip().split('=')[0]
            comp = line.strip().split('=')[1].split(';')[0]
            jump = 'null'

            line = '111' + comp_list[comp] + dest_list[dest] + jump_list[jump] + '\n'

        elif re.search('^\s*(.*;.*)$',line):
            dest = 'null'
            comp = line.strip().split(';')[0]
            jump = line.strip().split(';')[1]

            line = '111' + comp_list[comp] + dest_list[dest] + jump_list[jump] + '\n'
        
    hackfile.writelines(line)
    cursor = asmfile.tell()

hackfile.close()
asmfile.close()

