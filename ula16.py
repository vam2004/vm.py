class Operation:
    def __init__(self, value, overflow = 0, sign = 0):
        self.value = value
        self.sign = sign
        self.overflow = overflow
    def __repr__(self):
        return f"v={hex(self.value)} o={self.overflow} s={self.sign}"

# return the most significant bit (signal bit)
def getsign(number):
    return (number >> 15) & 0x1
# cast a number into 16-bits integer
def ucast(number):
    return number & 0xffff
# convert a signed 16-bits interger to python signed representation
def tomachine(number):
    if number >> 15:
        return number - 0x10000
    return number
# calculate the 16-bits two's complement of the number 
def inv(number):
    return ((number ^ 0xffff) + 1) & 0xffff
# convert a number from python signed representation to 16-bits signed interger
def frommachine(number):
    if number > 0:
        return (number & 0xffff)
    return number & 0xffff
# signed add
def iadd(left, right):
    value = left + right
    sl = getsign(left)
    sr = getsign(right)
    sv = getsign(value)
    overflow = 0
    if sl == sr:
        overflow = sl ^ sv
    return Operation(ucast(value), overflow, sv)
# unsigned addition
def uadd(left, right):
    value = left + right
    overflow = 0
    if value > 0xffff:
        overflow = 1
    return Operation(ucast(value), overflow)
# unsigned left shift (operation '<<') 
def ulsh(left, right):
    overflow = 1
    value = 0
    if right < 16:
        value = left << right
        overflow = 0
        if value >> 15:
            overflow = 1
    return Operation(ucast(value), overflow)

# unsigned right shift (operation '>>')
def ursh(left, right):
    return Operation(left >> right)
# logical xor
def lxor(left, right):
    return Operation(left ^ right)
# logical and
def land(left, right):
    return Operation(left & right)
# logical or
def lor(left, right):
    return Operation(left | right)

