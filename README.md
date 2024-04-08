[![Version: 0.0.1](https://img.shields.io/badge/Version-0.0.1%20Beta-orange.svg)](https://github.com/0x007e) [![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

# Small Python FreeCAD Export

This python script can be used with command line or as import from another script.

## Parameter

For additional information call:

``` bash
python ./pyfreecadexport.py -h
```

| Short | Expand         | Description                                           |
|-------|----------------|-------------------------------------------------------|
| -h    | --help         | Help menu                                             |
| -f    | --filename     | FreeCAD File *.FCStd                                  |
| -p    | --parttype     | Type of the part(s) to export (e.g. PartDesign::Body) |
| -d    | --directory    | Export Directory                                      |
| -e    | --extension    | Extension of exported file(s) (e.g. .stl,.step)       |
| -l    | --localization | Localization of FreeCAD.pyd                           |
| -v    | --verbose      | Verbose output                                        |

## CLI-Usage

``` bash
# Export to folder: export format: stl
/path/to/freecad/python export.py -f "housing.FCStd" -p "PartDesign::Body" -d "export" -e "stl" -l "path/to/freecad/pyd/bin"

# Export to folder: export format: step
/path/to/freecad/python export.py -f "housing.FCStd" -p "PartDesign::Body" -d "export" -e "step" -l "path/to/freecad/pyd/bin"
```

## Python usage

``` python
sys.path.append("/path/to/freecad/pyd")

partexport = PartExport("/path/to/file.FCStd", "PartDesign::Body")
partexport.export("./temp", ".stl")
```

> Important: The python version to export files has to be the same as the version for FreeCAD.pyd.