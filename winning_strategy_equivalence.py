# Irfansha Shaik, 25.01.2023, Linz.

import argparse
import os
import subprocess

from pysat.formula import CNF
from parse_qdimacs import PaserQDIMACS as pqdimacs



#==========================================================================================

# run qbf solver with assumptions and return the outer most assignment:
# creates a new qdmiacs encoding with assumptions and gets the assignment:
def run_depqbf_solver():

  #print(flipped_and_assumed_string)
  result = subprocess.run(['./solvers/depqbf/depqbf', 'intermediate_files/appended_instance.qdimacs'], stdout=subprocess.PIPE)
  output = result.stdout.decode('utf-8')
  #print(output)

  output_lines = output.split("\n")

  if ("UNSAT" in output):
    cur_status = "UNSAT"
  else:
    cur_status = "SAT"

  return cur_status



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
  text = "Given two QBFs (qdimacs) Q1 and Q2 and a certificate of Q1 (qdimacs), we check the winning strategy equivalence"
  parser = argparse.ArgumentParser(description=text,formatter_class=argparse.RawTextHelpFormatter)
  parser.add_argument("--certificate", help="certificate path (AAG/qdimacs)", default = 'intermediate_files/hein_04_equivalence/SN_certificate.aag')
  parser.add_argument("--instance1", help="qbf instance (qdimacs)", default = 'intermediate_files/hein_04_equivalence/SN.qdimacs')
  parser.add_argument("--instance2", help="qbf instance (qdimacs)", default = 'intermediate_files/hein_04_equivalence/LN.qdimacs')
  parser.add_argument("--shared_variables", help="file with a list of variables that are shared with respect to the winning strategy", default = 'intermediate_files/hein_04_equivalence/shared_variables.txt')
  parser.add_argument("--status", help=" instance status sat/unsat (default sat)",default = "sat")

  args = parser.parse_args()
  print(args)

  
  # checking the first line of the file for the certificate type:
  with open(args.certificate,"r") as f:
    first_line_cert = f.readline()

  if ("cnf" in first_line_cert):
    certificate_formula = CNF(from_file=args.certificate)
  else:
    # first converting aiger to cnf:
    cnf_translator_command = "python3 aag_to_dimacs.py --input_file " + args.certificate + " > intermediate_files/translated_cert.cnf"
    os.system(cnf_translator_command)
    certificate_formula = CNF(from_file="intermediate_files/translated_cert.cnf")

  # parse instance1 and instance2
  parsed_instance1 = pqdimacs(args.instance1)
  parsed_instance2 = pqdimacs(args.instance2)


  # parse the same variables in both instances:
  # given as a first line separated by spaces:
  with open(args.shared_variables,"r") as f:
    first_line_sv = f.readline()

  shared_vars = first_line_sv.strip("\n").split(" ")
  shared_vars_int = []
  for var in shared_vars:
    shared_vars_int.append(int(var))
  #print(shared_vars_int)
  

  # renumber the certificate non-relevant variables:
  # append the certificate to the instance2:
  parsed_instance2.renumber_and_append_wrf(certificate_formula,shared_vars_int)

  # check if the second instance is true:
  # for now we are assuming that the both instances are true and have same winning strategy corresponding to the shared variables:
  cur_status = run_depqbf_solver()

  is_error = status_print(cur_status, args)
  if (is_error == True):
    print("Formulas are winning strategy NOT equivalent")
  else:
    print("Formulas are winning strategy equivalent")
