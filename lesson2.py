"""IF statements check conditions to see if something should be done.  Let's make a variable, and then check if our variable is greater than 0."""

x = 5

if x > 0:
    print(f'X is greater than 0.   X is {x}')  #Here we introduce an f string.  It allows us to enter variables in text by using curly braces.

"""We can check several conditions in a sequence using IF/ELSE statements.  The code will go through each level until it either finds a true statement or comes to the end."""

user_input = int(input("What number do you pick?:  "))  #Remember, reading from right to left, we ask the user for input, convert it to an integer, and assign the value to a variable

if user_input > x:
    print(f'Your number is greater than {x}')
elif user_input < x:
    print(f'Your number is less than {x}')
else:
    print(f'Your number is {x}!')

"""IF is the first check.  ELIF is the next check.  You can have as many ELIF statements as you need, or none.  ELSE is the final catch.
ELSE says that if none of the other statements in this part were true, then do this last thing."""

if 0 <= user_input <= 10:                             #This checks if 0 is less then or equal to user input AND if user input is less than or equal to 10
    print(f'Your answer is between 0 and 10')         #If that is true, it prints this response
else:
    print(f'Your answer is NOT between 0 and 10')     #If it's not true, it prints this response instead.


"""Sometimes we want to group a bunch of code into a package that we can use over and over.  These packages of code are called functions"""

def my_function():          #def means define function, my_function is the name of our function
    print("Hello World")

#When we create a function, nothing happens until we call it in the code.

my_function()

#The parenthesis shows that we are calling a function.  Parenthesis allow for some data to be passed into the function for the function to use.  
#Our print statements have been functions this whole time!

"""Here we call the print funciton with no data for it to use.  It prints a blank line.  Then we give it data, and it prints the data.  Then another blank line.
Then we call our own function.  Our function is not designed to take data, so nothing can go inside the parenthesis when we call it."""

print()
print('Hello')
print()
my_function()
print()

"""let's make a function to add numbers"""

def add(x, y):   #def defines a function, our function is called add, our function takes two variables which we called x and y
    print(x+y)   #Python can automatically do math with INT or FLOAT.  Here we use the automatic addition function in python within our print statement.

a = 3
b = 4

add(a, b)

"""When we made our function, the x and y were just temporary place holders.  They tell python that our function needs 2 things passed into it.  The first thing (which we 
called x) will get used every place that we have x inside the function.  The second thing (which we called y) will get used every place that we have y inside the function.

Since these are just place holders, later on when we call the function we are able to pass in the real variable no matter what it is"""

def math_functions(x, y):
    print(f' {x} + {y} = {x+y}')
    print(f' {x} - {y} = {x-y}')
    print(f' {x} * {y} = {x*y}')
    print(f' {x} / {y} = {x/y}')

math_functions(6, 3)    #Here we passed in integers instead of variables.

#math_functions('this', 'that')

#Notice that if we try to pass strings into this that we get an error called a Traceback

"""Strings can be concatenated, which means added together.  In our math_functions function, when we passed in a string the + worked but we got an error as soon as it tried -"""

"""If we think we might encounter an error (especially with user input), we can use a TRY and EXCEPT block to protect our code and catch the error."""

try:
    math_functions("this", "that")
except TypeError:
    print(f'Please enter an integer!!!')

"""Our exception caught the error and prevented the program from crashing"""