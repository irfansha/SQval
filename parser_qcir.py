# Irfansha Shaik, 28.01.2023, Linz.

class PaserQCIR:
  #==========================================================================================
  # Parses matrix lines:
  def parse_matrix(self,matrix_lines):
    # we can merge matrix lines if there are the same quatifier type:
    previous_qtype = ''

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
        # adding input gates to all gates:
        if (int(var) not in self.all_gates):
          self.all_gates.append(int(var))


      # we are in the same quantifier block:
      if (previous_qtype == cur_qtype):
        self.parsed_matrix[-1][1].extend(int_cur_var_list)
      else:
        # a tuple of type and the var list:
        self.parsed_matrix.append((cur_qtype,int_cur_var_list))
        previous_qtype = cur_qtype


    # assert the quantifier are alternating in the parsed_matrix:
    for i in range(len(self.parsed_matrix)-1):
      assert(self.parsed_matrix[i][0]!=self.parsed_matrix[i+1][0])
  #==========================================================================================


  #==========================================================================================
  # Parse gate lines:
  def parse_gates(self,gate_lines):
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
      # all gates:
      if (int(cur_gate) not in self.all_gates):
        self.all_gates.append(int(cur_gate))
      self.parsed_gates.append((cur_type, cur_gate, cur_var_list))



  # Reads qcir format:
  # Parses matrix lines:
  def parse_qcir_format(self):

    f = open(self.input_file,"r")
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
        self.output_gate = int(stripped_line.strip(")").split("(")[-1])
      else:
        gate_lines.append(stripped_line)

    # Parse matrix lines:
    self.parse_matrix(matrix_lines)

    # Parse gate lines:
    self.parse_gates(gate_lines)

  # we flip universal layers in first k layers and add assumption as a new intermediate gate:
  def flip_and_assume(self, k, assum):

    flipped_and_assumed_string = ''

    for i in range(len(self.parsed_matrix)):
      layer_string = ",".join(str(x) for x in self.parsed_matrix[i][1])
      if i < k:
        flipped_and_assumed_string += "exists(" + layer_string + ")\n"
      elif (self.parsed_matrix[i][0] == "e"):
        flipped_and_assumed_string += "exists(" + layer_string + ")\n"
      else:
        flipped_and_assumed_string += "forall(" + layer_string + ")\n"

    # new output gate, assert it is not in the existing gates:
    new_output_gate = self.output_gate + 1
    assert(new_output_gate not in self.all_gates)
    flipped_and_assumed_string += "output(" + str(new_output_gate) + ")\n"

    # printing all the gates to the file:
    for line in self.parsed_gates:
      flipped_and_assumed_string += line[1] + "=" + line[0] + "(" + ",".join(line[2]) + ")\n"


    # new output gate, with assumptions + self.output_gate:
    temp_assum = list(assum)
    temp_assum.append(self.output_gate)
    flipped_and_assumed_string += str(new_output_gate) + "=and(" + ",".join(str(x) for x in temp_assum) + ")"

    return flipped_and_assumed_string



  def __init__(self, input_qbf):
    self.input_file = input_qbf
    self.parsed_matrix = []
    self.parsed_gates = []
    # remembering all gates for future assumptions:
    self.all_gates = []
    # initialising to 0, cannot be 0 at the end:
    self.output_gate = 0

    self.parse_qcir_format()



