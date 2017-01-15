import shlex
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
from Cython.Build import cythonize


with open('requirements.txt') as fd:
    requirements = [line.rstrip() for line in fd]

with open('test_requirements.txt') as fd:
    test_requirements = [line.rstrip() for line in fd]


class PyTest(TestCommand):

    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = '--cov=outbrain  --ignore=/home/fram/kaggle/outbrain/libs --ignore=/home/fram/kaggle/outbrain/venv'

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)


setup(name='outbrain',
      version='0.0.1',
      author='fram',
      author_email='pavel.sht(gav-gav-gav)yandex.ru',
      install_requires=requirements,
      tests_require=test_requirements,
      cmdclass={'test': PyTest},
      packages=find_packages(),
      scripts=['outbrain/scripts/vw_pipeline_runner.py',
               'outbrain/scripts/generate_train_test.py',
               'outbrain/scripts/csvsort.py',
               'outbrain/scripts/merger.py',
               'outbrain/scripts/evaluate_metrics.py',
               'outbrain/scripts/vw_pipeline_generator.py',
               'outbrain/scripts/preprocess_common.py',
               'outbrain/scripts/filter_categories.py',
               'outbrain/scripts/prepare_log_for_vw.py',
               'outbrain/scripts/apply_vw_model_auto.py',
               'outbrain/scripts/generate_solution.py',
               'outbrain/scripts/replace_missing.py',
               'outbrain/scripts/create_geomapping.py',
               'outbrain/scripts/preprocess_lgbm.py'
               ],
      ext_modules=cythonize("outbrain/*/*.pyx")
)
