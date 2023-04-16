from Run import Run


def __main__():
    poker = Run()
    poker.start()
    while poker.checker_subround_num() != 6:
        poker.run_subround()
        poker.next_subround()


__main__()