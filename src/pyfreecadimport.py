import os, sys
import argparse
from pathlib import Path
from turtle import shape

class ImportPart:
    def __init__(self, filename: str, path: str):

        self.filename = filename
        self.path = path
        self.x_coordinate = 0.0
        self.y_coordinate = 0.0
        self.z_coordinate = 0.0
        self.document = FreeCAD.openDocument(filename)
    
    @property
    def verbose(self) -> bool:
        return self.__verbose

    @verbose.setter
    def verbose(self, value) -> None:
        self.__verbose = value

    @property
    def filename(self) -> str:
        return self.__filename

    @filename.setter
    def filename(self, value) -> None:
        if(not value and not os.path.isfile(value)):
            raise Exception("Filename not found or empty -> " + value)
        self.__filename = value

    @property
    def document(self):
        return self.__document

    @document.setter
    def document(self, value):
        self.__document = value

    @property
    def path(self) -> str:
        return self.__path

    @path.setter
    def path(self, value) -> None:
        if(not value):
            raise Exception("Value is empty -> " + value)
        self.__path = value
    
    @property
    def x_coordinate(self) -> float:
        return self.__x_coordinate

    @x_coordinate.setter
    def x_coordinate(self, value):
        if value is None or not isinstance(value, float):
            raise Exception("Value is not a float or empty -> " + str(value))
        self.__x_coordinate = value

    @property
    def y_coordinate(self) -> float:
        return self.__y_coordinate

    @y_coordinate.setter
    def y_coordinate(self, value):
        if value is None or not isinstance(value, float):
            raise Exception("Value is not a float or empty -> " + str(value))
        self.__y_coordinate = value

    @property
    def z_coordinate(self) -> float:
        return self.__z_coordinate

    @z_coordinate.setter
    def z_coordinate(self, value):
        if value is None or not isinstance(value, float):
            raise Exception("Value is not a float or empty -> " + str(value))
        self.__z_coordinate = value

    def add(self):
        if self.verbose:
            print("Adding part with path '%s'" % self.path)
        
        shape = Part.read(self.path)
        obj = self.document.addObject("Part::Feature", "PCB")
        obj.Shape = shape
        
        p = obj.Placement
        p.Base.x += self.x_coordinate
        p.Base.y += self.y_coordinate
        p.Base.z += self.z_coordinate
        obj.Placement = p

        self.document.recompute()
        self.document.save()

def importpart_main(argv):
    filename = Path(__file__).name

    argumentParser = argparse.ArgumentParser()
    argumentParser.add_argument("-f", "--filename", required=True, help="FreeCAD filename *.FCStd")
    argumentParser.add_argument("-p", "--path", required=True, help="Path to file that should be imported in FreeCAD document")
    argumentParser.add_argument("-x", "--x_coordinate", required=False, help="X coordinate for placement")
    argumentParser.add_argument("-y", "--y_coordinate", required=False, help="Y coordinate for placement")
    argumentParser.add_argument("-z", "--z_coordinate", required=False, help="Z coordinate for placement")
    argumentParser.add_argument("-l", "--localization", required=True, help="Path to FreeCAD (FreeCAD.pyd/FreeCAD.so)")
    argumentParser.add_argument("-v", "--verbose", action="store_false", help="Show whats going on")
    
    args = argumentParser.parse_args()

    if(not os.path.exists(args.localization)):
        raise Exception("Localization path not found")
    
    sys.path.append(args.localization)
    
    import FreeCAD
    import Part

    if(args.verbose):
        print(filename, "args=%s" % args)

    importpart = ImportPart(args.filename, args.path)
    importpart.verbose = args.verbose

    if(args.x_coordinate):
        importpart.x_coordinate = float(args.x_coordinate)
    if(args.y_coordinate):
        importpart.y_coordinate = float(args.y_coordinate)
    if(args.z_coordinate):
        importpart.z_coordinate = float(args.z_coordinate)

    importpart.add()

if __name__ == "__main__":
    importpart_main(sys.argv[1:])