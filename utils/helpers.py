def counter(init_val=0, step=1):
    counter_val = init_val
    while True:
        counter_val += step
        yield counter_val
