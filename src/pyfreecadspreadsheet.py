import os, sys
import argparse
from pathlib import Path

class SpreadsheetModify:
    def __init__(self, filename: str, spreadsheet: str, alias: str, data: str):

        self.filename = filename
        self.spreadsheet = spreadsheet
        self.alias = alias
        self.data = data
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
    def spreadsheet(self) -> str:
        return self.__spreadsheet

    @spreadsheet.setter
    def spreadsheet(self, value) -> str:
        if(not value):
            raise Exception("Value is empty -> " + value)
        self.__spreadsheet = value

    @property
    def alias(self) -> str:
        return self.__alias

    @alias.setter
    def alias(self, value) -> str:
        if(not value):
            raise Exception("Value is empty -> " + value)
        self.__alias = value

    @property
    def data(self) -> str:
        return self.__data

    @data.setter
    def data(self, value) -> str:
        if(not value):
            raise Exception("Value is empty -> " + value)
        self.__data = value

    def modify(self):
        if self.verbose:
            print("Modifying spreadsheet cell with alias '%s' to value '%s'" %
                (self.alias, self.data))

        spreadsheet = self.document.getObject(self.spreadsheet)

        if not spreadsheet:
            objs = self.document.getObjectsByLabel(self.spreadsheet)

            if not objs:
                raise Exception("Spreadsheet '%s' not found in document" %
                    self.spreadsheet)
            
            spreadsheet = objs[0]
        
        cell = spreadsheet.getCellFromAlias(self.alias)

        if cell:
            spreadsheet.set(cell, self.data)
        else:
            raise Exception("Cell with alias '%s' not found in spreadsheet '%s'" % (self.alias, spreadsheet.Label))
        
        self.document.recompute()
        self.document.save()

def spreadsheet_main(argv):
    filename = Path(__file__).name

    argumentParser = argparse.ArgumentParser()
    argumentParser.add_argument("-f", "--filename", required=True, help="FreeCAD filename *.FCStd")
    argumentParser.add_argument("-s", "--spreadsheet", required=True, help="Name of Spreadsheet object in FreeCAD document")
    argumentParser.add_argument("-a", "--alias", required=True, help="Spreadsheet alias (e.g. Length, Width, Height, etc.)")
    argumentParser.add_argument("-d", "--data", required=True, help="Data to write into the spreadsheet cell")
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

    spreadsheet = SpreadsheetModify(args.filename, args.spreadsheet, args.alias, args.data)
    spreadsheet.verbose = args.verbose
    spreadsheet.modify()

if __name__ == "__main__":
    spreadsheet_main(sys.argv[1:])