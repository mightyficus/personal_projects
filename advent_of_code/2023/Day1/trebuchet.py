coord_total = 0

with open("input.txt","r") as infile:
    for line in infile:
        digits = []
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