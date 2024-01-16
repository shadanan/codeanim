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

The syntax is:

```vscanim
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

# Expressions

This code that we wrote on line 2 is called an expression. Let's write an expression that prints out the result of adding 2 + 2.

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

# Variables and the Assignment Operator

Now, let's say that we want to reuse our 2 + 2 expression. We can do this by assigning the result of the expression to a variable, and then print out the result.

```vscanim
move(lines=-2)
newline()
type("result", return_after=False)
```

So, we create a new variable called result

```vscanim
type(" = 2 + 2", return_after=False)
```

And assign it to 2 + 2. The equal sign here is called the assignment operator.

```vscanim
move(lines=1, cols=-1)
backspace(5)
type("result")
```

And then we print out the variable to see its value.

```vscanim
run()
```

Run the script and we see that 4 was printed out.

You know, it would be clearer if we also printed out the name of the variable. We can do this by passing an additional item separated by a comma.

```vscanim
jump(line=3, col=7)
type('""', return_after=False)
move(cols=-1)
```

So, we add a quote,

```vscanim
type("result", return_after=False)
```

Then result,

```vscanim
move(cols=1)
type(", ")
```

Then a comma to separate the arguments.

Notice in this expression that the first argument is a string, because it has quotes around it. And the second value is the variable result, which we created on line 4.

```vscanim
run()
```

Run, and now we have the name of the variable being printed out.

# Exercise

Alright, time for an exercise. Create a variable called city, and assign it to a string that is the city you currently live in. Then print, "I live in [city]". Pause the video and give it a try!

Okay, here's the solution.

```vscanim
newline()
type("city", return_after=False)
```

Create a variable called city

```vscanim
type(' = "Vancouver"')
```

Set it equal to Vancouver

```vscanim
type("print", return_after=False)
type("(", return_after=False)
type('"I live in"', return_after=False)
type(", ", return_after=False)
type("city")
```

Then print, parens, quote, I live in, comma, city.

```vscanim
run()
```

Run, and we get I live in Vancouver.

```vscanim
clear_canvas(line=5)
```

# Accumulations

A frequently used operator is the `+=` operator, sometimes called the addition assignment operator. Here's an example:

```vscanim
type("result", return_after=False)
```

Result,

```vscanim
type(" += ", return_after=False)
```

Plus-equals,

```vscanim
type("3")
```

3

This operator:

- Takes the previous value of a variable,
- Adds the value on the right hand side,
- And reassigns it back to the variable.

In this case, it takes result, which currently has the value 4, adds 3 to it, which gives 7, and reassigns the value back to result.

```vscanim
type("print(result)")
```

Let's print result.

```vscanim
run()
```

And, running the program, we can see that result is now 7.

# Other Operators

In addition to the assignment and addition operators, there are other basic arithmetic operators such as subtraction, multiplication, division, and exponentiation. Let's take a quick look at each of these.

To subtract, use the minus operator:

```vscanim
clear_canvas()
type("print(5 - 3)")
run()
```

So, 5 minus 3 equals 2

```vscanim
clear_canvas()
type("print(3 * 3)")
run()
```

To multiply, use the asterisk operator:
print(3 \* 3)

So, 3 times 3 equals 9

Division is interesting in Python. There are two division operators. One does regular division:

```vscanim
clear_canvas()
type("print(10 / 3)")
run()
```

So, 10 divided by 3 equals 3.3 repeating.

And, the other does integer division:

```vscanim
clear_canvas()
type("print(10 // 3)")
run()
```

So, in this case 10 divided by 3 is just equal to 3. Basically, integer division is the floor of normal division.

Related to the division operator is the modulo operator. This operator returns the remainder of a division:

```vscanim
clear_canvas()
type("print(10 % 3)")
run()
```

So, 10 modulo 3 equals 1 because when you divide 10 by 3 you get a remainder of 1.

To exponentiate, use the double asterisk operator:

```vscanim
clear_canvas()
type("print(5**3)")
run()
```

So, here is 5 cubed which is 125.

# Exercise

Okay, now for an interesting exercise. Let's use Python to find the roots of the following equation:

x^2 - 8x + 12 = 0

To refresh your memory, the roots of an equation are the values of x where the function is equal to zero. For quadratic equations, we can find the roots using the quadratic formula which is

-b +- sqrt(b^2 - 4ac) / 2a

Print out the two roots! Pause the video and give it a try. By the way, you can get the square root by raising a value to the power of 0.5.

```vscanim roots-exercise
clear_canvas()
type("a = 1")
type("b = -8")
type("c = 12")
```

So, we have three variables, a, b, and c. A equals the coefficient of x squared which is 1, B equals the coefficient of x, which is -8, And C equals 12.

```vscanim
type("r1", return_after=False)      # r1
type(" = (", return_after=False)    # equals parens
type("-b", return_after=False)      # minus b
type(" + (", return_after=False)    # plus parens
type("b**2", return_after=False)    # b squared
type(" - 4", return_after=False)    # minus four
type(" * a", return_after=False)    # times a
type(" * c", return_after=False)    # times c
move(cols=1)
type(" ** 0.5", return_after=False) # raised to the power of a half
move(cols=1)
type(" / ", return_after=False)     # all over
type("(2 * a)")                     # two times a
```

```vscanim
type("r2 = (-b - (b**2 - 4 * a * c) ** 0.5) / (2 * a)")
```

Next, r2 is the same as r1, except we replace the + with a -.

```vscanim
type("print", return_after=False)    # print
type("(", return_after=False)        # parens
type('"r1:", ', return_after=False)  # the label r1, comma
type("r1, ", return_after=False)     # the value of r1
type('"r2:", ', return_after=False)  # the label r2, comma
type("r2")                           # the value of r2
```

```vscanim
run()
```

Run, and we see that the roots are 6 and 2. Great!

# Summary

In this lecture:

- We talked about how to create a new Python script,
- How to use the Print function,
- And we introduced the idea of expressions, strings, variables, and operators.

Thanks for watching, and see you in the next one!
