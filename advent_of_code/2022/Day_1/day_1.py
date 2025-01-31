"""
The jungle must be too overgrown and difficult to navigate in vehicles or access from the air; the Elves' expedition traditionally goes on foot. As your boats approach land, the Elves begin taking inventory of their supplies. One important consideration is food - in particular, the number of Calories each Elf is carrying (your puzzle input).

The Elves take turns writing down the number of Calories contained by the various meals, snacks, rations, etc. that they've brought with them, one item per line. Each Elf separates their own inventory from the previous Elf's inventory (if any) by a blank line.

Find the Elf carrying the most Calories. How many total Calories is that Elf carrying?
"""

with open("day_1_input.txt", 'r') as f:
    # Initialize elf and calorie variables
    calories = 0
    elf_calorie_list = []
    for line in f:
        if line.strip() == "":
            elf_calorie_list.append(calories)
            calories = 0
        else:
            calories += int(line)
    total_calories = 0
    for x in range(-3, 0, 1):
        total_calories += sorted(elf_calorie_list)[x]
    print(f"The top three elves have {total_calories} calories")



