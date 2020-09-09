import re
import os
import sys
import argparse

class CPerlCompile():
    def __init__(self):
        self.output_file_lines = []
        self.output_file_lines.append("#!/usr/bin/perl\n")
        self.output_file_lines.append("use warnings;\n")
        self.output_file_lines.append("use strict;\n")
        self.output_file_lines.append("\n")
        self.output_file_lines.append("my $argv1 = $ARGV[0];\n")
        self.output_file_lines.append("my $gen_file_buffer = <<END_C_CODE;\n")

    def get_command_line_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-i', dest='input_path',
                            help='REQUIRED: The p3lang file',
                            required=True)
        parser.add_argument('-o', dest='output_file_name',
                            help='Rename the output to <input>.c',
                            nargs='?', type=str, default=None, required=False)
        self.args =  parser.parse_args()
        #self.rcPath = self.args.input_path
        #if self.args.output_file_name is not None:
        #    self.outputFileName = self.args.output_file_name
        return parser.parse_args()

    def should_i_output(self, line):
        if "# vim: set filetype=c:" in line:
            return False
        if line.strip().startswith("{."):
            return False
        if line.strip().startswith(".}"):
            return False
        return True

    def parse_p3lang_file(self, verbose=False):
        self.add_signal_dict = {}
        print(": Opening: ", self.args.input_path)
        add_signal_list = []
        inside_perl_script = False

        with open(self.args.input_path, 'r') as file_object:
            for line in file_object:

                if line.strip().startswith("{."):
                    self.output_file_lines.append("@{[eval{\n")
                    inside_perl_script = True

                if line.strip().startswith(".}"):
                    self.output_file_lines.append("}]}\n")
                    inside_perl_script = False

                if self.should_i_output(line):
#                    re.sub(r'(\n+)(?=[A-Z])', r'\\n', line)
                    if not inside_perl_script: 
                        line = re.sub(r'([\\n]+)(\")', r'\\\\n"', line)

                    self.output_file_lines.append(line)

        self.output_file_lines.append("END_C_CODE\n")


        self.output_file_lines.append("# make sure the file is called: file.c.p3\n")
        self.output_file_lines.append("# file.c.p3 -> file.c\n")
        self.output_file_lines.append("my $foo = substr($0, 0, -3);\n")
        self.output_file_lines.append("open (OUT, \">$foo\") or die \"Unable to open $foo for writing:$!\\n\";\n")
        self.output_file_lines.append("binmode OUT;\n")
        self.output_file_lines.append("print OUT $gen_file_buffer;\n")
        self.output_file_lines.append("close OUT;\n")
        self.output_file_lines.append("__END__\n")
        self.output_file_lines.append("\n")



                    #print(line, end="")
        return self.add_signal_dict

    def save_expanded_file(self):
        with open(self.args.output_file_name, 'w', newline='') as outfile:
#            outfile.write("rc_path,full_signal_path,\n")
            for line in self.output_file_lines:
                outfile.write(line)
#                outfile.write("%s,%s,\n"%(key, signal_path))

if __name__ == '__main__':
    CPerlCompile_inst = CPerlCompile()
    print("Starting")
    CPerlCompile_inst.get_command_line_args()
#    CPerlCompile_inst.get_rc_path_list()
    CPerlCompile_inst.parse_p3lang_file()
#    CPerlCompile_inst.build_full_signal_path_dict()
    CPerlCompile_inst.save_expanded_file()
    print("Finished, exiting now.")

