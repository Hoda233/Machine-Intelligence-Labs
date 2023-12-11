from typing import Tuple
import re
from CSP import Assignment, Problem, UnaryConstraint, BinaryConstraint

#TODO (Optional): Import any builtin library or define any helper function you want to use

# This is a class to define for cryptarithmetic puzzles as CSPs
class CryptArithmeticProblem(Problem):
    LHS: Tuple[str, str]
    RHS: str

    # Convert an assignment into a string (so that is can be printed).
    def format_assignment(self, assignment: Assignment) -> str:
        LHS0, LHS1 = self.LHS
        RHS = self.RHS
        letters = set(LHS0 + LHS1 + RHS)
        formula = f"{LHS0} + {LHS1} = {RHS}"
        postfix = []
        valid_values = list(range(10))
        for letter in letters:
            value = assignment.get(letter)
            if value is None: continue
            if value not in valid_values:
                postfix.append(f"{letter}={value}")
            else:
                formula = formula.replace(letter, str(value))
        if postfix:
            formula = formula + " (" + ", ".join(postfix) +  ")" 
        return formula

    @staticmethod
    def from_text(text: str) -> 'CryptArithmeticProblem':
        # Given a text in the format "LHS0 + LHS1 = RHS", the following regex
        # matches and extracts LHS0, LHS1 & RHS
        # For example, it would parse "SEND + MORE = MONEY" and extract the
        # terms such that LHS0 = "SEND", LHS1 = "MORE" and RHS = "MONEY"
        pattern = r"\s*([a-zA-Z]+)\s*\+\s*([a-zA-Z]+)\s*=\s*([a-zA-Z]+)\s*"
        match = re.match(pattern, text)
        if not match: raise Exception("Failed to parse:" + text)
        LHS0, LHS1, RHS = [match.group(i+1).upper() for i in range(3)]

        problem = CryptArithmeticProblem()
        problem.LHS = (LHS0, LHS1)
        problem.RHS = RHS

        #TODO Edit and complete the rest of this function
        # problem.variables:    should contain a list of variables where each variable is string (the variable name)
        # problem.domains:      should be dictionary that maps each variable (str) to its domain (set of values)
        #                       For the letters, the domain can only contain integers in the range [0,9].
        # problem.constaints:   should contain a list of constraint (either unary or binary constraints).

        problem.variables = []
        problem.domains = {}
        problem.constraints = []
        
        # variables 
        all_chars = LHS0 + LHS1 + RHS
        unique_chars = set()
        for char in all_chars:
            unique_chars.add(char)

        unique_chars = list(unique_chars)

        # carries
        
        no_of_carries = len(RHS) - 1
        
        carries = []
        for i in range(no_of_carries):
            # var = chr(ord('a')+i)
            var = 'C'+str(i)
            carries.append(var)

        problem.variables = unique_chars + carries
        # print(problem.variables)

        # domains 
        last_digits = set()
        last_digits.add(LHS0[0])
        last_digits.add(LHS1[0])
        last_digits.add(RHS[0])

        for var in unique_chars:
            if var in last_digits:
                problem.domains[var] = set(range(1, 10))
            else:
                problem.domains[var] = set(range(0, 10))

        for c in carries:
            problem.domains[c] = set(range(0, 2))
        
        # print(problem.domains)

        # constraints 
        
        # all different constraint
        for v1 in unique_chars:
            for v2 in unique_chars:
                if v1 is not v2:
                    binary_constraint = BinaryConstraint((v1,v2), lambda value1, value2:  value1 != value2)
                    problem.constraints.append(binary_constraint)
        

        LHS0_rev = LHS0[::-1]
        LHS1_rev = LHS1[::-1]
        RHS_rev = RHS[::-1]

        min_length = min(len(LHS0), len(LHS1))
        max_length = max(len(LHS0), len(LHS1))
        l0_length, l1_length, r_length = len(LHS0), len(LHS1), len(RHS)
        

        for i in range(r_length): 
            if i == 0:
                # A + B = C + 10 C1

                aux1 = (LHS0_rev[i], LHS1_rev[i])
                aux2 = (RHS_rev[i], carries[i])

                problem.variables.append(aux1)
                problem.variables.append(aux2) 

                dom=set()
                for x in problem.domains[LHS0_rev[i]]:
                    for y in problem.domains[LHS1_rev[i]]:
                        dom.add((x,y))
                problem.domains[aux1] = dom

                dom=set()
                for x in problem.domains[RHS_rev[i]]:
                    for y in problem.domains[carries[i]]:
                        dom.add((x,y))
                problem.domains[aux2] = dom
                
                binary_constraint = BinaryConstraint((LHS0_rev[i],aux1), lambda a, b: a == b[0])
                problem.constraints.append(binary_constraint)

                binary_constraint = BinaryConstraint((LHS1_rev[i],aux1), lambda a, b: a == b[1])
                problem.constraints.append(binary_constraint)
                
                print(RHS_rev[i],aux2,aux2[0],aux2[1])
                binary_constraint = BinaryConstraint((RHS_rev[i],aux2), lambda a, b: a == b[0])
                problem.constraints.append(binary_constraint)

                binary_constraint = BinaryConstraint((carries[i],aux2), lambda a, b: a == b[1])
                problem.constraints.append(binary_constraint)

                binary_constraint = BinaryConstraint((aux1,aux2), lambda a, b: a[0] + a[1]  == b[0] + 10 * b[1])
                problem.constraints.append(binary_constraint)

                
            
            elif i == r_length - 1:

                if i < l0_length and i < l1_length:
                    # A + B + C1 = C 
                    aux1 = (LHS0_rev[i], LHS1_rev[i], carries[i - 1])
                    
                    problem.variables.append(aux1) 

                    dom=set()
                    for x in problem.domains[LHS0_rev[i]]:
                        for y in problem.domains[LHS1_rev[i]]:
                            for z in problem.domains[carries[i - 1]]:
                                    dom.add((x,y,z))
                    problem.domains[aux1] = dom
                    
                    binary_constraint = BinaryConstraint((LHS0_rev[i],aux1), lambda a, b: a == b[0])
                    problem.constraints.append(binary_constraint)

                    binary_constraint = BinaryConstraint((LHS1_rev[i],aux1), lambda a, b: a == b[1])
                    problem.constraints.append(binary_constraint)

                    binary_constraint = BinaryConstraint((carries[i-1],aux1), lambda a, b: a == b[2])
                    problem.constraints.append(binary_constraint)

                    binary_constraint = BinaryConstraint((aux1,RHS_rev[i]), lambda a, b: a[0] + a[1] + a[2] == b)
                    problem.constraints.append(binary_constraint)

                    

                elif i < l0_length and i>=l1_length:
                    # C1 + A     = C

                    aux1 = (LHS0_rev[i], carries[i - 1])
                    
                    problem.variables.append(aux1) 

                    dom=set()
                    for x in problem.domains[LHS0_rev[i]]:
                        for y in problem.domains[carries[i-1]]:
                                    dom.add((x,y))
                    problem.domains[aux1] = dom
                    
                    binary_constraint = BinaryConstraint((LHS0_rev[i],aux1), lambda a, b: a == b[0])
                    problem.constraints.append(binary_constraint)

                    binary_constraint = BinaryConstraint((carries[i-1],aux1), lambda a, b: a == b[1])
                    problem.constraints.append(binary_constraint)

                    binary_constraint = BinaryConstraint((aux1,RHS_rev[i]), lambda a, b: a[0] + a[1] == b)
                    problem.constraints.append(binary_constraint)

                    

                elif i >= l0_length and i<l1_length:
                    # C1 + B     = C

                    aux1 = (LHS1_rev[i], carries[i - 1])
                    
                    problem.variables.append(aux1) 

                    dom=set()
                    for x in problem.domains[LHS1_rev[i]]:
                        for y in problem.domains[carries[i-1]]:
                                    dom.add((x,y))
                    problem.domains[aux1] = dom
                    
                    binary_constraint = BinaryConstraint((LHS1_rev[i],aux1), lambda a, b: a == b[0])
                    problem.constraints.append(binary_constraint)

                    binary_constraint = BinaryConstraint((carries[i-1],aux1), lambda a, b: a == b[1])
                    problem.constraints.append(binary_constraint)

                    binary_constraint = BinaryConstraint((aux1,RHS_rev[i]), lambda a, b: a[0] + a[1] + a[2] == b)
                    problem.constraints.append(binary_constraint)

                    

                elif i >= l0_length and i >= l1_length:
                    # C1 = C
                    binary_constraint = BinaryConstraint((carries[i-1],RHS_rev[i]), lambda a, b: a == b)
                    problem.constraints.append(binary_constraint)

                    
            
            else: 
                if i < l0_length and i < l1_length:
                    # A + B + C1 = C + 10 C2
                    aux1 = (LHS0_rev[i], LHS1_rev[i], carries[i - 1])
                    aux2 = (RHS_rev[i], carries[i])

                    problem.variables.append(aux1) 
                    problem.variables.append(aux2) 

                    dom=set()
                    for x in problem.domains[LHS0_rev[i]]:
                        for y in problem.domains[LHS1_rev[i]]:
                            for z in problem.domains[carries[i - 1]]:
                                dom.add((x,y,z))
                    problem.domains[aux1] = dom

                    dom=set()
                    for x in problem.domains[RHS_rev[i]]:
                        for y in problem.domains[carries[i]]:
                            dom.add((x,y))
                    problem.domains[aux2] = dom


                    binary_constraint = BinaryConstraint((LHS0_rev[i],aux1), lambda a, b: a == b[0])
                    problem.constraints.append(binary_constraint)

                    binary_constraint = BinaryConstraint((LHS1_rev[i],aux1), lambda a, b: a == b[1])
                    problem.constraints.append(binary_constraint)

                    binary_constraint = BinaryConstraint((carries[i-1],aux1), lambda a, b: a == b[2])
                    problem.constraints.append(binary_constraint)

                    binary_constraint = BinaryConstraint((RHS_rev[i],aux2), lambda a, b: a  == b[0])
                    problem.constraints.append(binary_constraint)

                    binary_constraint = BinaryConstraint((carries[i],aux2), lambda a, b: a  == b[1])
                    problem.constraints.append(binary_constraint)

                    binary_constraint = BinaryConstraint((aux1,aux2), lambda a, b: a[0] + a[1] + a[2] == b[0] + 10 * b[1])
                    problem.constraints.append(binary_constraint)
                
                else:
                    if i < l0_length and i>=l1_length:
                        # A + C1     = C + 10 C2
                        aux1 = (LHS0_rev[i] , carries[i - 1])
                        aux2 = (RHS_rev[i] , carries[i])

                        problem.variables.append(aux1)
                        problem.variables.append(aux2) 

                        dom=set()
                        for x in problem.domains[LHS0_rev[i]]:
                            for y in problem.domains[carries[i-1]]:
                                dom.add((x,y))
                        problem.domains[aux1] = dom

                        dom=set()
                        for x in problem.domains[RHS_rev[i]]:
                            for y in problem.domains[carries[i]]:
                                dom.add((x,y))
                        problem.domains[aux2] = dom

                        binary_constraint = BinaryConstraint((LHS0_rev[i],aux1), lambda a, b: a == b[0])
                        problem.constraints.append(binary_constraint)

                        

                    elif i >= l0_length and i<l1_length:
                        # B + C1     = C + 10 C2
                        aux1 = (LHS1_rev[i] , carries[i - 1])
                        aux2 = (RHS_rev[i] , carries[i])

                        problem.variables.append(aux1)
                        problem.variables.append(aux2) 

                        dom=set()
                        for x in problem.domains[LHS1_rev[i]]:
                            for y in problem.domains[carries[i-1]]:
                                dom.add((x,y))
                        problem.domains[aux1] = dom

                        dom=set()
                        for x in problem.domains[RHS_rev[i]]:
                            for y in problem.domains[carries[i]]:
                                dom.add((x,y))
                        problem.domains[aux2] = dom


                        binary_constraint = BinaryConstraint((LHS1_rev[i],aux1), lambda a, b: a == b[0])
                        problem.constraints.append(binary_constraint)

                    binary_constraint = BinaryConstraint((carries[i - 1],aux1), lambda a, b: a == b[1])
                    problem.constraints.append(binary_constraint)

                    binary_constraint = BinaryConstraint((RHS_rev[i],aux2), lambda a, b: a == b[0])
                    problem.constraints.append(binary_constraint)

                    binary_constraint = BinaryConstraint((carries[i],aux2), lambda a, b: a == b[1])
                    problem.constraints.append(binary_constraint)

                    binary_constraint = BinaryConstraint((aux1,aux2), lambda a, b: a[0] + a[1]  == b[0] + 10 * b[1])
                    problem.constraints.append(binary_constraint)

                    
    

        return problem

    # Read a cryptarithmetic puzzle from a file
    @staticmethod
    def from_file(path: str) -> "CryptArithmeticProblem":
        with open(path, 'r') as f:
            return CryptArithmeticProblem.from_text(f.read())


