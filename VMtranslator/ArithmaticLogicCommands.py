class ALCommands:
    def __init__(self):
        self.eq_n = 1
        self.gt_n = 1
        self.lt_n = 1

    def add(self):
        result = '''
// add //
    @SP
    M=M-1
    A=M
    D=M
    
    @SP
    M=M-1
    A=M
    M=M+D
    
    @SP
    M=M+1'''

        return result

    def sub(self):
        result = '''
// sub //
    @SP
    M=M-1
    A=M
    D=M
    
    @SP
    M=M-1
    A=M
    M=M-D
    
    @SP
    M=M+1'''

        return result

    def neg(self):
        result = '''
// neg //
    @SP
    M=M-1
    A=M
    M=-M
    
    @SP
    M=M+1'''

        return result

    def eq(self):
        result = f'''
// eq //
    @SP
    M=M-1
    A=M
    D=M
    
    @SP
    M=M-1
    A=M
    D=M-D

    @TRUE.EQ{self.eq_n}
    D;JEQ

// FALSE 
    @SP
    A=M
    M=0

    @NEXT.EQ{self.eq_n}
    0;JMP

(TRUE.EQ{self.eq_n})
    @SP
    A=M
    M=-1
    
(NEXT.EQ{self.eq_n})
    @SP
    M=M+1'''

        self.eq_n += 1
        return result

    def gt(self):
        result = F'''
// gt //
    @SP
    M=M-1
    A=M
    D=M
    
    @SP
    M=M-1
    A=M
    D=M-D

    @TRUE.GT{self.gt_n}
    D;JGT

// FALSE 
    @SP
    A=M
    M=0

    @NEXT.GT{self.gt_n}
    0;JMP

(TRUE.GT{self.gt_n})
    @SP
    A=M
    M=-1
    
(NEXT.GT{self.gt_n})
    @SP
    M=M+1'''

        self.gt_n += 1
        return result

    def lt(self):
        result = f'''
// lt //
    @SP
    M=M-1
    A=M
    D=M
    
    @SP
    M=M-1
    A=M
    D=M-D

    @TRUE.LT{self.lt_n}
    D;JLT

// FALSE 
    @SP
    A=M
    M=0

    @NEXT.LT{self.lt_n}
    0;JMP

(TRUE.LT{self.lt_n})
    @SP
    A=M
    M=-1
    
(NEXT.LT{self.lt_n})
    @SP
    M=M+1'''

        self.lt_n += 1
        return result

    def AND(self):
        result = '''
// AND //
    @SP
    M=M-1
    A=M
    D=M
    
    @SP
    M=M-1
    A=M
    M=M&D
    
    @SP
    M=M+1'''

        return result

    def OR(self):
        result = '''
// OR //
    @SP
    M=M-1
    A=M
    D=M
    
    @SP
    M=M-1
    A=M
    M=M|D
    
    @SP
    M=M+1'''

        return result

    def NOT(self):
        result = '''
// NOT //
    @SP
    M=M-1
    A=M
    M=!M
    
    @SP
    M=M+1'''

        return result
