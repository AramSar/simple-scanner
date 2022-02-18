import sys

letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
digits = "0123456789"
string_quote = '"'
valid_lexems = [
"*",
"&",
"+",
"-",
"=",
"#",
"<",
"<=",
">",
">=",
":",
":=",
";",
":",
",",
".",
"or",
"div",
"mod",
"char",
"integer",
"boolean",
"begin",
"false",
"true",
"not",
"(",
")",
"while",
"repeat",
"until",
"do",
"loop",
"end",
"if",
"else",
"elsif",
"procedure",
"const",
"type",
"var",
"module",
"import"
]

def getSym():
    file_loc = sys.argv[1]
    with open(file_loc, 'r') as f:
        while True:
            char = f.read(1)
            if not char:
                break
            yield char


def check_lexems(chars, lexem_list=valid_lexems):
    matches = []
    for e in lexem_list:
        if chars == e[:len(chars)]:
            matches.append(e)
    return matches


def scanner():
    lexems = []
    reader = getSym()
    flags = [False, False, False, False, False] # digit, identifier, string, v_lexem, error
    curr_lexem=""
    curr_v_lexems=[]

    def interrupted_lexem_appension(curr_lexem, flags, curr_v_lexems):
        nonlocal lexems
        if curr_lexem in curr_v_lexems:
            lexems.append(curr_lexem)
        elif set(curr_lexem).intersection(set(letters)):
            curr_lexem+=": Identifier"
            lexems.append(curr_lexem)
        else:
            curr_lexem+=": Invalid Lexem"
            lexems.append(curr_lexem)

    def transition(curr_lexem, flags, curr_v_lexems):
        nonlocal lexems
        if flags[0]:
            curr_lexem+=": Number"
            lexems.append(curr_lexem)
            curr_lexem=""
            flags[0] = False
        elif flags[1]:
            curr_lexem+=": Identifier"
            lexems.append(curr_lexem)
            curr_lexem=""
            flags[1] = False
        elif flags[4]:
            curr_lexem+=": Invalid Lexem"
            lexems.append(curr_lexem)
            curr_lexem=""
            flags[4] = False
        elif flags[3]:
            interrupted_lexem_appension(curr_lexem, flags, curr_v_lexems)
            flags[3] = False
            curr_lexem=""

        return curr_lexem, flags

    def validator(next_char, flags, curr_lexem, curr_v_lexems):
        nonlocal lexems
        if next_char == " " or next_char == "\n" or next_char == "\t" and not flags[2]:
            curr_lexem, flags = transition(curr_lexem, flags, curr_v_lexems)
            return curr_lexem, flags, curr_v_lexems
        
        if not any(flags):
            v_lexems = check_lexems(next_char)
            if len(v_lexems) > 0:
                curr_v_lexems = v_lexems.copy()
                curr_lexem += next_char
                flags[3] = True

                return curr_lexem, flags, curr_v_lexems
                    
        if next_char in letters and not any(flags):
            flags[1] = True
            curr_lexem+=next_char
            return curr_lexem, flags, curr_v_lexems

        if next_char in digits and not any(flags):
           curr_lexem+=next_char
           flags[0] = True
           return curr_lexem, flags, curr_v_lexems
        
        if next_char in string_quote and not flags[2]:
           curr_lexem, flags = transition(curr_lexem, flags, curr_v_lexems)
           curr_lexem+=next_char
           flags[2] = True
           return curr_lexem, flags, curr_v_lexems


        if flags[3]:
            expected_lexem = curr_lexem+next_char
            expected_mathches = check_lexems(expected_lexem, curr_v_lexems)
            if len(expected_mathches) > 0:
                curr_lexem+=next_char
                curr_v_lexems = expected_mathches
                return curr_lexem, flags, curr_v_lexems
            else:
                if curr_lexem in curr_v_lexems:
                    curr_lexem, flags = transition(curr_lexem, flags, curr_v_lexems)
                    return validator(next_char, flags, curr_lexem, curr_v_lexems)
                else:
                    if not set(curr_lexem).intersection(set(letters)):
                        curr_lexem+=next_char
                        flags[3] = False
                        flags[4] = True
                        curr_v_lexems = []
                        curr_lexem, flags = transition(curr_lexem, flags, curr_v_lexems)
                    else:
                        flags[3] = False
                        flags[1] = True
                        curr_v_lexems = []

                    return validator(next_char, flags, curr_lexem, curr_v_lexems)

        if flags[2]:
            if next_char not in string_quote:
                curr_lexem+=next_char
                return curr_lexem, flags, curr_v_lexems
            else:
                curr_lexem+=next_char
                curr_lexem+=": String"
                lexems.append(curr_lexem)
                curr_lexem=""
                flags[2]=False
                return curr_lexem, flags, curr_v_lexems
        
            
        if flags[0]:
            if next_char in digits:
                curr_lexem+=next_char
                return curr_lexem, flags, curr_v_lexems
            elif next_char in letters:
                curr_lexem+=next_char
                flags[0] = False
                flags[4] = True
                return curr_lexem, flags, curr_v_lexems
            else:
                curr_lexem, flags = transition(curr_lexem, flags, curr_v_lexems)
                return validator(next_char, flags, curr_lexem, curr_v_lexems)
            
        if flags[4]:
            if next_char in digits or next_char in letters:
                curr_lexem+=next_char
                return curr_lexem, flags, curr_v_lexems
            else:
                curr_lexem, flags = transition(curr_lexem, flags, curr_v_lexems)
                return validator(next_char, flags, curr_lexem, curr_v_lexems)
        
        if flags[1]:
            if next_char in letters or next_char in digits:
                curr_lexem+=next_char
                return curr_lexem, flags, curr_v_lexems
            else:
                curr_lexem, flags = transition(curr_lexem, flags, curr_v_lexems)
                return validator(next_char, flags, curr_lexem, curr_v_lexems)
        
        curr_lexem, flags = transition(curr_lexem, flags, curr_v_lexems)
        lexems.append(next_char+": Invalid Lexem")
        return curr_lexem, flags, curr_v_lexems


    for next_char in reader:
        curr_lexem, flags, curr_v_lexems = validator(next_char, flags, curr_lexem, curr_v_lexems)
        # print(next_char, curr_lexem, flags, curr_v_lexems)

    
    # Post processing of the remaining parts of the lexems
    if flags[4] or flags[2]:
        curr_lexem+=": Invalid Lexem"
        lexems.append(curr_lexem)
    elif flags[1]:
        curr_lexem+=": Identifier"
        lexems.append(curr_lexem)
    elif flags[0]:
        curr_lexem+=": Number"
        lexems.append(curr_lexem)
    elif flags[3]:
       interrupted_lexem_appension(curr_lexem, flags, curr_v_lexems)


    for e in lexems:
        print(e)
            


if __name__ == '__main__':
    scanner()