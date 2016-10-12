from setuptools import setup

import sys


# Make sure we have the right Python version.
if sys.version_info[:2] < (2, 7):
    print("Phon requires Python 2.7 or newer. Python %d.%d detected" % sys.version_info[:2])
    sys.exit(-1)

sys.path.append('phon')

setup(name='phon',
      version='0.1.0',
      author='Kristoffer Carlsson',
      author_email='kristoffer.carlsson@chalmers.se',
      url='https://github.com/KristofferC/phon',
      download_url='https://github.com/KristofferC/Phon/tarball/master',
      description='Insertion of cohesive elements between grains in a mesh.',
      long_description=open('README.md').read(),
      packages=['phon', 'phon.io_tools', 'phon.io_tools.read', 'phon.io_tools.write',
                'phon.mesh_objects', 'phon.mesh_tools'],
      keywords='neper voronoi mesh cohesive oofem polycrystalline',
      license='The MIT License (MIT)',
      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Scientific/Engineering',
          'Topic :: Scientific/Engineering :: Mathematics',
          'Topic :: Scientific/Engineering :: Physics',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
      ],
      install_requires=['numpy>=1.9.0']
)
