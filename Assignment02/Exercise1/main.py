import math_utils

print("enter radius of circle:")
r = float(input())
area_circle = math_utils.area_of_circle(r)
print(f"Area of circle with radius {r} is {area_circle}")

print("enter length and width of rectangle:")
l = float(input()) 
w = float(input())
area_rectangle = math_utils.area_of_rectangle(l, w)

print(f"Area of rectangle with length {l} and width {w} is {area_rectangle}")
print("enter base and height of triangle:")
b = float(input())
h = float(input())
area_triangle = math_utils.area_of_triangle(b, h)
print(f"Area of triangle with base {b} and height {h} is {area_triangle}")

print(f"Enter side of square:")
s = float(input())
area_square = math_utils.area_of_square(s)
print(f"Area of square with side {s} is {area_square}")


if __name__ == "__main__":
    pass    

