"""PRINT statements allow many things to be displayed on the terminal.  To open a terminal, press CTRL + ~ or select terminal in the window and select NewTerminal"""

print("Hello World")

"""Notice that using triple quotes make an entire block of stuff into a comment."""  #If you want to comment out just one line, use #

"""Sometimes we want to do something multiple times.  Try printing Hello World 3 times"""

print("Hello World")
print("Hello World")
print("Hello World")

"""This is a lot of typing.  One way to make this easier is to use variables.  A variable is a like a bucket that can hold something that needs to be used multiple times.
Variables are usually declared before they can be used.""" # A variable must start with a letter or _ and is usually lower case.

x = "Hello World"
saying = 'Hello World'
text = 'Hello World'
number = "123"

"""Variable can also hold numbers.  Numbers are either integers INT (which means a whole number), or a float FLOAT (which means a decimanl number)"""

a = 1
num = 3.14

"""A variable could also be a boolean BOOL, which simple means True or False"""

yes = True
no = False

"""Notice that if I put the thing I want to assign inside single quotes or double quotes it is treated like text and NOT like a number or boolean.  Single quotes and double quotes make a STRING"""

"""Let's print Hello World 3 times using a variable.  Since the variable is just a bucket that holds our thing, we don't have to put any special quotes or marks around it"""

print(x)
print(x)
print(x)

"""That's still a LOT of typing the same thing over and over again.  We could use something called a FOR loop to make this easier"""

for i in range(3):
    print(x)  #Make sure each time you indent something that it is 4 spaces.  Indenting means that the indented code belongs inside the code that's over it

"""In this FOR loop, the letter i is just a place holder.  It is a temporary variable that we are just using for this loop. IN tells the for loop where to look
each time it goes through the loop.  RANGE(3) is a special function that let's us tell python what the length of the loop should be.  Notice the : at the end of the line.  This is 
VERY IMPORTANT for ending our lines of code.  VS Code will warn you if you miss a colon where it expects one.  On the next line, we tell python what we want it to do, each time it 
goes through the loop."""

"""We can use multiple variables in our code.  Let's create our own complex FOR loop"""

num_of_times = 3

for _ in range(num_of_times):
    print(x)

"""The _ is just a way to tell python we want a very temporary place holder to ITERATE through the loop.  In our variable, we used _ to join the words that name our variable.  In the FOR 
loop we used it by itself and it changed how python reads the _"""

times = 3

for time in range(times):
    print(x)

"""We can also get user input in python.  When we ask for input, it always gets read as a string STR.  If it should be a number, we have to convert the string to an INT or FLOAT"""

user_text = input("How many times do you want to say Hello?:  (Please enter 1, 2, or 3):  ")
#Our program will pause here while it waits for the user to input an answer

answer = int(user_text)  #Here we convert the user input into an integer

for time in range(answer):
    print(x)

"""All of this can be simplified into one easy line of code"""
user_text = int(input("Please enter the number of times to say Hello (1, 2, 3):  "))

for i in range(user_text):
    print(x)

#You could simplifiy this even more, but it starts to get confusing to someone reading the code
for _ in range(int(input("How many times do you want to do this???: "))):
    print(x)

"""We could also use a WHILE loop to iterate through our code.  """

times = 5   #Sets a variable equal to 5

while times >= 0:  #Checks if our variable is less than or equal to 0
    print(x)
    times -= 1  #Special syntax that subtracts 1 from our variable while it's being used in this WHILE loop

"""Code is read from right to left.  You can update variables by saying 'the new variable' equals 'the old variable' with some change"""
# times = times - 1
# times -= 1
"""Be careful not to use a variable name that is used somewhere else.  The new variable will overwrite the old variable."""

x = "Good Times"
print(x)

"""If we want a variable to be a constant, we usually create the variable in ALL CAPS at the top of our program."""
MY_CONSTANT = "Please don't change me!"