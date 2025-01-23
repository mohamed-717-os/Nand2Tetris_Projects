class Stack:
    def __init__(self):
        self.filename = ''
        self.defult = {'local': 'LCL', 'argument': 'ARG', 'this': 'THIS', 'that': 'THAT'}

    def push(self, segment, i):

        if segment == 'constant':
            #> *sp=i, sp++
            result=f'''
// PUSH {segment} //
    @{i}
    D=A   // D=i

    @SP
    A=M
    M=D   // *sp = D

    @SP
    M=M+1  // sp++
        '''

            return result
    
        if segment == 'temp':
        #> addr = 5 + i 
        #> *sp = *addr
        #> sp++

            result=f'''
// PUSH {segment} //
    @{i+5}
    D=M    // addr={i+5}

    @SP
    A=M
    M=D   // *sp = *addr

    @SP
    M=M+1  // sp++
        '''
            return result

        if segment == 'pointer':
        #> *sp = THIS/THAT, sp++

            if i==0:
                pointer = 'THIS' 
            elif i==1:
                pointer = 'THAT'
            else:
                raise Exception("Error: pointer is only 0 or 1")
            
            result=f'''
// PUSH {segment} //
    @{pointer}
    D=M   // D= THIS/THAT

    @SP
    A=M
    M=D   // *sp = D

    @SP
    M=M+1  // sp++
        '''

            return result

        if segment == 'static': 
            result = f'''
// PUSH {segment} //
    @{self.filename}.{i}
    D=M
    
    @SP
    A=M
    M=D
    
    @SP
    M=M+1'''
            return result       

        if segment in self.defult:
        #> addr = segment + i 
        #> *sp = *addr
        #> sp++

            result=f'''
// PUSH {segment} //
    @{i}
    D=A    // D={i}

    @{self.defult[segment]}
    A=M+D   // addr = {segment} + {i}
    D=M     // D = *addr

    @SP
    A=M
    M=D   // *sp = *addr

    @SP
    M=M+1  // sp++
        '''

            return result

    def pop(self, segment, i):

        if segment == 'constant':
            raise Exception("Error: There is no pop constant operation") 

        if segment == 'temp':
        #> addr = 5 + i 
        #> sp--
        #> *addr = *sp

            result=f'''
// POP {segment} //
    @SP
    M=M-1  // sp--
    A=M
    D=M   // D = *sp

    @{i+5}  // addr = 5 + i 
    M=D    // *addr = *sp
        '''
            return result
    
        if segment == 'pointer':
        #> sp--, THIS/THAT = *sp

            if i==0:
                pointer = 'THIS' 
            elif i==1:
                pointer = 'THAT'
            else:
                raise Exception("Error: pointer is only 0 or 1")
            
            result=f'''
// POP {segment} //
    @SP
    M=M-1  // sp--
    A=M
    D=M   // D = *sp 

    @{pointer}
    M=D   // THIS/THAT = *sp
        '''

            return result

        if segment == 'static': 
            result = f'''
// POP {segment} //
    @SP
    M=M-1
    A=M
    D=M

    @{self.filename}.{i}
    M=D'''
            return result       

        if segment in self.defult:
        #> addr = segment + i 
        #> sp--
        #> *addr = *sp

            result=f'''
// POP {segment} //
    @{i}
    D=A    // D={i}

    @{self.defult[segment]}
    D=M+D     // D = {segment} + {i}

    @addr
    M=D      // addr = {segment} + {i}

    @SP
    M=M-1  // sp--
    A=M
    D=M   // D = *sp

    @addr
    A=M
    M=D   // *addr = *sp
        '''

            return result
