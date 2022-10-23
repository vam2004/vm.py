INSTRUCTIONS = {
    "read": 0, # read from a adress
    "write": 1, # write to a adress
    "jez": 2, # jump if equal zero
    "flag": 3, # flush flag into register
    "addu": 4, # unsigned add
    "add": 5, # signed add
    "lsh": 6, # left shift
    "rsh": 7, # right shift
    "int": 8, # interrupt
    "xor": 9, # bitwise xor
    "and": 10, # bitwise and
    "or": 11, # bitwise or
    "ldim": 12, # load imediate
    # "swap": 13 # swap page adress
}
IMEDIATE_FLAG_MASK = 0x8000
class Instruction:
    def __init__(self, opcode, register, imediate):
        self.opcode = opcode
        self.register = register
        self.imediate = imediate
    @staticmethod
    def parseOpcode(operation):
        opcode = operation & 0x04
        register = (operation >> 0x04) & 0x04
        return (opcode, register)
    @staticmethod
    def createOperation(opcode, register):
        return (opcode & 0x04) | ((register & 0x04) << 0x04)
def parseInt(src):
    if src.startswith("0x"):
        return int(src, base=16)
    return int(src)

def inv_dict(src):
    tmp = {}
    for key, value in src.items():
        tmp[value] = key
    return tmp

DISASSEMBLY_INSTRUCTIONS = inv_dict(INSTRUCTIONS)

def assemblyline(line):
    t0 = line.partition(";")
    t1 = t0[0].partition(",")
    value = None
    if len(t1) > 1:
        rawvalue = t1[2].strip()
        value = parseInt(rawvalue)
        if value > 0xffff or value < 0:
            raise Exception("Invalid value")
    t2 = t1[0].partition(" ")
    if len(t2) < 2:
            raise Exception("Misformed assembly instruction")
    opcode = t2[0]
    register = t2[2]
    if opcode not in INSTRUCTIONS:
        raise Exception("Unknown operation")
    instruction = INSTRUCTIONS[opcode] | (parseRegister(register) << 4)
    if opcode == "ldim":
        #print(f"{opcode} {register}")
        return [instruction]
    elif value is None:
        raise Exception("Expected a argument")
    else:
        #print(f"{opcode} {register}, {rawvalue}")
        return [instruction, (value >> 8) & 0xff, value & 0xff]

def disassembly(mem, pos):
    opcode, register = Instruction.parseOpcode(mem[pos])
    opname = DISASSEMBLY_INSTRUCTIONS[opcode]
    if opcode == INSTRUCTIONS["ldim"]:
        return (f"{opname} r{register}", pos + 1)
    value = ((mem[pos + 1] & 0xff) << 8) | (mem[pos + 2] & 0xff)
    return (f"{opname} r{register}, {hex(value)}", pos + 3)

def assembler(lines):
    program = []
    needdata = False
    for line in lines:
        if line.startswith(".data"):
            needdata = True
            break
        program.extend(assemblyline(line))
    l = len(program)
    l0 = (l >> 24) & 0xff
    l1 = (l >> 16) & 0xff
    l2 = (l >> 8) & 0xff
    l3 = l & 0xff
    data = [l0, l1, l2, l3]
    data.extend(program)
    return data

def getProgramSize(data):
    l0 = (data[0] & 0xff) << 24
    l1 = (data[1] & 0xff) << 16
    l2 = (data[2] & 0xff) << 8
    l3 = (data[3] & 0xff)
    return l0 + l1 + l2 + l3

def dissambler(data):
    l = getProgramSize(data)
    print(f".data {hex(l)}")
    program = data[4:]
    index = 0
    while index < l:
        line, index = disassembly(program, index)
        print(line)
    
def parseRegister(register):
    if register.startswith("r"):
        return int(register.removeprefix("r"))
    return parseInt(register)

class Context:
    def __init__(self, MEMORY = None):
        if MEMORY is None:
            MEMORY = [0] * 0x10000
        if len(MEMORY) < 0x10000:
            needed = 0x10000 - len(MEMORY)
            MEMORY.extend([0] * needed)
        self.INSTRUCTION_POINTER = 4
        self.REGISTERS = [0] * 16
        self.IMEDIATE = 0
        self.FLAGS = 0
        self.MEMORY = MEMORY
    def interrupt(self, INT_ID):
        print(f"INTERRUPT: {INT_ID}")
    def clear_flags(self, mask):
        self.FLAGS = self.FLAGS & (mask ^ 0xffff)
    def set_flags(self, mask):
        self.FLAGS = self.FLAGS | mask
    def get_flags(self, mask):
        return self.FLAGS & mask
    def fetch_instruction(self):
        raw_inst = self.MEMORY[self.INSTRUCTION_POINTER]
        opcode = raw_inst & 0x0f
        register = (raw_inst & 0xf0) >> 0x4
        imediate = self.IMEDIATE
        if self.get_flags(IMEDIATE_FLAG_MASK) or opcode == INSTRUCTIONS["ldim"]:
            self.clear_flags(IMEDIATE_FLAG_MASK)
            self.INSTRUCTION_POINTER += 1
            return Instruction(opcode, register, imediate)
        INSTRUCTION_POINTER = self.INSTRUCTION_POINTER
        imediate = self.read16(INSTRUCTION_POINTER + 1)
        self.INSTRUCTION_POINTER = (INSTRUCTION_POINTER + 3) & 0xffff
        return Instruction(opcode, register, imediate)
    def write16(self, adress, value):
        self.MEMORY[adress] = (value >> 8) & 0xff
        self.MEMORY[adress + 1] = value & 0xff
    def read16(self, adress):
        return ((self.MEMORY[adress] & 0xff) << 8) | (self.memory[adress + 1] & 0xff)
    def write_to(self, register, imediate):
        value = self.REGISTERS[register]
        self.write16(imediate, value)
    def read_from(self, register, imediate):
        self.REGISTERS[register] = self.read16(imediate)

def readprogram():
    lines = []
    try:
        while True:
            tmp = input()
            if tmp.startswith(".end"):
                break
            lines.append(tmp)
    except EOFError:
        pass
    except KeyboardInterrupt:
        pass
    return assembler(lines)

def main():
    memory = readprogram()
    ctx = Context(memory)
    size = getProgramSize(memory)
    dissambler(memory)

main()
    
    
