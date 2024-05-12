from gooey import Gooey, GooeyParser
import timeseries as ts

def ArguementParser(h):
    return "yes"

@Gooey
def main():
    parser = GooeyParser()
    
    parser.add_argument("num1", action="store")
    parser.add_argument("num2", action="store")

    args = parser.parse_args()
    print(int(args.num1) + int(args.num2))

main()