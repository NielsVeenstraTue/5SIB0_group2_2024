import sys
sys.path.append('./EDF')
sys.path.append('./ECF')
sys.path.append('./EDDF')
import EDFtester
import ECFtester
import EDDFtester


def main():
    EDFtester.main()
    ECFtester.main()
    EDDFtester.main()
    return None

if __name__ == "__main__":
    main()