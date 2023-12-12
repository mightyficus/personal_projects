coord_total = 0
conversion = [("zero","0"), ("one","1"), ("two","2"), ("three","3"), ("four","4"), ("five","5"), ("six","6"), ("seven","7"), ("eight","8"), ("nine","9")]

with open("input.txt","r") as infile:
    for line in infile:
        first_found = True
        digits = []
        newline = []
        oldline = line
        # print(f"Old string is {line}")
        for i in range(0, len(line)-1):
            for conv in conversion:
                # print(f"First two letters: {line[i]}{line[i+1]}, {conv[0][0]}{conv[0][1]}")
                if line[i] == conv[0][0] and line[i+1] == conv[0][1]:
                    line = line.replace(conv[0],conv[1])
                    break
            else:
                continue
            break
        # print(f"Second stage is {line}")
        for i in range(len(line) - 2, 1, -1):
            for conv in conversion:
                # print(f"String letters: {line[i]}{line[i+1].strip()}, conversion letters: {conv[0][0]}{conv[0][1]}")
                if line[i:i + len(conv[0])] == conv[0]:
                    line = line.replace(conv[0], conv[1])
                    break
            else:
                continue
            break
                
        # print(f"Final string is {line}")
                
        for char in line:
            if char.isdigit():
                digits.append(str(char))
        if len(digits) >= 2:
            num = int(digits[0] + digits[-1])
        elif len(digits) == 1:
            num = int(digits[0]+digits[0])
        else:
            num = 0
        coord_total += num
        print(f"Line coord is {num}")
        
print(f"Total is {coord_total}")