# Irfansha Shaik, 29.01.2023, Linz.

class PaserQDIMACS:
  #==========================================================================================
  # Parses prefix lines:
  def parse_prefix(self,prefix_lines):
    # we can merge prefix lines if there are the same quatifier type:
    previous_qtype = ''

    for line in prefix_lines:
      # asserting the line is part of prefix:
      assert("e " in line or "a " in line)
      # removing spaces
      cur_qtype = line[0]
      cur_var_list = line[2:].split(" ")[:-1]
      #print(cur_var_list)

      # changing to integers:
      int_cur_var_list = []

      for var in cur_var_list:
        int_cur_var_list.append(int(var))
        # adding input gates to all gates:
        if (int(var) not in self.all_vars):
          self.all_vars.append(int(var))

      # we are in the same quantifier block:
      if (previous_qtype == cur_qtype):
        self.parsed_prefix[-1][1].extend(int_cur_var_list)
      else:
        # a tuple of type and the var list:
        self.parsed_prefix.append((cur_qtype,int_cur_var_list))
        previous_qtype = cur_qtype

      #print((cur_qtype,int_cur_var_list))

    # assert the quantifier are alternating in the parsed_prefix:
    for i in range(len(self.parsed_prefix)-1):
      assert(self.parsed_prefix[i][0]!=self.parsed_prefix[i+1][0])
  #==========================================================================================



  # Reads qdimacs format:
  # Parses prefix lines:
  def parse_qdimacs_format(self):

    f = open(self.input_file,"r")
    lines = f.readlines()
    f.close()

    prefix_lines = []

    # seperate prefix, output gate and inner gates:
    for line in lines:
      #print(line)
      # we strip if there are any next lines or empty spaces:
      stripped_line = line.strip("\n").strip(" ")
      # we ignore if comment or empty line:
      if (line == ""):
        continue
      elif(line[0] == "c"):
        continue
      elif(line[0] == "p"):
        self.preamble = stripped_line.split(" ")
      # if exists/forall in the line then it is part of prefix:
      elif ("e " in stripped_line or "a " in stripped_line):
        prefix_lines.append(stripped_line)
      else:
        self.clauses.append(stripped_line)

    #print(prefix_lines)

    # Parse prefix lines:
    self.parse_prefix(prefix_lines)

  # we flip universal layers in first k layers and add assumption TODO:
  def flip_and_assume(self, k, assum):

    flipped_and_assumed_string = ''

    # printing preamble:
    flipped_and_assumed_string += " ".join(self.preamble[:-1]) + " " +str(int(self.preamble[-1]) + len(assum)) + "\n"

    first_layers = ""
    for i in range(len(self.parsed_prefix)):
      layer_string = " ".join(str(x) for x in self.parsed_prefix[i][1])
      if i < k:
        first_layers += " " + layer_string
      elif (self.parsed_prefix[i][0] == "e"):
        # we merge the first layer:
        if(i == k):
          flipped_and_assumed_string += "e " + layer_string + " 0\n"
        else:
          flipped_and_assumed_string += "e " + layer_string + " 0\n"
      else:
        flipped_and_assumed_string += "a " + layer_string + " 0\n"

    # appending the flipping at the end:
    flipped_and_assumed_string += "e " + first_layers + " 0\n"
    

    # adding assumption clauses:
    for var in assum:
      flipped_and_assumed_string += str(var) + " 0\n"


    # printing all the gates to the file:
    for line in self.clauses:
      flipped_and_assumed_string += line + "\n"


    return flipped_and_assumed_string


  # assuming no open variables:
  def __init__(self, input_qbf):
    self.input_file = input_qbf
    self.preamble = []
    self.parsed_prefix = []
    self.clauses = []
    # remembering all gates for future assumptions:
    self.all_vars = []

    self.parse_qdimacs_format()

    #print(self.parsed_prefix)



