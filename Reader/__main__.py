
if __name__ == "__main__":
    from Reader.get_data import get_data
    from time import time
    tic = time()
    entries = get_data('BuildingPermits/Kitchener.csv')
    toc = time()
    e_time = toc-tic
    print(f'entries took {e_time}s')
