export PATH=/afs/cern.ch/sw/lcg/contrib/CMake/2.8.9/Linux-i386/bin:${PATH}
source /afs/cern.ch/sw/lcg/contrib/gcc/4.8.1/x86_64-slc6/setup.sh
source /afs/cern.ch/sw/lcg/app/releases/ROOT/6.02.08/x86_64-slc6-gcc48-opt/root/bin/thisroot.sh

export PODIOHOME=$PWD/install
export LD_LIBRARY_PATH=$PODIO/examples:$PODIOHOME/lib:$LD_LIBRARY_PATH
export PYTHONPATH=$PODIOHOME/examples:$PYTHONPATH
