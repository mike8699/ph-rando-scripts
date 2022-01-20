import sys

from desmume.emulator import DeSmuME

def write_actor(address: int, emu: DeSmuME):
    """Recursively traverse the list of NPCs while writing each to stdout."""
    # Convert the little endian NPC id to big endian so it's easier to read
    data = bytearray(emu.memory.unsigned[address:address+4])
    data.reverse()

    try:
        actor_id = bytes(data).decode('ascii')
        print(f'\n{actor_id}', file=sys.stdout, end='')
    except UnicodeDecodeError:
        return

    # Get the address of the next item in the list and recurse
    next_address = int.from_bytes(emu.memory.unsigned[address+16:address+20], 'little')
    write_actor(next_address, emu)

    

def main(argv: list[str]):
    if len(argv) < 3:
        print(f'Usage: python3 {__file__} <path to rom> <path to savestate>')
        exit(1)

    emu: DeSmuME = DeSmuME()
    emu.open(argv[1])
    emu.savestate.load_file(argv[2])

    base_addr = 0x2069120 # this is hardcoded in the rom's code
    base_addr = int.from_bytes(emu.memory.unsigned[base_addr:base_addr+4], 'little')

    write_actor(base_addr, emu)


if __name__ == '__main__':
    main(sys.argv)
