from distutils.core import setup
import sys

sys.path.append('phon')
import phon


setup(name='phon',
      version='0.1.0',
      author='Kristoffer Carlsson',
      author_email='kcarlsson89@gmail.com',
      url='https://github.com/KristofferC/phon',
      download_url='https://github.com/KristofferC/phon',
      description='Insertion of cohesive elements between polyhedral grains',
      long_description=open('README.rst').read(),
      packages=['phon', 'phon.io', 'phon.mesh_objects', 'phon.mesh_tools'],
      keywords='neper voronoi mesh cohesive oofem polycrystalline',
      license='The MIT License (MIT)',
      classifiers=['Development Status :: 2 - Pre-Alpha',
                   'Intended Audience :: Developers',
                   'Natural Language :: English',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python :: 2',
                   'Topic :: Scientific/Engineering :: GIS'],
      )
