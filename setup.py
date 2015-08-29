# -*- coding: utf-8 -*-
'''
Created on 20 Dec. 2014

@author: Mohamed Seghilani
'''

""" How to run the setup file:
see
https://docs.python.org/2/distutils/builtdist.html

python setup.py bdist_wininst # to generate windows installer 

python setup.py bdist_rpm # to generate a "rpm" installer

bdist_egg # to generate a platform ".egg" package 

"""

from setuptools import setup, find_packages

setup(name='opencavity',
      version='0.1',
      description='Optical cavity eigenmode solver',
      url='http://',
      author='Mohamed Seghilani',
      author_email='seghil@gmail.com',
      license='GPLv2',
      packages=['opencavity'],
      package_dir={'opencavity': 'opencavity'},
      package_data={'opencavity': ['Docs\_build\html/*.html','Docs\_build\html\_static/*','Docs\_build\html\_images/*','Docs\_build\html\_sources/*','\Docs\tuto_source/*']},
      #data_files=[('Documents', ['Docs\*.html'])],
      nstall_requires=[
          'numpy','scipy','matplotlib'
      ],
      include_package_data = True,
      zip_safe=False)

