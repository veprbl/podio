# podio

## Prerequisites

If you are on lxplus, all the necessary software is preinstalled.

On Mac OS or Ubuntu, you need to install the following software. 

### ROOT 6.06

Install ROOT 6.06 and set up your ROOT environment: 

    source <root_path>/bin/thisroot.sh

### Python 2.7

Check the python version by doing:

    python --version

Check that the yaml python module is available

    python
    >>> import yaml

If the import goes fine (no message), you're all set. If not, you need to install yaml. For that, you need to:

1- install the C++ yaml library, which is used by the python module. On Mac OS, The easiest way to do that is to use homebrew (install homebrew if you don't have it yet):

    brew install libyaml

2- install the python yaml module (first install pip if you don't have it yet)

    pip install yaml

Check that you can now import the yaml module in python.


## Preparing the environment

Before building and installing this package, and everytime you need to use it, do:

    source ./init.sh


## Compiling

Set up separate build and install areas, and trigger the build: 

    mkdir build
    mkdir install
    cd build
    cmake -DCMAKE_INSTALL_PREFIX=../install ..
    make -j 4 install

To see a list of options, do this in the build-directory:

    cmake -LH ..

## Running

The examples are for creating a file "example.root",

    ../install/examples/write

reading it again in C++,

    ../install/examples/read

and reading it again in python,

    python ../examples/read.py

## Modifying the data model

Podio features an example event data model, fully described in the yaml file
edm_1.yaml.
The C++ in examples/datamodel/ has been fully generated by a code generation script, python/podio_class_generator.py

To run the code generation script, do

    mkdir ../Tmp
    mkdir ../Tmp/data
    mkdir ../Tmp/src
    python ../python/podio_class_generator.py ../examples/datalayout.yaml ../Tmp data


## Running tests
After compilation you can run rudimentary tests with

    make test

### Unit tests (for developers)

In order to run the unit tests you have to enable them at configuration time with the flag `tests`. Note that GTest is needed. On lxplus the necessary environment is set up with the `init.sh`. On MacOS, you'll have to point cmake to your installation if it is local, see the option in braces below assuming you installed it in `<g_test_path>`.

To configure with unit tests enabled, do:

    cmake -DCMAKE_INSTALL_PREFIX=../install -Dpodio_tests=1 (-DCMAKE_PREFIX_PATH=<g_test_path>/install) ..
    make test

