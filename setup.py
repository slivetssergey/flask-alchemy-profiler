"""
Profiler for Flask and SQLAlchemy
-------------
"""
from setuptools import setup


setup(
    name='Flask-SQLAlchemy-Profiler',
    version='0.0.1',
    url='https://github.com/slivetssergey/flask-alchemy-profiler',
    license='BSD',
    author='RST-IT',
    author_email='slivetssergey@gmail.com',
    description='Profiler for Flask and SQLAlchemy',
    long_description=__doc__,
    packages=['flask_alchemy_profiler', 'flask_alchemy_profiler.templates'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=['SQLAlchemy', 'Flask'],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)