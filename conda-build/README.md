To build the conda package:
``` bash
conda build purge
conda build -c conda-forge -c bioconda . 1>log 2>&1
anaconda upload ~/miniconda3/conda-bld/noarch/pheri-0.2-0.tar.bz2
```
