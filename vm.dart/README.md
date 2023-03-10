# Assembly Specification
A `instruction` is composed by the `operation` byte followed optionally by the two byte big-endian `imediate`. 
The imediate can be calculate as `imediate := bytes[1] * 256 + bytes[2]`, while the operation is the first byte `operation := bytes[0]`. The operation also is also subvided into `field:opcode` (the lesser significant 4-bits) and `field:register` (the most significant 4-bits) fields.

Instructions that accept a imediate can enter `imediateless` mode (or `register-register` mode), which read a value previuosly loaded into a cache. The `imediateless` is triggered by the `flag:imediate`, which is cleared in next instruction.
# Halting
	The interrupt `int 00, 0x0000`, should always either halt the machine, indicating the end of all syncronous procedure or a recorverable failure in the interrupt handler, unless the `flag:interrupt` was cleared.
# Syntatic classes

## Branch family:
This class is reserved for instructions that modify the control flow of program. All instructions in assembly represent a combination of a single `instruction_code` with a `register_id`, which encoded the behavior (condition of branch) of that instructions.

    jump 0x0: jump [adress] # uncoditional jump
    jump 0x1: jez [adress]  # jump if equal to zero
    jump 0x2: jnez [adress] # jump if not equal to zero
    jump 0x3: jneg [adress] # jump if negative
    jump 0x4: jpos [adress] # jump if not negative
    jump 0x5: jovr [adress] # jump if overflow
    jump 0x6: jnov [adress] # jump if not overflow
 
## Pragma Instruction:
This class contains a function that change the syntax of the next instructions. In special, one instruction can make the next instruction use the data inside one register intead of a imediate, tranforming all instruction that is "register - imediate" into "register - register" mode.

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
## The imediate sintax 
The imediate could be:
 1. A unsigned decimal number stating with non zero decimal digit (among with 1-9) or containg only "0", and containing only decimal digits
 - example: "18920"
 2. A unsigned hexadecimal number prefixed "0x" or ending with sufix "h", and contaning only case-insentive hexadecimal digits
 - examples: "0x198F", "f7h" and "07h"
 3. A unsigned binary number stating with prefix "0b" and contaning only binary digits ("0" and "1")
 - example: "0b0011"
 4. A two-complement negative number starting with prefix "-" and followed by any unsigned counterpart specified at (1) until (3)
 - example: "-0b101", "-9", "-9h", "-09h", "-0"
 5. All numbers specified at (1) until (4) with sepator "'" among digits that are not prefix or sufix
 6. A label starting with "."
 7. A macro starting with a alphabetical character, including underscore, followed optionally by any alphanumeric character or underscore
 8. The indentifier "label" followed by "(" with a string label and ending with ")"
## LINKER_TAGS:


    export [.]<name> [:] # a public label 
    [.]<name> [:] # a private label
    ----------------------------------------
    export label <name> [:] # a public label
    label [section_name] [:] # a private label
    ----------------------------------------
    export const <name> [:] # a public const
    const <name> [:] # a private const
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
 
# Binary Structure


