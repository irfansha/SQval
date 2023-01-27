# Irfansha Shaik, 25.01.2023, Linz.

import argparse
import os
import textwrap
import random

from pysat.formula import CNF
from pysat.solvers import Minisat22


#==========================================================================================
# Parses matrix lines:
def parse_matrix(matrix_lines):
  # we can merge matrix lines if there are the same quatifier type:
  previous_qtype = ''
  parsed_matrix = []

  for line in matrix_lines:
    # asserting the line is part of matrix:
    assert("exists" in line or "forall" in line)
    # removing spaces
    cleaned_line = line.replace(" ","")
    if ("exists" in cleaned_line):
      cur_var_list = cleaned_line.strip("exists(").strip(")").split(",")
      cur_qtype = 'e'
    else:
      assert("forall" in cleaned_line)
      cur_var_list = cleaned_line.strip("forall(").strip(")").split(",")
      cur_qtype = 'a'

    # changing to integers:
    int_cur_var_list = []

    for var in cur_var_list:
      int_cur_var_list.append(int(var))

    # we are in the same quantifier block:
    if (previous_qtype == cur_qtype):
      parsed_matrix[-1][1].extend(int_cur_var_list)
    else:
      # a tuple of type and the var list:
      parsed_matrix.append((cur_qtype,int_cur_var_list))
      previous_qtype = cur_qtype


  # assert the quantifier are alternating in the parsed_matrix:
  for i in range(len(parsed_matrix)-1):
    assert(parsed_matrix[i][0]!=parsed_matrix[i+1][0])
  return parsed_matrix
#==========================================================================================


#==========================================================================================
# Parse gate lines:
def parse_gates(gate_lines):
  parsed_gate_lines = []
  for line in gate_lines:
    # asserting the line is part of gate:
    assert("or" in line or "and" in line)
    # removing spaces
    cleaned_line = line.replace(" ","")
    if ("or" in cleaned_line):
      # first seperating intermediate gate:
      [cur_gate, cur_list] = cleaned_line.split("=")
      cur_var_list = cur_list.strip("or(").strip(")").split(",")
      # if empty gate, we make the list empty:
      if (cur_var_list == ['']):
        cur_var_list = []
      cur_type = 'or'
    else:
      assert("and" in cleaned_line)
      # first seperating intermediate gate:
      [cur_gate, cur_list] = cleaned_line.split("=")
      cur_var_list = cur_list.strip("and(").strip(")").split(",")
      # if empty gate, we make the list empty:
      if (cur_var_list == ['']):
        cur_var_list = []
      cur_type = 'and'

    parsed_gate_lines.append((cur_type, cur_gate, cur_var_list))
  return parsed_gate_lines



# Reads qcir format:
# Parses matrix lines:
def parse_qcir_format(input_file, verbose):

  f = open(input_file,"r")
  qcir_lines = f.readlines()
  f.close()

  matrix_lines = []
  # cannot be 0, but initializing to 0:
  output_gate = 0
  gate_lines = []

  # seperate matrix, output gate and inner gates:
  for line in qcir_lines:
    # we strip if there are any next lines or empty spaces:
    stripped_line = line.strip("\n").strip(" ")
    # we ignore if comment or empty line:
    if (line == ""):
      continue
    elif(line[0] == "#"):
      continue
    # if exists/forall in the line then it is part of matrix:
    elif ("exists" in stripped_line or "forall" in stripped_line):
      matrix_lines.append(stripped_line)
    elif ("output" in stripped_line):
      output_gate = stripped_line.strip(")").split("(")[-1]
    else:
      gate_lines.append(stripped_line)

  # Parse matrix lines:
  parsed_matrix= parse_matrix(matrix_lines)

  # Parse gate lines:
  parsed_gate_lines = parse_gates(gate_lines)

  if (verbose == 1):
    #print(parsed_matrix)
    for line in parsed_matrix:
      print(line)
    #print(parsed_gate_lines)
    for line in parsed_gate_lines:
      print(line)

  return parsed_matrix, parsed_gate_lines


#==========================================================================================

# takes a list of vars and a model, returns the binary string based on the model:
def get_binary_string(cur_vars, cur_model):
  bin_string = ''
  # getting the values of state vars:
  for var in cur_vars:
    if (int(var) in cur_model):
      bin_string += '1'
    elif (-(int(var)) in cur_model):
      bin_string += '0'
    else:
      print("Error")

  return bin_string


# takes a list of vars and a model, returns the specific assignment for the vars given in the model:
def get_model_assignmet(cur_vars, cur_model):
  assg_lst = []
  # getting the values of vars:
  for var in cur_vars:
    if (int(var) in cur_model):
      assg_lst.append(int(var))
    elif (-(int(var)) in cur_model):
      assg_lst.append(-int(var))
    else:
      print("Error")

  return assg_lst


# runs the sat solver with assumption and returns a model:
def run_sat_solver(m, assm):
  m.solve(assumptions=assm)
  return m.get_model()

def extract_first_player_move(model):
  print("extract move, To do")


# Main:
if __name__ == '__main__':
  text = "Given a QBF, one can interactively play for validation\n both static validation i.e., playing with certificate and dynamic validation i.e., playing with QBF solver are availablec/n handles both ascii-aiger and cnf formats for certificates"
  parser = argparse.ArgumentParser(description=text,formatter_class=argparse.RawTextHelpFormatter)
  parser.add_argument("--certificate", help="certificate path (AIG/qdimacs)", default = 'intermediate_files/LN_hein_04_3x3_05/certificate.aag')
  parser.add_argument("--instance", help="qbf instance (qcir/qdimacs)", default = 'intermediate_files/LN_hein_04_3x3_05/qbf.qcir')
  parser.add_argument("--player", help=textwrap.dedent('''
                                  player type:
                                  user = interactive user play
                                  random = random player, playes random move  (default)'''),default = 'random')
  parser.add_argument("--validation", help=textwrap.dedent('''
                                  validation type:
                                  static = only using certificate (default)
                                  dynamic = only using QBF solver
                                  hybrid = using certificate for first n layers and QBF solver for the rest'''),default = 'static')
  parser.add_argument("--seed", help="seed value for random generater (default 0)", type=int,default = 0)
  parser.add_argument("-v", help="verbose(0/1) (default 0)", type=int,default = 0)

  args = parser.parse_args()
  print(args)

  # Reading the input problem file
  parsed_matrix, parsed_gates = parse_qcir_format(args.instance, args.v)


  if (args.player == 'random'):
    random.seed(args.seed)
    print("Initializing random generator with seed: ", args.seed)


  # checking the first line of the file for the certificate type:
  with open(args.certificate,"r") as f:
    first_line = f.readline()

  if ("cnf" in first_line):
    formula = CNF(from_file=args.certificate)
  else:
    # first converting aiger to cnf:
    cnf_translator_command = "python3 aag_to_dimacs.py --input_file " + args.certificate + " > intermediate_files/translated_cert.cnf"
    os.system(cnf_translator_command)
    formula = CNF(from_file="intermediate_files/translated_cert.cnf")

    #print(formula)

  m = Minisat22(bootstrap_with=formula.clauses)


  # for assumption we remember the moves played
  moves_played_vars = []

  for k in range(len(parsed_matrix)):

    print("quantification layer: ", k)

    # if first player then we extract the assignment:
    if (k%2 == 0):
      assert(args.validation == "static")
      cur_move_model = run_sat_solver(m,moves_played_vars)
      first_player_move = extract_first_player_move(cur_move_model)
      print("\nFirst player assignment:", first_player_move)
      #print(moves_played_vars)
    # if white player (for now user), then we get the move from terminal:
    elif (args.player == 'random'):
      number_of_vars = len(parsed_matrix[k][1])
      # generating a random number with random bits:
      second_player_move = random.getrandbits(number_of_vars)
      # retriving the binary bits from the random number:
      binary_string = format(second_player_move, '0' + str(number_of_vars) + 'b')
      second_player_assignment = []
      # generating random assignment based on the random bits:
      for i in range(number_of_vars):
        if (binary_string[i] == '0'):
          second_player_assignment.append(-parsed_matrix[k][1][i])
        else:
          second_player_assignment.append(parsed_matrix[k][1][i])

      print("Random player plays: ", second_player_assignment)
      # adding the second player assignment to the moves played for later assumptions:
      moves_played_vars.extend(second_player_assignment)
    else:
      second_player_move = input("\nEnter your move: ")
      second_player_assignment = second_player_move.split(" ")
      print(second_player_assignment)

      # adding the second player assignment to the moves played for later assumptions:
      moves_played_vars.extend(second_player_assignment)

