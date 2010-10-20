if __name__=='__main__':
    from timeit import Timer
    t = Timer("test_tabu.set_up()", "import test_tabu")
    #t = Timer('drive_seb', 'import drive_seb')
    print float(t.timeit(number=20)) / 20
