import unittest

if __name__ == '__main__':
    testsuite = unittest.TestLoader().discover('./unittests')
    unittest.TextTestRunner(verbosity=2).run(testsuite)
