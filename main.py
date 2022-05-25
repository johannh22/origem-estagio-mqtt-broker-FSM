from Modelo import *


def handle_key(obj, key):
    stop = False
    if key == 'o':
        obj.off()
    elif key == 'p':
        obj.on()
    elif key == 'g':
        obj.open_drawer()
    elif key == 'c':
        obj.close_drawer()
    elif key == 'i':
        obj.ignite()
    elif key == 'b':
        obj.ask_for_bat()
    elif key == 's':
        stop = True
    return stop

def main():
    factory = Fabrica()
    supplier = Fornecedor()
    moto = factory.make_moto(supplier)
    # moto.on()
    # moto.open_drawer()
    # moto.ask_for_bat()
    # moto.close_drawer()
    # moto.ignite()
    stop = False
    while not stop:
        action = input(
            f"\n\nCurrent state is '{moto.get_state()}'. Do you want to change state? Press the key then 'enter'\n\
                - 'o' for 'off'\n\
                - 'p' for 'on'\n\
                - 'g' for 'open_drawer'\n\
                - 'c' for 'close_drawer'\n\
                - 'i' for 'ignite'\n\
                - 'b' for 'insert_battery'\n\
                - 's' if you want to stop the program\n\
                - any other key + 'enter' to continue\n\n")
        stop = handle_key(moto, action)

if __name__ == "__main__":
    main()
