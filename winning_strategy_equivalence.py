# Irfansha Shaik, 25.01.2023, Linz.

import argparse
import os

from pysat.formula import CNF
from parse_qdimacs import PaserQDIMACS as pqdimacs



#==========================================================================================

# run qbf solver with assumptions and return the outer most assignment:
# creates a new qdmiacs encoding with assumptions and gets the assignment:
def run_depqbf_solver(k,assm, assertions):
  '''
  flipped_and_assumed_string = parsed_instance.flip_and_assume(k,assm, assertions)
  f = open("intermediate_files/temp_qbf.qdimacs","w")
  f.write(flipped_and_assumed_string)
  f.close()
  #print(k, assm)

  #print(flipped_and_assumed_string)
  result = subprocess.run(['./solvers/depqbf/depqbf', '--qdo', '--no-dynamic-nenofex' , 'intermediate_files/temp_qbf.qdimacs'], stdout=subprocess.PIPE)
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
  '''
  print("TODO")



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
  parser.add_argument("--certificate", help="certificate path (AAG/qdimacs)", default = 'intermediate_files/LN_hein_04_3x3_05_SAT/certificate.aag')
  parser.add_argument("--instance1", help="qbf instance (qdimacs)", default = 'intermediate_files/LN_hein_04_3x3_05_SAT/qbf.qdimacs')
  parser.add_argument("--instance2", help="qbf instance (qdimacs)", default = 'intermediate_files/SN_hein_04_3x3_05_SAT/qbf.qdimacs')
  parser.add_argument("--shared_variables", help="file with a list of variables that are shared with respect to the winning strategy", default = 'intermediate_files/SN_hein_04_3x3_05_SAT/qbf.qdimacs')

  parser.add_argument("-v", help="verbose(0/1) (default 0)", type=int,default = 0)

  args = parser.parse_args()
  print(args)

  
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

  # parse instance1 and instance2
  parsed_instance1 = pqdimacs(args.instance1)
  parsed_instance2 = pqdimacs(args.instance2)


  # parse the same variables in both instances:

  # parse certificate

  # renumber the certificate non-relevant variables:

  # append the certificate to the instance2:

  # check if the second instance is true:
  # for now we are assuming that the both instances are true and have same winning strategy corresponding to the shared variables:

