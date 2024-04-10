import os, sys
import argparse
from pathlib import Path

class PartExport:
    def __init__(self, filename: str, parttype: str):

        self.filename = filename
        self.parttype = parttype
        self.document = FreeCAD.openDocument(filename)
    
    @property
    def verbose(self) -> bool:
        return self.__verbose

    @verbose.setter
    def verbose(self, value) -> bool:
        self.__verbose = value

    @property
    def filename(self) -> str:
        return self.__filename

    @filename.setter
    def filename(self, value) -> str:
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
    def parttype(self) -> str:
        return self.__parttype

    @parttype.setter
    def parttype(self, value) -> str:
        if(not value):
            raise Exception("Value is empty -> " + value)
        self.__parttype = value

    def export(self, directory: str, extension: str, ):
        if(not os.path.exists(directory)):
            raise Exception("File not found -> " + filename)

        if(not extension):
            raise Exception("Extension is empty")
        
        extension.replace(".", " ")

        for part in self.document.Objects:

            if(part.TypeId == self.parttype):
                if(self.verbose == True):
                    print("Part name/label/type:", part.Name, part.TypeId, part.Label)

                filename = os.path.join(directory, (part.Label + "." + extension))
                Part.export([part], filename)

def partexport_main(argv):
    filename = Path(__file__).name

    argumentParser = argparse.ArgumentParser()
    argumentParser.add_argument("-f", "--filename", required=True, help="FreeCAD filename *.FCStd")
    argumentParser.add_argument("-p", "--parttype", required=True, help="Type of the part(s) to export (e.g. PartDesign::Body)")
    argumentParser.add_argument("-d", "--directory", required=True, help="Directory to export Parts")
    argumentParser.add_argument("-e", "--extension", required=True, help="Extension of exported file(s) (e.g. .stl,.step)")
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

    if(args.directory):
        os.makedirs(args.directory, exist_ok=True)

    partexport = PartExport(args.filename, args.parttype)
    partexport.verbose = args.verbose
    partexport.export(args.directory, args.extension)

if __name__ == "__main__":
    partexport_main(sys.argv[1:])