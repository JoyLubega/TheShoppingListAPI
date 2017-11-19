"""This module runs all the unittests in the application"""
import os
import nose

if __name__ == "__main__":
    file_path = os.path.abspath(__file__)
    tests_path = os.path.join(os.path.abspath(os.path.dirname(file_path)), "tests")
    result = nose.run(argv=[os.path.abspath(__file__),
                            "--with-cov", "--verbosity=3", "--cover-package=api", tests_path])
