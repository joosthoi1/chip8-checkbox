def ram(kb):
    KB = 1024
    return ["0"]*(KB*kb)


if __name__ == "__main__":
    ram = Ram(1)
    print(ram.ram)
