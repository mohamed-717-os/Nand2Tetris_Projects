from Statements import *

typepattern = ['int', 'char', 'boolean']

def subroutineBody(file, cursor, space=1):
    file.seek(cursor)

    while True:
        char = file.read(1)
        if char == '{':
            break
    result = '  '*(space-1) + '<subroutineBody>\n'

    result += '  '*space + '<symbol> { </symbol>\n'

    cursor = file.tell()
    while True:
        line = file.readline()
        startVar = re.search('^\s*var', line)

       
        if startVar:
            endVar = re.search(';', line)
            result += varDec(line[:endVar.start()], space+1)

            cursor = cursor + endVar.end()

        elif re.search('^\s*//', line):
            cursor = file.tell()
            continue
        elif re.search('^\s*\w', line):
            break

    result += '  '*(space) + '<statements>\n'

    while True:
        result += statements(file, cursor, space+1)
        cursor = file.tell()

        endif = re.search(r'^\s*\}', file.readline()) 
        if endif:
            file.seek(cursor + endif.end())
            break

    result += '  '*(space) + '</statements>\n'
    result += '  '*space + '<symbol> } </symbol>\n'
    result += '  '*(space-1) + '</subroutineBody>\n'
    return result

def parameterList(plist, space=1):
    result = '  '*(space-1) + '<parameterList>\n'

    parameters = re.split('\s*,\s*', plist.strip())

    if plist.strip():
        for p in parameters:
            tokins = p.split()
            result += chooseType(tokins[0], typepattern, space)

            result += '  '*space + f'<identifier> {tokins[1]} </identifier>\n'

            if p != parameters[-1]:
                result += '  '*space + f'<symbol> , </symbol>\n'

    result+= '  '*(space-1) + '</parameterList>\n'
    return result

def subroutineDec(file,cursor, space=1):
    file.seek(cursor)
    s = file.readline()
    result = '  '*(space-1) + '<subroutineDec>\n'

    listpattern = re.search(r'\(.*\)', s)
    tokins = s[:listpattern.start()].split()

    result += '  '*space + f'<keyword> {tokins[0]} </keyword>\n'

    result += chooseType(tokins[1], typepattern + ['void'], space)
    result += '  '*space + f'<identifier> {tokins[2]} </identifier>\n'


    result += '  '*space + '<symbol> ( </symbol>\n'
    result += parameterList(listpattern.group()[1:-1], space+1)
    result += '  '*space + '<symbol> ) </symbol>\n'

    cursor = cursor + listpattern.end()
    result += subroutineBody(file, cursor, space+1)

    result += '  '*(space-1) + '</subroutineDec>\n'
    return result

def classVarDec(c, space=1):
    c = c.strip()
    result = '  '*(space-1) + '<classVarDec>\n'

    tokins = re.split('\s*,\s*|\s+', c[:-1])

    result += '  '*space + f'<keyword> {tokins[0]} </keyword>\n'

    result += chooseType(tokins[1], typepattern, space)

    for t in tokins[2:]:
        result += '  '*space + f'<identifier> {t} </identifier>\n'

        if t != tokins[-1]:
            result += '  '*space + f'<symbol> , </symbol>\n'

    result += '  '*space + f'<symbol> ; </symbol>\n'

    result+= '  '*(space-1) + '</classVarDec>\n'
    return result

def classCombile(file,cursor, space=1):
    file.seek(cursor)
    endExpression = cursor
    
    while True:
        char = file.read(1)
        if char == '{':
            break
        else: endExpression += 1

    result = '  '*(space-1) + '<class>\n'

    result += '  '*space + '<keyword> class </keyword>\n'

    cursor += 5
    file.seek(cursor)
    className = file.read(endExpression - cursor).strip()
    result += '  '*space + f'<identifier> {className} </identifier>\n'

    result += '  '*space + '<symbol> { </symbol>\n'

    cursor = endExpression+1
    while True:
        line = file.readline().strip()
        endif = re.search(r'\}', line)
        if endif:
            file.seek(cursor + endif.end())
            break

        multi, line = comments(file, line)
        if multi:
            cursor = file.tell()
            continue

        if re.search('^(static|field)', line):
            endCommand = re.search(';', line).end()
            result += classVarDec(line[:endCommand], space+1)

        elif re.search('^(constructor|function|method)', line):
            file.seek(cursor)
            result += subroutineDec(file, cursor, space+1)
        
        cursor = file.tell()

    result += '  '*space + '<symbol> } </symbol>\n'
    result += '  '*(space-1) + '</class>\n'
    return result


def comments(file, line):
    # comments
    comments = re.search('//',line)
    if comments:
        line = line[:comments.start()]

    # multiline comment
    comment = re.search(r'/\*\*', line)
    if comment:
        while True:
            cursor = file.tell()
            commentEnd = re.search(r'\*/', line)
            if commentEnd:
                # cursor -= cursor - commentEnd.end()
                file.seek(cursor)
                break

            line = file.readline()

        return True, line
        
    return False, line


def varDec(v, space=1):

    result = '  '*(space-1) + '<varDec>\n'
    tokins = re.split('\s*,\s*|\s+', v.strip())

    result += '  '*space + f'<keyword> var </keyword>\n'

    result += chooseType(tokins[1], typepattern, space)
    for t in tokins[2:]:
        result += '  '*space + f'<identifier> {t} </identifier>\n'

        if t != tokins[-1]:
            result += '  '*space + f'<symbol> , </symbol>\n'

    result += '  '*space + f'<symbol> ; </symbol>\n'
    result += '  '*(space-1) + '</varDec>\n'
    return result

def chooseType(t, types, space):
    if t in types:
        return '  '*space + f'<keyword> {t} </keyword>\n'

    else:
        return '  '*space + f'<identifier> {t} </identifier>\n'
