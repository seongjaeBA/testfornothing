import unittest
import os
os.environ["R_HOME"] = r"C:\Users\seong\anaconda3\lib\R"

from rpy2.robjects import pandas2ri
pandas2ri.activate()


# from rpy2.robjects import tests

# # the verbosity level can be increased if needed
# tr = unittest.TextTestRunner(verbosity = 1)

# suite = tests.suite()
# tr.run(suite)