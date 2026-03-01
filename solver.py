import argparse
from fractions import Fraction

import utils as Utils
import const as Const

def main():

    parser = argparse.ArgumentParser(description="argparse")
    parser.add_argument("--input_file", help="Path to the input file" )
    args = parser.parse_args()

    solver = Utils.Solver(args.input_file==None , args.input_file)
        
    solver.visualize()


if __name__ == "__main__":

    main()




