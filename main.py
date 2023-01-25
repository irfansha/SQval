# Irfansha Shaik, 25.01.2023, Linz.

import argparse
import os
import textwrap
import random

from pysat.formula import CNF
from pysat.solvers import Minisat22


def parse(problem_path):
  f = open(problem_path, 'r')
  lines = f.readlines()
  f.close()
  return lines


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

def extract_first_player_move():
  print("extract move, To do")


# Main:
if __name__ == '__main__':
  text = "Given a QBF, one can interactively play for validation\n both static validation i.e., playing with certificate and dynamic validation i.e., playing with QBF solver are availablec/n handles both ascii-aiger and cnf formats for certificates"
  parser = argparse.ArgumentParser(description=text,formatter_class=argparse.RawTextHelpFormatter)
  parser.add_argument("--certificate", help="certificate path", default = 'intermediate_files/certificate.aag')
  parser.add_argument("--instance", help="meta information for game file path", default = 'intermediate_files/instance.qdimacs')
  parser.add_argument("--player", help=textwrap.dedent('''
                                  player type:
                                  user = interactive user play (default)
                                  random = random player, playes random move'''),default = 'user')
  parser.add_argument("--validation", help=textwrap.dedent('''
                                  validation type:
                                  static = only using certificate (default)
                                  dynamic = only using QBF solver
                                  hybrid = using certificate for first n layers and QBF solver for the rest'''),default = 'dynamic')
  parser.add_argument("--seed", help="seed value for random generater (default 0)", type=int,default = 0)

  args = parser.parse_args()
  print(args)

  # generate variables matrix list:
  matrix_vars = []

  # Reading the input problem file
  parsed_instance = parse(args.instance)


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

  for k in range(len(matrix_vars)):

    print("quantification layer: ", k)

    # if first player then we extract the assignment:
    if (k%2 == 0):
      cur_move_model = run_sat_solver(m,moves_played_vars)
      first_player_move = extract_first_player_move(cur_move_model)
      print("\nFirst player assignment:", first_player_move)
      #print(moves_played_vars)
    # if white player (for now user), then we get the move from terminal:
    elif (args.player == "static"):
      second_player_move = input("\nEnter your move: ")
      second_player_move_assignment = second_player_move.split(" ")
      print(second_player_move_assignment)

      # adding the second player assignment to the moves played for later assumptions:
      moves_played_vars.extend(second_player_move_assignment)
    else:
      if (args.player == 'random'):
        # generating a random number with random bits:
        second_player_move = random.getrandbits(len(matrix_vars[k]))
        # retriving the binary bits from the random number:
        binary_string = format(second_player_move, '0' + len(matrix_vars) + 'b')
        second_player_assignment = []
        # generating random assignment based on the random bits:
        for i  in len(matrix_vars[k]):
          if (binary_string[i] == '0'):
            second_player_assignment.append(-matrix_vars[i])
          else:
            second_player_assignment.append(matrix_vars[i])

        print("Random player plays: ", second_player_assignment)
        # adding the second player assignment to the moves played for later assumptions:
        moves_played_vars.extend(second_player_move_assignment)

