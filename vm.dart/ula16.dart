class Operation {
  int value;
  int overflow;
  int sign;
  Operation(this.value, [this.overflow = 0, this.sign = 0]);
  @override
  toString() {
    String hexvalue = value.toRadixString(16);
    return "v=0x$hexvalue o=$overflow s=$sign";
  }
}
int getsign(int number) {
  return (number >> 15) & 0x1;
}
// cast a number into 16-bits integer
int ucast(int number) {
  return number & 0xffff;
}
// convert a signed 16-bits interger to python signed representation
int tomachine(int number) {
  if (number >> 15 != 0) {
    return number - 0x10000;
  }
  return number;
}
// calculate the 16-bits two's complement of the number 
int inv(int number) {
  return ((number ^ 0xffff) + 1) & 0xffff;
} 
// convert a number from python signed representation to 16-bits signed interger
int frommachine(int number) {
  if (number > 0) {
    return (number & 0xffff);
  }
  return number & 0xffff;
}
// signed add
Operation iadd(int left, int right) {
  int value = left + right;
  int sl = getsign(left);
  int sr = getsign(right);
  int sv = getsign(value);
  int overflow = 0;
  if(sl == sr){
    overflow = sl ^ sv;
  }
  return Operation(ucast(value), overflow, sv);
}
// unsigned addition
Operation uadd(int left, int right) {
  int value = left + right;
  int overflow = 0;
  if (value > 0xffff) {
    overflow = 1;
  }
  return Operation(ucast(value), overflow);
}
// unsigned left shift (operation '<<') 
Operation ulsh(int left, int right) {
  int overflow = 1;
  int value = 0;
  if (right < 16) {
    value = left << right;
    overflow = 0;
    if(value >> 15 != 0){
      overflow = 1;
    }
  }
  return Operation(ucast(value), overflow);
}
// unsigned right shift (operation '>>')
Operation ursh(int left, int right) {
  return Operation(left >> right);
}
// logical xor
Operation lxor(left, right) {
  return Operation(left ^ right);
} 
// logical and
Operation land(left, right) {
  return Operation(left & right);
}
// logical or
Operation lor(left, right) {
  return Operation(left | right);
}

