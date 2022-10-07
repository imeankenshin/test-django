a = input("Enter the number: ")
try:
  print(int(a) * 6)
except ValueError:
  print("ValueError: Enter the number, not String.")
except TypeError:
  print("TypeError")   
