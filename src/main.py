from bb84 import (
    simuler_bb84
)



def main():
    print("=== BB84 with Eve ===")
    simuler_bb84(10000, True,False)

    print("\n=== BB84 without Eve ===")
    simuler_bb84(10000, False,False)

    


if __name__ == "__main__":
    main()