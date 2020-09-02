# Demo of pip, setuptools, CMake and f90wrap

## Prerequisites
C and Fortran compilers. Tested with gcc suite. Some flags are specific to gcc suite. 

## Compilation of the code
```bash
pip install .
```
Note that there is a dot after install.


## Testing the code
Unfortunately even though the code is correctly installed at the correct location, few issues are still pending.

```python
import cylinder  # should work
import cylinder.cyl # will fail
```


## Pending Issues
1. One of the intermediate library is not seamlessly loaded with user intervention. Add the directory of installation to $LD_LIBRARY_PATH.
The directory of the installation can be found from 
```bash
python -c "import cylinder; print(cylinder.__path__)"
```
2. Slight modification of the f90wrap generated cyl.py is required. Open the cyl.py from the path identified in the previous step and change the line containing 
```python
import _cyl 
```
to
```python
import cylinder._cyl as _cyl
```

Now both lines should work
```python
import cylinder  # should work
import cylinder.cyl # should work
```

3. The following code is not properly working because cylinder package is not fully populated with its contents
```python
import cylinder
print(dir(cylinder))
```

## Additional Details
For additional details, refer to https://github.com/jameskermode/f90wrap/tree/master/examples/cylinder.
Replace **Example** in https://github.com/jameskermode/f90wrap/blob/master/examples/cylinder/tests.py with **cylinder.cyl**.
