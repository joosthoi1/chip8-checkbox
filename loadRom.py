def loadRom(rom):
    with open(rom, 'rb') as file:
        buff = file.read()
    return ('{:02X}'.format(b) for b in buff)
