# Irfansha Shaik, 23.09.2022, Aarhus

# Takes a ascii-aiger format and transforms to dimacs

import argparse

#==========================================================================================

# simply negates the var
def negate_var(var):
    return -1 * var

# divides with 2, and gets the sign from modulo:
def get_var(gate_var):
  var = int(int(gate_var)/2)
  sign = int(gate_var)%2

  if (sign == 0):
    return var
  else:
    return -var


# Main:
if __name__ == '__main__':
  text = "Takes aag file and traslates to dimacs format"
  parser = argparse.ArgumentParser(description=text,formatter_class=argparse.RawTextHelpFormatter)
  parser.add_argument("--input_file", help="input aag file path")
  args = parser.parse_args()

  with open(args.input_file,"r") as f:
    first_line = f.readline()

  header = first_line.strip("\n").split(" ")
  # asserting the input is ascii-aiger format:
  #print(header)
  assert(header[0] == 'aag')

  max_index = int(header[1])


  # no latches:
  assert(header[3] == '0')


  count = int(header[2]) + int(header[4]) + 1


  print("p cnf " + str(max_index) + " " + str(3*int(header[5])))
  line_count = 0

  with open(args.input_file,"r") as f:
    for line in f:
      if (count > 0):
        count = count - 1
        continue
      else:
        #print(line.strip("\n"))
        gate = line.strip("\n").split(" ")
        temp_list = []
        if (gate[1] == '1' and gate[2] == '1'):
          print(str(get_var(gate[0])) + " 0")
          line_count += 1
        elif (gate[1] == '0' and gate[2] == '0'):
          print(str(negate_var(get_var(gate[0]))) + " 0")
          line_count += 1
        else:
          # asserting there is no false input gate:
          assert(gate[1] != '0')
          assert(gate[2] != '0')
          first_input = get_var(gate[1])
          second_input = get_var(gate[2])

          output = get_var(gate[0])

          # if the vars are contradictory, it is false:
          if (first_input ==  negate_var(second_input)):
            print(str(negate_var(output)) + " 0")
            line_count += 1
          else:
            var_list = []
            if (gate[1] != "1"):
              var_list.append(first_input)
            if (gate[2] != "1" and second_input not in var_list):
              var_list.append(second_input)

            # binary clauses:
            for var in var_list:
              print(str(var) + " " + str(negate_var(output)) + " 0")
              line_count += 1
            # long clause:
            temp_list = []
            for var in var_list:
              temp_list.append(negate_var(var))
            temp_list.append(output)
            temp_string = ''
            for var in temp_list:
              temp_string += str(var) + " "
            temp_string += "0"
            print(temp_string)
            line_count += 1


  #print("p cnf " + str(max_index) + " " + str(line_count))

  #==================================================================================
