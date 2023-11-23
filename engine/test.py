import pstats
p = pstats.Stats('C:\Users\there\OneDrive\Documents\Projects\Personal\PythonEngine\git\engine\output.txt')
p.sort_stats('tottime').print_stats(10)