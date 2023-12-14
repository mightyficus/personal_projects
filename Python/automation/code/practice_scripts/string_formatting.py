data = [
    (1000, 10),
    (200, 17),
    (2500, 170),
    (2500, -170),
]

# Print the header
print("REVENUE | PROFIT | PERCENT")

# Template aligns and displays the data in the proper format
TEMPLATE = '{revenue:>7,} | {profit:>+6} | {percent:>7.2%}'

# Print the data rows
for revenue, profit in data:
    row = TEMPLATE.format(revenue=revenue, profit=profit, percent=profit / revenue)
    print(row)

# A good place to find documentation on string formatting is https://pyformat.info