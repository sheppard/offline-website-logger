import subprocess
from setuptools import setup, find_packages

LONG_DESCRIPTION = """
Django REST app to help track page/screen views (and other events) in
offline-capable websites/web-apps/hybrid apps.
"""


def parse_markdown_readme():
    """
    Convert README.md to RST via pandoc, and load into memory
    (fallback to LONG_DESCRIPTION on failure)
    """
    try:
        subprocess.call(
            ['pandoc', '-t', 'rst', '-o', 'README.rst', 'README.md']
        )
    except OSError:
        return LONG_DESCRIPTION

    # Attempt to load output
    try:
        readme = open('README.rst')
    except IOError:
        return LONG_DESCRIPTION
    else:
        return readme.read()

setup(
    name='owl',
    version='0.1.0-dev',
    author='S. Andrew Sheppard',
    author_email='andrew@wq.io',
    url='https://github.com/wq/offline-web-log',
    license='MIT',
    packages=['owl'],
    description=LONG_DESCRIPTION.strip(),
    long_description=parse_markdown_readme(),
    install_requires=[
        'djangorestframework',#>=2.4',
        'djangorestframework-bulk',
        'swapper',
    ],
    classifiers=[
        'Framework :: Django',
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: Log Analysis',
        'Topic :: System :: Logging',
        'Topic :: Scientific/Engineering :: Visualization',
    ],
    test_suite='tests',
#    tests_require=['wq.db'],
)
