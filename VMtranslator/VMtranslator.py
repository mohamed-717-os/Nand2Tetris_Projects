import re
from MemoryCommands import *
from ArithmaticLogicCommands import ALCommands
from BranchingCommands  import *
from FunctionCommands import Functions


def translate(filepath):
    VM_file = open(filepath)

    stack = Stack()
    stack.filename = filepath.split('\\')[-1].split('.')[0]

    AL = ALCommands()
    F = Functions()

    # symbols
    memory={
        'push': stack.push,
        'pop':  stack.pop,

    }
    Arithmatic_Logic = {
        'add': AL.add(),
        'sub': AL.sub(),
        'neg': AL.neg(),
        
        'and': AL.AND(),
        'or': AL.OR(),
        'not': AL.NOT(),
    }
    branching = {
        'label': label,
        'goto': goto,
        'if-goto': if_goto
    }

    filecontent = ''
    cursor = VM_file.tell()

    while True:
        line = VM_file.readline()
        
        if cursor == VM_file.tell():
            break

        # comments
        comments = re.search('//',line)
        if comments:
            line = line[:comments.start()]

        # new lines
        new_lines = re.search('^\s*(\n)?$', line)
        if new_lines:
            cursor = VM_file.tell()
            continue

        # // cmmands // 
        # Arithmatic and Logical Commands
        parts = line.split()
        if parts[0] == 'eq':
            line = AL.eq()
        elif parts[0] == 'gt':
            line = AL.gt()
        elif parts[0] == 'lt':
            line = AL.lt()
            
        elif parts[0] in Arithmatic_Logic:
            line = Arithmatic_Logic[parts[0]]

        # Memory access Commands
        elif parts[0] in memory:             
            line = memory[parts[0]](parts[1], int(parts[2]))

        # Branching commands
        elif parts[0] in branching:
            line = branching[parts[0]](parts[1])

        # Function commands
        elif parts[0] == 'function':
            line = F.function(parts[1], int(parts[2]))

        elif parts[0] == 'call':
            line = F.call(parts[1], int(parts[2]))

        elif parts[0] == 'return':
            line = F.Return()
        

        filecontent += line
        cursor = VM_file.tell()

            

    VM_file.close()
    return filecontent
