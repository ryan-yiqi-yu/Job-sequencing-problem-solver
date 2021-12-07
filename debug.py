import solver
from parse import read_input_file, write_output_file


tasks = read_input_file('inputs/small/small-245.in')
output = solver.test(tasks)
print(output)
