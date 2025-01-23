def label(name):
    result = f'''
({name})'''
    
    return result

def goto(label):
    result = f'''
// goto {label}
    @{label}
    0;JMP'''
    
    return result

def if_goto(label):
    result = f'''
// if-goto {label}
    @SP
    M=M-1
    A=M
    D=M

    @{label}
    D;JNE  //  if D=0 => *SP = false'''  
    
    return result