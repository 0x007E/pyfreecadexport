import os, sys
import argparse
from pathlib import Path

class RemovePart:
    def __init__(self, filename: str, part: str, name: str):

        self.filename = filename
        self.part = part
        self.name = name
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
    def part(self) -> str:
        return self.__part

    @part.setter
    def part(self, value) -> None:
        if(not value):
            raise Exception("Value is empty -> " + value)
        self.__part = value

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value) -> None:
        if(not value):
            raise Exception("Value is empty -> " + value)
        self.__name = value

    def delete_with_children(self, document, obj):
        for child in list(obj.OutList):
            self.delete_with_children(document, child)
        
        document.removeObject(obj.Name)

    def remove(self):
        if self.verbose:
            print(f"Removing part '{self.part}' with name '{self.name}'")

        targets = []
        for obj in list(self.document.Objects):
            type_id = getattr(obj, "TypeId", None)
            name    = getattr(obj, "Name", None)
            label   = getattr(obj, "Label", None)
            if type_id == self.part and (name == self.name or label == self.name):
                targets.append(obj)
        
        for obj in targets:
            if self.verbose:
                print(f"Removing subtree: {obj.Name} ({obj.Label}) [{obj.TypeId}]")
            self.delete_with_children(self.document, obj)

        self.document.recompute()
        self.document.save()

def removepart_main(argv):
    filename = Path(__file__).name

    argumentParser = argparse.ArgumentParser()
    argumentParser.add_argument("-f", "--filename", required=True, help="FreeCAD filename *.FCStd")
    argumentParser.add_argument("-p", "--part", required=True, help="Part object to remove in FreeCAD document")
    argumentParser.add_argument("-n", "--name", required=True, help="Name/Label of the part to remove")
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

    removepart = RemovePart(args.filename, args.part, args.name)
    removepart.verbose = args.verbose
    removepart.remove()

if __name__ == "__main__":
    removepart_main(sys.argv[1:])