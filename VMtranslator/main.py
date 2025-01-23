import os
from VMtranslator import translate

# r'ProgramFlow\BasicLoop'
# r'ProgramFlow\FibonacciSeries'

# r'FunctionCalls\SimpleFunction'
# r'FunctionCalls\FibonacciElement'
# r'FunctionCalls\StaticsTest'

path = r'FunctionCalls\StaticsTest'
filecontent = ''
files = os.listdir(path)

if 'Sys.vm' in files:
    files.remove('Sys.vm')
    files.insert(0, 'Sys.vm')

for x in files:
    if x.endswith(".vm"):
        filepath = f'{path}\{x}'

        filecontent += translate(filepath)

hackpath = os.path.join(path, path.split('\\')[-1]+'.asm')
hackfile = open(hackpath, 'w')
hackfile.write(filecontent)

hackfile.close()
