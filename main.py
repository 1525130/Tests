import unittest

from utils.result import HTMLTestResult, MarkdownTestResult

unittest.TextTestRunner(descriptions=False, verbosity=2, resultclass=HTMLTestResult).run(unittest.TestSuite([
    # add your TestLoader here
    unittest.defaultTestLoader.discover('demo'),
    # unittest.defaultTestLoader.loadTestsFromTestCase(),
    # ...
]))
