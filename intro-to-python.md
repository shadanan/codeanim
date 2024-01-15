# Introduction

Hello and welcome! In this lecture we’re going to learn how to write our first Python script.

# Creating a Script

Typically, an executable Python program lives in a file, which is often referred to as a script. Let's create a new script called: syntax.py. At the top of this file, we add:

```vscanim
type("#!/usr/bin/env python3")
```

This line indicates to your computer that this is a Python 3 script.

# Print Function

Now, let's do what every programmer does when writing code for the first time! Let's print out "Hello World" to the screen.

To do this, we will use the print function.

```python
print("Hello, world!")
```

The syntax is:

```vscanim
newline()
type("print", return_after=False)
type("(", return_after=False)
type('"', return_after=False)
type("Hello, world!")
```

Notice that we used quotes to surround our Hello World. This is known as a string. And we call the print function using parentheses.

To run our script, we click the play button up here. And then down in the terminal, we can see that Hello World was printed out. Great!

```vscanim
run()
```

Expressions
This code that we wrote on line 3 is called an expression. Let's write an expression that prints out the result of adding 2 + 2.

The syntax is:

```vscanim
clear_canvas()
type("print", return_after=False)
type("(", return_after=False)
type("2 + 2")
```

Notice how we used a plus sign here. This is known as the addition operator.

```vscanim
run()
```

Now, when we run the script again, we see that 4 was printed out. Great!

Variables and the Assignment Operator
Now, let's say that we want to reuse our 2 + 2 expression. We can do this by assigning the result of the expression to a variable, and then print out the result.
result = 2 + 2
print(result)

So:
We create a new variable result
And assign it to 2 + 2
The equal sign here is called the assignment operator.
And then we print out the variable to see its value.
Run the script and we see that 4 was printed out.
You know, it would be clearer if we also printed out the name of the variable. We can do this by passing an additional item separated by a comma.
print("result", result)

So:
We add quote
Result
Then a comma
Notice in this expression that the first argument is a string, because it has quotes around it. And the second value is the variable result, which we created on line 5.
Run, and now we have the name of the variable being printed out.
Exercise
Alright, time for an exercise. Create a variable called city, and assign it to a string that is the city you currently live in. Then print, "I live in [city]". Pause the video and give it a try!
Okay, here's the solution.
Create a variable called city
Set it equal to Seattle
Then Print
Parens
Quote
I live in
Comma
City
Run, and we get I live in Seattle.
Accumulations
A frequently used operator is the += operator, sometimes called the addition assignment operator. Here's an example:
result += 3

Result
+=
3
This operator takes the previous value of a variable, adds the value on the right hand side, and reassigns it back to the variable. In this case, it takes result, which currently has the value 4, adds 3 to it, which gives 7, and reassigns the value back to result.
Running the program, we can see that result is now 7.
Other Operators
In addition to the assignment and addition operators, there are other basic arithmetic operators such as subtraction, multiplication, division, and exponentiation. Let's take a quick look at each of these.
To subtract, use the minus operator:
print(5 - 3)

So, 5 minus 3 equals 2
To multiply, use the asterisk operator:
print(3 \* 3)

So, 3 times 3 equals 9
Division is interesting in Python. There are two division operators. One does regular division:
print(10 / 3)

So, 10 divided by 3 equals 3.3 repeating.
And, the other does integer division:
print(10 // 3)

So, in this case 10 divided by 3 is just equal to 3. Basically, integer division is the floor of normal division.
Related to the division operator is the modulo operator. This operator returns the remainder of a division:
print(10 % 3)

So, 10 modulo 3 equals 1 because when you divide 10 by 3 you get a remainder of 1.
To exponentiate, use the double asterisk operator.
print(5 \*\* 3)

So, here is 5 cubed which is 125.
Exercise
Okay, now for an interesting exercise. Let's use Python to find the roots of the following equation:
x^2 - 8x + 12 = 0
To refresh your memory, the roots of an equation are the values of x where the function is equal to zero. For quadratic equations, we can find the roots using the quadratic formula which is -b +- sqrt(b^2 - 4ac) / 2a. Print out the two roots! Pause the video and give it a try. By the way, you can get the square root by raising a value to the power of 0.5.
a = 1
b = -8
c = 12
x1 = (-b + (b**2 - 4 _ a _ c) ** 0.5) / (2 _ a)
x2 = (-b - (b\*\*2 - 4 _ a _ c) \*\* 0.5) / (2 _ a)
print("x1:", x1, "x2:", x2)

So, we have three variables, a, b, and c.
A equals the coefficient of x squared which is 1
B equals the coefficient of x, which is -8
And C equals 12
Now we say, x1 equals
Parens
-b

- Parens
  b\*\*2

* 4
  Times
  a
  Times
  C
  Raised to
  0.5
  All divided by
  2
  Times
  A
  Next, x2 is the same as x1
  But we replace the + with -
  Then print
  X1, comma
  The value x1
  X2, comma
  The value of x2
  Run, and we see that the roots are 6 and 2. Great!
  Summary
  In this lecture:
  We talked about how to create a new Python script,
  How to use the Print function,
  And we introduced the idea of expressions, strings, variables, and operators.
  Thanks for watching, and see you in the next one!
