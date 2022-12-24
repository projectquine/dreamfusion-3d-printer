# This is just a mock version of the dreamfusion script to test against

import os, sys, getopt

def main(argv):
   workspace = ''
   text = ''
   iters = ''
   opts, args = getopt.getopt(argv,"hw:t:i:",["workspace=","text=","iters="])
   for opt, arg in opts:
      if opt == '-h':
         print ('df.py -w <inputfile> -t <outputfile> -i <iterations>')
         sys.exit()
      elif opt in ("-w", "--workspace"):
         workspace = arg
      elif opt in ("-t", "--text"):
         text = arg
      elif opt in ("-i", "--iters"):
         iters = arg
   print ('workspace is ', workspace)
   print ('Text input is ', text)
   current_directory = os.getcwd()
   path = os.path.join(current_directory, workspace)
   os.mkdir(path)

if __name__ == "__main__":
   main(sys.argv[1:])
