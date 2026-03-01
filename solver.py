import argparse

def main():

    parser = argparse.ArgumentParser(
        description="argparse"
    )

    parser.add_argument(
        "--input",
        help="Path to the input file"
    )

    args = parser.parse_args()

    if not parser.input:
        pass



if __name__ == "__main__":

    main()




