import random
from PIL import Image
import math
import pyscreenshot as ImageGrab



def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)
        >>> build_random_function(5,7)
        191
    """
    import random

    options2 = {"prod": 2, "avg": 2, "cos_pi": 1,
               "sin_pi": 1}
    options3 = ["prod", "avg", "cos_pi", "sin_pi"]
    options4 = ["x", "y"]

    myChoice = random.choice(options3)
    myNum = options2[myChoice]
    back = [myChoice]
    if(min_depth <= 0):
        if(random.randint(0, max_depth - min_depth) > max_depth-1):

            return random.choice(options4)

    first = build_random_function(min_depth-1, max_depth-1)

    back.append(first)

    if (myNum == 2):
        second = build_random_function(min_depth-1, max_depth-1)
        back.append(second)

    return back


def evaluate_random_function(f, x, y):
    """ Evaluate the random function f with inputs x,y
        Representation of the function f is defined in the assignment writeup

        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value

        >>> evaluate_random_function(["x"],-0.5, 0.75)
        -0.5
        >>> evaluate_random_function(["y"],0.1,0.02)
        0.02
    """
    options = {"prod": "a*b", "avg": "0.5*(a+b)", "cos_pi": "cos(pi*a)",
               "sin_pi": "sin(pi*a)"}
    lastOption = {"x": "x", "y": "y"}
    options2 = {"prod": 2, "avg": 2, "cos_pi": 1,
               "sin_pi": 1}
    if(lastOption.__contains__(f[0])):
        if(f[0] == 'x'):
            return x
        else:
            return y
    else:
        a = evaluate_random_function(f[1], x, y)
        if(options2[f[0]] == 2):
            b = evaluate_random_function(f[2], x, y)
        if(f[0] == "prod"):
            return (a * b)
        elif(f[0] == "avg"):
            return .5 * (a + b)
        elif(f[0] == "cos_pi"):
            return math.cos(math.pi * a)
        elif(f[0] == "sin_pi"):
            return math.sin(math.pi * a)
        else:
            return None

        return exec(options[f[0]])



def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """
    percent = (val - input_interval_start)/(input_interval_end-input_interval_start)
    return output_interval_start + percent * (output_interval_end-output_interval_start)
    pass


def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)


def generate_art(filename, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(5, 6)
    green_function = build_random_function(5, 6)
    blue_function = build_random_function(5, 6)

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                    color_map(evaluate_random_function(red_function, x, y)),
                    color_map(evaluate_random_function(green_function, x, y)),
                    color_map(evaluate_random_function(blue_function, x, y))
                    )

    im.save(filename)


if __name__ == '__main__':
    import doctest
    #doctest.run_docstring_examples(color_map, globals(), verbose=True)
    im = Image.open("agario.png")

    im = ImageGrab.grab()
    im.show()
    pixels = im.load()
    pixels[50, 50] = (0, 255, 0)
    counter = 0
    me = 100
    tot = 0
    x = 0
    y = 0
    last = 0
    x_size, y_size = im.size
    print(x_size)
    print(y_size)
    for i in range(0,y_size-1,5):
        for j in range(0,x_size-1,5):
            r, g, b = pixels[j, i]
            if last < 200 and last == (r + g + b)/3:
                counter += 1
            else:
                if counter > me/5:
                    print(counter)
                    pixels[j - counter * 2.5, i] = (0, 0, 0)
                counter = 0
            last = (r + g + b)/3
        counter = 0

    print(x)
    print(y)
    im.show()



    # Create some computational art!
    # TODO: Un-comment the generate_art function call after you
    #       implement remap_interval and evaluate_random_function
    # generate_art("myart.png")


    # Test that PIL is installed correctly
    # TODO: Comment or remove this function call after testing PIL install
    #test_image("noise.png")
