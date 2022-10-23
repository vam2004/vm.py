"""
JUMP_FAMILY:
    jump 0x0: jump [adress] # uncoditional jump
    jump 0x1: jez [adress] # jump if equal to zero
    jump 0x2: jnez [adress] # jump if not equal to zero
    jump 0x3: jneg [adress] # jump if negative
    jump 0x4: jpos [adress] # jump if not negative
    jump 0x5: jovr [adress] # jump if overflow
    jump 0x6: jnov [adress] # jump if not overflow

NO_IMEDIATE:
    rdim [register] # read imediate - read a imediate from register

INTERRUPT:
    int [number], [argument] # interrupt 
NORMAL:
    read    [register], [value]	# read from a adress
    write   [register], [value]	# write to a adress
    uadd    [register], [value]	# unsigned add
    iadd    [register], [value]	# signed add
    lsh	    [register], [value]	# left shift
    rsh	    [register], [value]	# right shift
    xor	    [register], [value]	# bitwise xor
    and	    [register], [value]	# bitwise and
    or	    [register], [value]	# bitwise or
    load    [register], [value]	# set register with imediate

LINKER_TAGS:
    export [.]<name> [:] # a public label 
    [.]<name> [:] # a label
    ----------------------------------------
    export label <name> [:] # a public label
    label [section_name] [:] # label
    ----------------------------------------
    export const <name> [:] # a public const
    const <name> [:]
    ----------------------------------------
DATA_FAMILY:
    byte  [hexdecimal]  # 8-bits constant
    word  [hexdecimal]  # 16-bits constant
    dword [hexdecimal]  # 32-bits constant
    qword [hexdecimal]  # 64-bits constant
    bword [hexdecimal]  # 128-bits constant
    -------------------------------------------
    bytes  [bytes]  # raw bytes
    string [string] # a string
    -------------------------------------------
    decimal byte  [number]  # 01-bytes constant
    decimal word  [number]  # 02-bytes constant
    decimal dword [number]  # 04-bytes constant
    decimal qword [number]  # 08-bytes constant
    decimal bword [number]  # 16-bytes constant
    
SECTION:
    [.] [section_name] [:] # define a label
"""

"""
# -------------------------------
# hello world program in assembly
# -------------------------------
const hello:
    string "hello world"
export label .entrypoint:
    load r1, 11
    load r0, .hello
    label loop:
        int 15, 0x0000
        uadd r1, 1
        sub r1, 1
        jnez .loop
"""

"""
NUMBER ::= ((?:0x[0-9a-fA-F]*)|(?:[1-9][0-9]*))
REGISTER ::= ([rR][0-9][1-5]?)
NORMAL_INSTRUCTION ::= <INSTRUCTION_NAME> <REGISTER> (,) <value>
INT_INSTRUCTION ::= "int" | <NUMBER>
LDIM_INSTRUCTION ::= "ldim" | <REGISTER>

"""
import re
class LinkerTag:
    def __init__(self, visibility, kind, name):
        self.kind = kind
        self.visibility = visibility
        self.name = LinkerTag.normalize_name(name)
    @staticmethod
    def normalize_name(name):
        if name[0] != ".":
            return "." + name
        return name
    def __repr__(self):
        return f"[SECTION] {self.visibility} {self.kind} [{self.name}]"
    def __str__(self):
        return self.__repr__()
    
class ScapeUtf:
    class InvalidScape(Exception):
        pass
    scape_words = {
	'0': '\0',
	'a': '\a',
	'b': '\b',
	't': '\t',
	'n': '\n',
	'v': '\v',
	'f': '\f',
	'r': '\r',
	'e': '\e',
	'"': '\"',
        '\\': '\\',
        '\'': '\'',
    }
    def __init__(self):
        self.buffer = []
        self.length = 0
        self.uninit = True
    def feed(self, value):
        if self.uninit:
            if value in ScapeUtf.scape_words:
                return ScapeUtf.scape_words[value]
            if value == "u":
                self.length = 4
            elif value == "x":
                self.length = 2
            else:
                raise ScapeUtf.InvalidScape()
            self.uninit = False
            return False
        if self.length:
            self.buffer.append(value)
            self.length -= 1
            return False
        data = "".join(self.buffer)
        return chr(int(data, base=16))

class ReadString:
    class UnclosedString(Exception):
        pass
    def __init__(self):
        self.scape_parse = None
        self.buffer = []        
        self.scape_level = 0
    def scape_mode(self, value):
        scaped = self.scape_parse.feed(value)
        if scaped:
            self.keep(scaped)
            self.scape_level = 0
            self.scape_parse = None
            return False
        return True
    def keep(self, value):
        self.buffer.append(value)
    def feed(self, value):
        if self.scape_level:
            if self.scape_mode(value):
                return False
        if value == '\\':
            self.scape_parse = ScapeUtf()
            self.scape_level = 1
            return False
        if value == '"':
            return "".join(self.buffer)
        self.keep(value)
        return False
    def parse(self, buffer):
        for index, value in enumerate(buffer):
            data = self.feed(value)
            if data:
                return (data, index)
        raise ReadString.UnclosedString()

class InvalidLinkerTag(Exception):
    pass

class REGEXS:
    SECTION_NAME = re.compile(r"[.]\w+$")
    REGISTER = re.compile("[Rr](?:[02-9]|1[0-5]?)")
class InlineData:
    SIZES = {
        "bytes": 0, # dynamic sized
        "byte": 1,
        "word": 2,
        "dword": 4,
        "qword": 8,
        "bword": 16,
    }
    class RequiredData(Exception):
        pass
    class MisalignedByte(Exception):
        pass
    class MisalignedBytes(MisalignedByte):
        pass
    def __init__(self, data, aligment, bytenum):
        InlineData.validade_alignment(data, aligment, bytenum)
        self.data = data
    @staticmethod
    def validade_alignment(data, aligment, bytenum):
        if aligment & 1:
            raise InlineData.MisalignedByte("Memory always is byte aligned, please use padding")
        if bytenum > 1:
            if len(data) != bytenum:
                print(data, bytenum >> 1)
                raise InlineData.MisalignedBytes("Invalid number alignment, please use padding")
        elif bytenum == 0:
            if aligment:
                raise InlineData.MisalignedBytes("'bytes' are 16-bits aligned")
    @staticmethod
    def read_bytes(rawdata):
        print(rawdata)
        rawdata = rawdata.replace(" ", "")
        if len(rawdata) < 2:
            raise InlineData.RequiredData()
        buffer = []
        _byte = int(rawdata[:2], base=16)
        align = 1
        for value in rawdata[2:]:
            bitpos = align & 1
            if bitpos:
                buffer.append(_byte)
                _byte = 0x00
            parsed = int(value, base=16)
            _byte = _byte | parsed << (bitpos << 2)
            align = (align + 1) % 4
        if align & 1:
            buffer.append(_byte)
        # (align != 3) => ERROR 
        return (buffer, 3 - align)
    
def parseInt(src):
    if src.startswith("0x"):
        return int(src, base=16)
    return int(src)

class Instruction:
    class InvalidRegister(Exception):
        pass
    NAMES = ["read", "write", "uadd", "iadd",
             "lsh", "rsh", "int", "xor", "and", "or", "rdim", "load"]
    NUMBERS = {
        "read": 0,	# read from a adress
        "write": 1,	# write to a adress
        "jump": 2,      # JUMP_FAMILY
        "uadd": 3,	# unsigned add
        "iadd": 4,	# signed add
        "lsh": 5,	# left shift
        "rsh": 6,	# right shift
        "int": 7,	# interrupt
        "xor": 8,	# bitwise xor
        "and": 9,	# bitwise and
        "or": 10,	# bitwise or
        "rdim": 11,	# load imediate
        "load": 12,	# read imediate
    }
    def __init__(self, name, register, imediate = ""):
        self.parse(name, register, imediate)
    def parse(self, name, register, imediate):
        self.name = name
        self.parse_oregs(name, register, imediate)
        self.parse_ocode(name, register, imediate)
        self.parse_value(name, register, imediate)
    def parse_oregs(self, name, register, imediate):
        if register.startswith("r"):
            self.register = int(register.removeprefix("r"))
        elif self.oregs_kind() == 2:
            self.register = parseInt(register)
        else:
            raise Instruction.InvalidRegister()
    def parse_ocode(self, name, register, imediate):
        self.opcode = Instruction.NUMBERS[name]
    def parse_value(self, name, register, imediate):
        if imediate == "":
            self.imediate = None
        else:
            self.imediate = parseInt(imediate.strip())
    def instruction(self):
        return Assembler.create_operation(self.opcode, self.register)
    def represent_oregs(self):
        kind = self.oregs_kind()
        prefix = "r"
        if kind == 2:
            prefix = ""
        return prefix + str(self.register)
    def represent_oname(self):
        return self.name
    def represent_value(self):
        imediate = "%IMEDIATE%"
        if self.imediate is not None:
            imediate = hex(self.imediate)
        return imediate
    def oregs_kind(self):
        # 0 == normal register
        # 1 == register less
        # 2 == number as register
        return 0
    def value_kind(self):
        # 0 == normal imediate
        # 1 == imediate less
        return 0
    def __repr__(self):
        value = self.represent_value()
        oname = self.represent_oname()
        if self.oregs_kind() == 1:
            return f"{oname} {value}"
        oregs = self.represent_oregs()
        return f"{oname} {oregs}, {value}"

class JumpFamily(Instruction):
    OPCODE = Instruction.NUMBERS["jump"]
    NAMES = ["jump", "jez","jnez","jneg","jpos","jovr","jnov"]
    NUMBERS = {
        "jmp": 0x0,
        "jez": 0x1,
        "jnez": 0x2,
        "jneg": 0x3,
        "jpos": 0x4,
        "jovr": 0x5,
        "jnov": 0x6,
    }
    def parse_oregs(self, name, register, imediate):
        self.register = JumpFamily.NUMBERS[name]
    def parse_ocode(self, name, register, imediate):
        self.opcode = JumpFamily.OPCODE # JUMP_FAMILY
    def oregs_kind(self):
        return 1

def InstInterrupt(Instruction):
    def oregs_kind(self):
        return 2
def InstRdim(Instruction):
    def value_kind(self):
        return 1

class Assembler:
    @staticmethod
    def issection(line):
        for prefix in [".", "export", "label", "const"]:
            if(line.startswith(prefix)):
                return line.endswith(":")
        return False
    @staticmethod
    def remove_comments(line):
        string_mode = False
        scape_mode = False
        for index, value in enumerate(line):
            if string_mode:
                if scape_mode:
                    scape_mode = False
                    continue
                if value == '\\':
                    scape_mode = True
                    continue
                if value == '"':
                    string_mode = False
                continue
            if value == '"':
                string_mode = True
                continue
            if value == '#':
                return line[:index]
        return line
    
    @staticmethod
    def linker_tags(line): # parses linker tags and returns LinkerTag(kind, name)
        line = line.removesuffix(":").strip()
        visibility = "private"
        if line.startswith("export"): # read export modifier
            visibility = "public"
            line = line.removeprefix("export").strip() # discard the modifier and trailing spaces
        if line.startswith("."):
            name = REGEXS.SECTION_NAME.match(line)
            kind = "label"
            if name is None:
                raise InvalidLinkerTag()
            return LinkerTag(visibility, kind, name.group())
        for prefix in ["const", "label"]:
            if(line.startswith(prefix)):
                line = line.removeprefix(prefix).strip()
                name = None
                if line[0] == '"':
                    parser = ReadString()
                    length = len(line)
                    name, index = parser.parse(line)
                    name = '"' + name + '"'
                    if length != index + 1:
                        raise InvalidLinkerTag()
                else:
                    name = REGEXS.SECTION_NAME.match(line)
                    if name is None:
                        raise InvalidLinkerTag()
                    name = name.group()
                return LinkerTag(visibility, prefix, name)
    @staticmethod
    def is_inline_data(line):
        opcode = line.split()[0]
        for keyword in ["decimal", "byte", "word", "dword", "qword", "bword", "bytes"]:
            if keyword == opcode:
                return True
        return False
    @staticmethod
    def inline_data(line): # parses inline data and returns InlineData([...bytes])
        opcode = line.split()[0]
        if opcode == "decimal":
            raise NotImplementedError("decimal constant not implemeted")
        line = line.removeprefix(opcode).strip()
        data, align = InlineData.read_bytes(line)
        return InlineData(data, align, InlineData.SIZES[opcode])
    @staticmethod
    def is_brach(line):
        opcode = line.split()[0]
        for prefix in JumpFamily.NAMES:
            if opcode == prefix:
                return True
        return False
    @staticmethod
    def branch(line): # parses jump family and returns JumpFamily(kind, adress)
        opcode = line.split()[0]
        imediate = line.removeprefix(opcode).strip()
        return JumpFamily(opcode, None, imediate)
    @staticmethod
    def has_no_imediate(line):
        pass
    @staticmethod
    def no_imediate(line):
        pass
    @staticmethod
    def is_instruction(line):
        opcode = line.split()[0]
        for prefix in Instruction.NAMES:
            if opcode == prefix:
                return True
        return False
    @staticmethod
    def instruction(line): # parses normal instruction and returns Instruction(operation, imediate)
        opcode = line.split()[0]
        line = line.removeprefix(opcode).strip()
        register, _, imediate = line.partition(",")
        if opcode == "int":
            return InstInterrupt(opcode, register, imediate)
        if opcode == "rdim":
            return InstRdim(opcode, register)
        return Instruction(opcode, register, imediate)
    @staticmethod
    def pre_parse(line):
        line = Assembler.remove_comments(line).strip()
        if line == "": # empty line
            return False
        if Assembler.issection(line):
            return Assembler.linker_tags(line)
        if Assembler.is_inline_data(line):
            return Assembler.inline_data(line)
        if Assembler.is_brach(line):
            return Assembler.branch(line)
        if Assembler.has_no_imediate(line):
            return Assembler.no_imediate(line)
        if Assembler.is_instruction(line):
            return Assembler.instruction(line)
        raise NotImplementedError("unknown or not implemeted sintax")
    @staticmethod
    def create_operation(opcode, register):
        # assert not opcode >> 4 and not register >> 4
        opcode = opcode & 0x4 # sanity the input
        register = register & 0x4  # sanity the input
        return opcode | (register << 0x4)



"""        
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
"""



