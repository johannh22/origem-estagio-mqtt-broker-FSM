from Modelo import *


def main():
    factory = Fabrica()
    supplier = Fornecedor()
    bike = factory.make_moto()
    bike.communicate()  # try with no battery
    bike.ask_for_bat(supplier)
    bike.communicate()


if __name__ == "__main__":
    main()
