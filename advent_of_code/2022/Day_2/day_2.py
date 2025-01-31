opponent_total = 0
own_total = 0

"""with open("day_2_input.txt", 'r') as input:
    for line in input:
        opponent = line.strip()[0]
        own = line.strip()[2]
        # Opponent  A = Rock, B = Paper, C = Scissors
        # Points    1 = Rock, 2 = Paper, 3 = Scissors
        # Outcomes  3 > 2, 2 > 1, 1 > 3
        for chr in [('A', 1),('B', 2),('C', 3),]:
            if opponent == chr[0]:
                opponent_val = chr[1]
        # print(f"Opponent used {opponent} with value {opponent_val}")
        # print(f"You used {own} with value {own_val}")

        # Rock and Scissors is a special case, because points for Scissors > Rock,
        # But Rock actually beats Scissors
        # Opponent Chooses Rock (1), You choose Scissors (3)
        if opponent_val == 1 and own_val == 3:
            opponent_total += opponent_val + 6
            own_total += own_val
            # print(f"Opponent Won with {opponent_val + 6} points")
            # print(f"You lost with {own_val} points")
        # Opponent Chooses Scissors (3), You choose Rock (1)
        elif own_val == 1 and opponent_val == 3:
            opponent_total += opponent_val
            own_total += own_val + 6
            # print(f"You Won with {own_val + 6} points")
            # print(f"Opponent lost with {opponent_val} points")

        # Otherwise, if one point value is bigger than the other, it wins
        elif opponent_val > own_val:
            opponent_total += opponent_val + 6
            own_total += own_val
            # print(f"Opponent Won with {opponent_val + 6} points")
            # print(f"You lost with {own_val} points")
        elif own_val > opponent_val:
            opponent_total += opponent_val
            own_total += own_val + 6
            # print(f"You Won with {own_val + 6} points")
            # print(f"Opponent lost with {opponent_val} points")
        # In a tie, each player gets 3 points
        elif own_val == opponent_val:
            opponent_total += opponent_val + 3
            own_total += own_val + 3
            # print(f"It was a tie with {own_val + 3} points")"""

# Rock = A, Paper = B, Scissors = C
# Lose = X, Tie = Y, Win = Z

# Rock = 1, Paper = 2, Scissors = 3
# 3 > 2, 2 > 1, 1 > 3
with open("input_test.txt",'r') as fin:
    for line in fin:
        opponent = line.strip()[0]
        outcome = line.strip()[2]
        # Sets point value based on letter
        for chr in [('A', 1),('B', 2),('C', 3),]:
            if opponent == chr[0]:
                opponent_val = chr[1]
        for chr in [('X', -1),('Y', 0),('Z', 1)]:
            if outcome == chr[0]:
                own_val = opponent_val + chr[1]
                # Make sure values for rock/paper wrap
                if own_val == 0:
                    own_val = 3
                if own_val == 4:
                    own_val = 1


print(f"You scored {own_total} and your opponent scored {opponent_total}!")
            