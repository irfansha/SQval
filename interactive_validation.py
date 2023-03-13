# Irfansha Shaik, 25.01.2023, Linz.

import argparse
import os
import subprocess
import textwrap
import random

from pysat.formula import CNF
from pysat.solvers import Minisat22

from parser_qcir import PaserQCIR as pqcir
from parse_qdimacs import PaserQDIMACS as pqdimacs


#==========================================================================================

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

# run qbf solver with assumptions and return the outer most assignment:
# creates a new qcir encoding with assumptions and gets the assignment:
def run_quabs_solver(k,assm, assertions,temp_qbf_file):
  flipped_and_assumed_string = parsed_instance.flip_and_assume(k,assm, assertions)
  f = open("intermediate_files/temp_qbf.qcir","w")
  f.write(flipped_and_assumed_string)
  f.close()
  #print(k, assm)

  #print(flipped_and_assumed_string)
  result = subprocess.run(['./solvers/quabs/quabs', '--partial-assignment',temp_qbf_file], stdout=subprocess.PIPE)
  output = result.stdout.decode('utf-8')

  int_partial_assignment = []

  #print(output)
  if ("r UNSAT" in output):
    cur_status = "UNSAT"
  else:
    cur_status = "SAT"
  partial_assignment = output.split("\n")[0][2:-2].split(" ")
  # if assignment is given:
  if ("V " in output):
    for var in partial_assignment:
      int_partial_assignment.append(int(var))
  return int_partial_assignment, cur_status


# run qbf solver with assumptions and return the outer most assignment:
# creates a new qdmiacs encoding with assumptions and gets the assignment:
def run_depqbf_solver(k,assm, assertions,temp_qbf_file):
  flipped_and_assumed_string = parsed_instance.flip_and_assume(k,assm, assertions)
  f = open(temp_qbf_file,"w")
  f.write(flipped_and_assumed_string)
  f.close()
  #print(k, assm)

  #print(flipped_and_assumed_string)
  result = subprocess.run(['./solvers/depqbf/depqbf', '--qdo', '--no-dynamic-nenofex' , temp_qbf_file], stdout=subprocess.PIPE)
  output = result.stdout.decode('utf-8')
  #print(output)
  int_partial_assignment = []

  output_lines = output.split("\n")

  if ("s cnf 0" in output):
    cur_status = "UNSAT"
  else:
    cur_status = "SAT"

  for i in range(1,len(output_lines)):
    # making sure that the line is assignment:
    if ('V' in output_lines[i]):
      cur_var = output_lines[i].split(" ")[-2]
      assert(len(output_lines[i].split(" ")) == 3)
      int_partial_assignment.append(int(cur_var))
  return int_partial_assignment, cur_status


# for each variable in the first player move, we check if the assignment is true or false and return the assignment for entire block:
def extract_player_move(model, first_vars):
  cur_assignment = []
  for var in first_vars:
    if (var in model):
      cur_assignment.append(var)
    elif (-var in model):
      cur_assignment.append(-var)
    else:
      # we interpret as open variable, i.e., any assignment would give UNSAT
      # we always take the negation:
      cur_assignment.append(-var)
  return cur_assignment

def status_print(cur_status, args):
 if (cur_status == "SAT"):
    # if the current status is different than the status provided, then it is an error:
    if(args.status == "unsat"):
      print("ERROR: status change in the play from UNSAT -> SAT")
      return True
 else:
    if(args.status == "sat"):
      print("ERROR: status change in the play from SAT -> UNSAT")
      return True

# Main:
if __name__ == '__main__':
  text = "Given a QBF, one can interactively play for validation\n both static validation i.e., playing with certificate and dynamic validation i.e., playing with QBF solver are availablec/n handles both ascii-aiger and cnf formats for certificates"
  parser = argparse.ArgumentParser(description=text,formatter_class=argparse.RawTextHelpFormatter)
  parser.add_argument("--certificate", help="certificate path (AAG/qdimacs)", default = 'intermediate_files/LN_hein_04_3x3_05_SAT/certificate.aag')
  parser.add_argument("--instance", help="qbf instance (qcir/qdimacs)", default = 'intermediate_files/LN_hein_04_3x3_05_SAT/qbf.qcir')
  parser.add_argument("--player", help=textwrap.dedent('''
                                  player type:
                                  user = interactive user play
                                  random = random player, playes random move  (default)'''),default = 'random')
  parser.add_argument("--validation", help=textwrap.dedent('''
                                  validation type:
                                  static = only using certificate (default)
                                  dynamic = only using QBF solver
                                  hybrid = using certificate for first n layers and QBF solver for the rest(TODO)'''),default = 'static')
  parser.add_argument("--hybrid_depth", help="if hybrid validation enable, this depth specifies the swtich from certificate to solver", type=int,default = None)
  parser.add_argument("--assertion_check", help=" assertion check is enabled (1/0) (default 0)", type=int,default = 0)
  parser.add_argument("--assertion_infile", help=" assertions file path",default = 'intermediate_files/LN_hein_04_3x3_05_SAT/assertion.cnf')
  parser.add_argument("--qbf_intermediate_file", help=" path for intermediate qbf file",default = 'intermediate_files/temp_qbf.qdimacs')
  parser.add_argument("--cert_intermediate_file", help=" path for intermediate certificate file",default = 'intermediate_files/translated_cert.cnf')
  parser.add_argument("--status", help=" instance status sat/unsat (default sat)",default = "sat")
  parser.add_argument("--seed", help="seed value for random generater (default 0)", type=int,default = None)
  parser.add_argument("-v", help="verbose(0/1) (default 0)", type=int,default = 0)

  args = parser.parse_args()
  print(args)

  # Reading the input instance file
  # checking the first line of the file for the instance type:
  with open(args.instance,"r") as f:
    first_line = f.readline()

  # for a qdimacs file, the first line is either a comment or preamble:
  if ("c " == first_line[0:2] or "p " == first_line[0:2]):
    parsed_instance = pqdimacs(args.instance)
    instance_type = "qdimacs"
  # else it is a qcir file:
  else:
    parsed_instance = pqcir(args.instance)
    instance_type = "qcir"

  if (args.player == 'random'):
    if args.seed:
        random.seed(args.seed)
        print("Initializing random generator with seed: ", args.seed)

  if (args.validation == "static" or args.validation == "hybrid"):
    # checking the first line of the file for the certificate type:
    with open(args.certificate,"r") as f:
      first_line = f.readline()

    if ("cnf" in first_line):
      formula = CNF(from_file=args.certificate)
    else:
      # first converting aiger to cnf:
      cnf_translator_command = "python3 aag_to_dimacs.py --input_file " + args.certificate + " > " + args.cert_intermediate_file
      os.system(cnf_translator_command)
      formula = CNF(from_file=args.cert_intermediate_file)

    m = Minisat22(bootstrap_with=formula.clauses)


  if (args.assertion_check == 1):

    # we parse the assertions file:
    assertion_formula = CNF(from_file=args.assertion_infile)
    print(assertion_formula.clauses)
  
  # sat certificate, play every second move as an opponent:
  if (args.status == "sat"):
    time_step_modulo = 0
  # else play as first player:
  else:
    time_step_modulo = 1


  # for assumption we remember the moves played
  moves_played_vars = []

  for k in range(len(parsed_instance.parsed_prefix)):

    # if first player then we extract the assignment:
    if (k%2 == time_step_modulo):
      if (args.validation == "static" or (args.validation == "hybrid" and k < args.hybrid_depth)):
        cur_move_model = run_sat_solver(m,moves_played_vars)
        #print(parsed_instance.parsed_prefix[k][1])
        Cert_player_move = extract_player_move(cur_move_model, parsed_instance.parsed_prefix[k][1])
        print("L"+ str(k) + " Cert-player plays:", Cert_player_move)
        # remembering the current assignment for later:
        moves_played_vars.extend(Cert_player_move)
      elif (args.validation == "dynamic" or (args.validation == "hybrid" and k >= args.hybrid_depth)):
        #print(moves_played_vars)
        if (instance_type == "qcir"):
          # we do not have any assertion clauses:
          cur_move_model, cur_status = run_quabs_solver(k,moves_played_vars,[],args.qbf_intermediate_file)
        else:
          # we do not have any assertion clauses:
          cur_move_model, cur_status = run_depqbf_solver(k,moves_played_vars,[],args.qbf_intermediate_file)
        QBF_player_move = extract_player_move(cur_move_model, parsed_instance.parsed_prefix[k][1])
        print("L"+ str(k) + " QBF-player plays: ", QBF_player_move)
        # remembering the current assignment for later:
        moves_played_vars.extend(QBF_player_move)
        is_error = status_print(cur_status, args)
        if (is_error == True):
            break
    # if white player (for now user), then we get the move from terminal:
    elif (args.player == 'random'):
      number_of_vars = len(parsed_instance.parsed_prefix[k][1])
      # generating a random number with random bits:
      second_player_move = random.getrandbits(number_of_vars)
      # retriving the binary bits from the random number:
      binary_string = format(second_player_move, '0' + str(number_of_vars) + 'b')
      second_player_assignment = []
      # generating random assignment based on the random bits:
      for i in range(number_of_vars):
        if (binary_string[i] == '0'):
          second_player_assignment.append(-parsed_instance.parsed_prefix[k][1][i])
        else:
          second_player_assignment.append(parsed_instance.parsed_prefix[k][1][i])

      print("L"+ str(k) + " R-player plays:   ", second_player_assignment)
      # adding the second player assignment to the moves played for later assumptions:
      moves_played_vars.extend(second_player_assignment)
    else:
      second_player_move = input("\nEnter your move: ")
      #print(list(second_player_move))
      second_player_assignment = second_player_move.split(" ")
      #print(second_player_assignment)

      int_second_player_assignment = []
      for var in second_player_assignment:
        if (var == ""):
          continue
        int_second_player_assignment.append(int(var))

      complete_assignment = []
      for var in parsed_instance.parsed_prefix[k][1]:
        if (var in int_second_player_assignment):
          complete_assignment.append(int(var))
        else:
          complete_assignment.append(-int(var))
      print("complete move: ",complete_assignment)

      # adding the second player assignment to the moves played for later assumptions:
      moves_played_vars.extend(complete_assignment)


  # final run to check the status and assertion:
  # we use the qbf solver:
  if (instance_type == "qcir"):
    if (args.assertion_check == 0):
      cur_move_model, cur_status = run_quabs_solver(k,moves_played_vars,[],args.qbf_intermediate_file)
    else:
      cur_move_model, cur_status = run_quabs_solver(k,moves_played_vars,assertion_formula.clauses,args.qbf_intermediate_file)
  else:
    if (args.assertion_check == 0):
      cur_move_model, cur_status = run_depqbf_solver(k,moves_played_vars,[],args.qbf_intermediate_file)
    else:
      cur_move_model, cur_status = run_depqbf_solver(k,moves_played_vars,assertion_formula.clauses,args.qbf_intermediate_file)

  is_error = status_print(cur_status, args)
  if (is_error == True):
    print("Validation failed")
  else:
    print("Validation successful")
    if (args.assertion_check == 1):
      print("Assertion validated")
