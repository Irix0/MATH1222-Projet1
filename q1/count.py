import numpy as np

input = "abbbabcabcbcbdababbcacacbdacbacbbbdabdabbabacabbabdabdacbababbcacbabcbcacbcbabdacbbbbacbabbdacababcacbdabbbacbdacbcbdacbdababcbdacbabacabcabcbcababbcbababbcabcbdacbcacbdacbdacacabbdacabdabbababcababbdabcbabbabcabcbababbabbdacabbbdabbbabacabacacbbdabdabcbbbcabbdacabababbbbcbdabdacabdacabbbabacacbbbdacabcbdabcbacbbcbbbacacabbdababcbbcbbdacbdacabdacbababcacbdacbabdabbbacbababbdababbcacbcabdabdabcbdacbbdacbcbbbabdabbbbcabcbcbdabbcbabbabacabdabacbbabbcbdababacabcabbabdacbdababdabcacbbabacbabdabcabdac"

# Count the number of times we switch from a to a, a to b, from a to c, from a to d, etc.
a=0
b=0
c=0
d=0

a_to_a = 0
a_to_b = 0
a_to_c = 0
a_to_d = 0

b_to_a = 0
b_to_b = 0
b_to_c = 0
b_to_d = 0

c_to_a = 0
c_to_b = 0
c_to_c = 0
c_to_d = 0

d_to_a = 0
d_to_b = 0
d_to_c = 0
d_to_d = 0

# Iterate through the string
for i in range(len(input) - 1):
      if input[i] == "a":
         a += 1
         if input[i + 1] == "a":
               a_to_a += 1
         elif input[i + 1] == "b":
               a_to_b += 1
         elif input[i + 1] == "c":
               a_to_c += 1
         elif input[i + 1] == "d":
               a_to_d += 1
      elif input[i] == "b":
         b += 1
         if input[i + 1] == "a":
               b_to_a += 1
         elif input[i + 1] == "b":
               b_to_b += 1
         elif input[i + 1] == "c":
               b_to_c += 1
         elif input[i + 1] == "d":
               b_to_d += 1
      elif input[i] == "c":
         c += 1
         if input[i + 1] == "a":
               c_to_a += 1
         elif input[i + 1] == "b":
               c_to_b += 1
         elif input[i + 1] == "c":
               c_to_c += 1
         elif input[i + 1] == "d":
               c_to_d += 1
      elif input[i] == "d":
         d += 1
         if input[i + 1] == "a":
               d_to_a += 1
         elif input[i + 1] == "b":
               d_to_b += 1
         elif input[i + 1] == "c":
               d_to_c += 1
         elif input[i + 1] == "d":
               d_to_d += 1

# Divide the number of times we switch from a to a, a to b, etc. by the number of times we start with a, b, c, or d, respectively.
a_to_a = a_to_a / a
a_to_b = a_to_b / a
a_to_c = a_to_c / a
a_to_d = a_to_d / a

b_to_a = b_to_a / b
b_to_b = b_to_b / b
b_to_c = b_to_c / b
b_to_d = b_to_d / b

c_to_a = c_to_a / c
c_to_b = c_to_b / c
c_to_c = c_to_c / c
c_to_d = c_to_d / c

d_to_a = d_to_a / d
d_to_b = d_to_b / d
d_to_c = d_to_c / d
d_to_d = d_to_d / d

# Put the results into a numpy matrix
transition_matrix = np.array([[a_to_a, a_to_b, a_to_c, a_to_d], [b_to_a, b_to_b, b_to_c, b_to_d], [c_to_a, c_to_b, c_to_c, c_to_d], [d_to_a, d_to_b, d_to_c, d_to_d]])

# Print the results
print(transition_matrix)