from Run import Run


def __main__():
    poker = Run()
    poker.start()
    while True:
        while True:
            poker.run_subround()
            poker.next_subround()


__main__()