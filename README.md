# Syntatic classes

## JUMP_FAMILY:

    jump 0x0: jump [adress] # uncoditional jump
    jump 0x1: jez [adress]  # jump if equal to zero
    jump 0x2: jnez [adress] # jump if not equal to zero
    jump 0x3: jneg [adress] # jump if negative
    jump 0x4: jpos [adress] # jump if not negative
    jump 0x5: jovr [adress] # jump if overflow
    jump 0x6: jnov [adress] # jump if not overflow
    
## NO_IMEDIATE:

    rdim [register] # read imediate - read a imediate from register
    
## INTERRUPT:

    int [number], [argument] # interrupt 
    
## OPTIONAL_IMEDIATE:

    read    [register], [value]?	# read from a adress
    write   [register], [value]?	# write to a adress
    uadd    [register], [value]?	# unsigned add
    iadd    [register], [value]?	# signed add
    lsh	    [register], [value]?	# left shift
    rsh	    [register], [value]?	# right shift
    xor	    [register], [value]?	# bitwise xor
    and	    [register], [value]?	# bitwise and
    or	    [register], [value]?	# bitwise or
    load    [register], [value]?	# set register with imediate
    
## LINKER_TAGS:


    export [.]<name> [:] # a public label 
    [.]<name> [:] # a label
    ----------------------------------------
    export label <name> [:] # a public label
    label [section_name] [:] # label
    ----------------------------------------
    export const <name> [:] # a public const
    const <name> [:]
    ----------------------------------------
    
    
## DATA_FAMILY:

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
    
