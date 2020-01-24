
f_x = 1000
f_y = 1100
c_x = 320
c_y = 240

# u = c_x + f_x * X/Z
# v = c_y + f_y * Y/Z
# p1 = (u1, v1)
# p2 = (u2, v2)
# u1 - u2 = (f_x / Z) * (X1 - X2) = 0  
# v1 - v2 = (f_y / Z) * (Y1 - Y2) = f_y / Z
# | p1 - p2 | = sqrt([u1-u2]^2 + [v1-v2]^2) = f_y / Z = 220

Z = f_y / 220
print('Z =', Z)

