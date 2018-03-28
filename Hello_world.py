import os
import glob
import sys

HW = "Hello World!" 

def print_HW():
	i = raw_input("To output 'Hello World!' please enter 1.\n")

	if i == "1": 
		print HW
	else:
		print ("Your input did not equal 1\n")
		print_HW()

print_HW()
