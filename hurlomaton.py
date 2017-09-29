"""
Main Hurlomaton python program
- launches the slideshow
- listen to the GPIO number ###
- if the GPIO is True for two seconds...
    - launches the spots on GPIO ###
    - wait 0.5s
    - captures an image
    - shows success screens
        - screen 1: Well done!
        - screen 2: The picture
        - sreeen 3: Thank you!
"""

# fact = 1
# num = int(input("Enter any number: "))
# for i in range(1, num+1, 1):
#     fact = fact * i
# print("The fact of", num, "is", fact)

num = int(input("Enter any number: "))
i = 1
fact = 1

while i <= num:
    fact = fact  * i
    i = i + 1
 print("The fact of", num, "is", fact)
