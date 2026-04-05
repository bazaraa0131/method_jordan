import argparse
from fractions import Fraction

import utils as Utils
import const as Const

def main():

    parser = argparse.ArgumentParser(description="argparse")
    parser.add_argument("--input_file", help="Path to the input file" )
    parser.add_argument("--method", help="Which Gauss-Jordan method to use to transform tables.", required=True)

    parser.add_argument("--redundant_rel", action="store_true", help="Print redundant relations")

    parser.set_defaults(redundant_rel=False)
    args = parser.parse_args()

    if int(args.method) != 1 and int(args.method) != 2:
        print("Гаусс-Жордан нь зөвхөн 1 болон 2 хэмээх аргуудтай.")
        return

    solver = Utils.Solver(args.input_file==None , args.input_file, int(args.method))

    while True:
        solver.visualize()

        if solver.is_rank_fin():
            if solver.is_finished():
                solver.print_relations(args.redundant_rel)
            else:
                if solver.is_solveable():
                    solver.print_relations(args.redundant_rel)
                else:
                    print("Систем тэгшитгэл шийдгүй.")
            break

        while not solver.perform_step():
            continue


if __name__ == "__main__":

    main()




