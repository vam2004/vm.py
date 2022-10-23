"""
JUMP_FAMILY:
    jmp 0x0: jmp [adress] # uncoditional jump
    jmp 0x1: jez [adress] # jump if equal to zero
    jmp 0x2: jnez [adress] # jump if not equal to zero
    jmp 0x3: jneg [adress] # jump if negative
    jmp 0x4: jpos [adress] # jump if not negative
    jmp 0x5: jovr [adress] # jump if overflow
    jmp 0x6: jnov [adress] # jump if not overflow

NO_IMEDIATE:
    int [number] # interrupt 
    ldim [register] # load imediate - read a imediate from register

NORMAL:
    read    # read from a adress
    write   # write to a adress
    uadd    # unsigned add
    iadd    # signed add
    lsh	    # left shift
    rsh	    # right shift
    xor	    # bitwise xor
    and	    # bitwise and
    or	    # bitwise or
    ldim    # load imediate
    rdim    # read imediate

LINKER_TAGS:
    data [section_name] [:] # represent a data section
    func [section_name] [:] # represent a public function declaration

DATA_FAMILY:
    byte [8bits]    # 8-bits constant
    word [16bits]   # 16-bits constant
    dword [32bits]  # 32-bits constant
    qword [64bits]  # 64-bits constant
    bytes [bytes]   # vector of bytes

SECTION:
    [.] [section_name] [:] # define a label
"""

class INSTRUCTIONS:
    inst_read = 0   # read from a adress
    inst_write = 1  # write to a adress
    # jump family: 0x2
    inst_uadd = 3   # unsigned add
    inst_iadd = 4   # signed add
    inst_lsh = 5    # left shift
    inst_rsh = 6    # right shift
    inst_int = 7    # interrupt
    inst_xor = 8    # bitwise xor
    inst_and = 9    # bitwise and
    inst_or = 10    # bitwise or
    inst_ldim = 11  # load imediate
    inst_rdim = 12  # read imediate
    DISASSEMBLY_NAMES = {
        0: "read",	# read from a adress
        1: "write",	# write to a adress
        # jump family: 0x2
        3: "uadd",	# unsigned add
        4: "iadd",	# signed add
        5: "lsh",	# left shift
        6: "rsh",	# right shift
        7: "int",	# interrupt
        8: "xor",	# bitwise xor
        9: "and",	# bitwise and
        10: "or",	# bitwise or
        11: "ldim",	# load imediate
        12: "rdim",	# read imediate
    }
    ASSEMBLY_NAMES = {
        "read": 0,	# read from a adress
        "write": 1,	# write to a adress
        # jump family: 0x2
        "uadd": 3,	# unsigned add
        "iadd": 4,	# signed add
        "lsh": 5,	# left shift
        "rsh": 6,	# right shift
        "int": 7,	# interrupt
        "xor": 8,	# bitwise xor
        "and": 9,	# bitwise and
        "or": 10,	# bitwise or
        "ldim": 11,	# load imediate
        "rdim": 12,	# read imediate
    }

class JUMP_ID:
    inst_jmp: 0
    inst_jez: 1
    inst_jnez: 2
    inst_jneg: 3
    inst_jpos: 4
    inst_jovr: 5
    inst_jnov: 6
    JUMP_NUMBER = {
        "jmp": 0x0,
        "jez": 0x1,
        "jnez": 0x2,
        "jneg": 0x3,
        "jpos": 0x4,
        "jovr": 0x5,
        "jnov": 0x6,
    }
    JUMP_NAMES = {
        0: "jmp",
        1: "jez",
        2: "jnez",
        3: "jneg",
        4: "jpos",
        5: "jovr",
        6: "jnov",
    }
