from setuptools import setup, find_packages

setup(
    name='quantum-fx',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],  # Add your package dependencies here
    entry_points={
        'console_scripts': [],  # Add console scripts if needed
    },
    author='yaniFitriyani',
    author_email='yanifitriyani02021983@gmail.com',
    description='A package for quantum FX calculations',
    license='MIT',
    url='https://github.com/yanifitriyani02021983-lang/quantum-fx',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)