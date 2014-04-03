from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='seeing_in_3d',
      version=version,
      description="Companion code for Seeing chairs in 3D",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='vision graphics 3d models',
      author='Daniel Maturana',
      author_email='dimatura@cmu.edu',
      url='',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
