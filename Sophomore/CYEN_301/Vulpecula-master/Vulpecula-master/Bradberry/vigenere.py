import sys
import string

mode = sys.argv[1]
key = "".join(ch for ch in sys.argv[2].upper() if ch.isupper())
py3 = sys.version_info[0] > 2

lower_values = {l:i for i,l in enumerate(string.ascii_lowercase)}
upper_values = {l:i for i,l in enumerate(string.ascii_uppercase)}

if mode == "-e":
    while(True):
        try:
            if py3:
                to_encode = input()
            else:
                to_encode = raw_input()
        except (EOFError):
                break

        encoded = ""
        
        key_index = 0

        for l in range(len(to_encode)):
            if to_encode[l].isupper():
                encoded += string.ascii_uppercase[(upper_values[to_encode[l]] + upper_values[key[key_index % len(key)]]) % 26]
                key_index += 1
            elif to_encode[l].islower():
                encoded += string.ascii_lowercase[(lower_values[to_encode[l]] + upper_values[key[key_index % len(key)]]) % 26]
                key_index += 1
            else:
                encoded += to_encode[l]
        print(encoded)
elif mode == "-d":
    while(True):
        try:
            if py3:
                to_decode = input()
            else:
                to_decode = raw_input()
        except (EOFError):
            break
        decoded = ""
        
        key_index = 0

        for l in range(len(to_decode)):
            if to_decode[l].isupper():
                decoded += string.ascii_uppercase[(upper_values[to_decode[l]] - upper_values[key[key_index % len(key)]]) % 26]
                key_index += 1
            elif to_decode[l].islower():
                decoded += string.ascii_lowercase[(lower_values[to_decode[l]] - upper_values[key[key_index % len(key)]]) % 26]
                key_index += 1
            else:
                decoded += to_decode[l]
        print(decoded)

else:
    print("Illegal argument. Try \"-e\" or \"-d\"")
