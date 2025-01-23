from MemoryCommands import *

class Functions:
    def __init__(self):
        self.funcname = ''
        self.retnum = 1

    def function(self, name, nVars):
        self.funcname = name
        result = f'''
({name})'''
        
        for i in range(nVars):
            result += f'''
    @{i}
    D=A

    @LCL
    A=M+D
    M=0
    
    @SP
    M=M+1'''
                        
        return result
    
    def call(self, name, nArgs):
        result = f'''
// call {name}
    @{self.funcname}$ret.{self.retnum}
    D=A
    
    @SP
    A=M
    M=D
    
    @SP
    M=M+1''' #> push returnAddress
        
        # saves caller segments
            #> a tricky way to chose segments memory value
        result += Stack().push('temp', -4)
        result += Stack().push('temp', -3)
        result += Stack().push('temp', -2)
        result += Stack().push('temp', -1)

        # repositions LCL & ARG
        result += f'''
    @SP
    D=M
    
    @LCL
    M=D

    @{5+nArgs}
    D=D-A

    @ARG
    M=D'''
        
        # go to function
        result += f'''
    @{name}
    0;JMP

({self.funcname}$ret.{self.retnum})''' #> return address
        
        self.retnum += 1
        return result
    
    def Return(self):
        result = f'''
// return
    @LCL
    D=M

    @endFrame
    M=D''' #> endFrame = LCL
        
        result += f'''
    @5
    D=A
    
    @LCL
    A=M-D
    D=M
    
    @retAddr
    M=D''' #> retAdd = *(LCL-5)
        
        result += Stack().pop('argument', 0)
        result += '''
    @ARG
    D=M+1
    
    @SP
    M=D''' #> SP = ARG+1
        
        # Restores caller segments
        result += '''
    @endFrame
    A=M-1
    D=M
    
    @THAT
    M=D
    
    @2
    D=A
    @endFrame
    A=M-D
    D=M
    
    @THIS
    M=D
    
    @3
    D=A
    @endFrame
    A=M-D
    D=M
    
    @ARG
    M=D
    
    @4
    D=A
    @endFrame
    A=M-D
    D=M
    
    @LCL
    M=D''' 
        
        result += '''
    @retAddr
    A=M
    0;JMP''' # End
        
        return result
        
        
