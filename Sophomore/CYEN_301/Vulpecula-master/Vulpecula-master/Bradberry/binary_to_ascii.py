import sys

py3 = sys.version_info[0] > 2

try:
    if py3:
        binary_string = str(input())
    else:
        binary_string = str(raw_input())
except (EOFError):
    pass

if len(binary_string) % 7 == 0:
    chars = []
    for x in range(len(binary_string) / 7):
        chars.append(int(binary_string[7 * x : 7 * (x + 1)], base=2))
    string_repr = ""
    for ch in chars:
        string_repr += chr(ch)
    print(string_repr)

if len(binary_string) % 8 == 0:
    chars = []
    for x in range(len(binary_string) / 8):
        chars.append(int(binary_string[8 * x : 8 * (x + 1)], base=2))
    string_repr = ""    
    for ch in chars:
        string_repr += chr(ch)
    print (string_repr)

