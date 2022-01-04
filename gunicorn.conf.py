import multiprocessing

workers = 2 * multiprocessing.cpu_count()
bind = "0:80"
