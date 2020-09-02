# Demo of pip, setuptools, CMake and f90wrap

## Prerequisites
C and Fortran compilers. Tested with gcc suite. Some flags are specific to gcc suite. 

## Compilation of the code
```bash
pip install .
```

## Testing the code
```python
import cylinder.cyl as cyl
```

If the code is compiled and installed properly, the import should work!
For additional details, refer to https://github.com/jameskermode/f90wrap/tree/master/examples/cylinder.
Replace Example in https://github.com/jameskermode/f90wrap/blob/master/examples/cylinder/tests.py with cyl.
