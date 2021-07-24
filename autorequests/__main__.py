import argparse
import difflib
from pathlib import Path
from typing import List

from autorequests.classes.outputfile import OutputFile
from .classes import Class, InputFile
from .utils import PathType


class AutoRequests(argparse.ArgumentParser):
    # filepath: PathType
    # filename: str
    # file: File

    def __init__(self):
        super().__init__()
        self.add_argument("-i", "--input", default=None, help="Input Directory")
        self.add_argument("-o", "--output", default=None, help="Output Directory")
        self.add_argument("--return-text", action="store_true",
                          help="Makes the generated method's responses return .text instead of .json()"
                          )
        self.add_argument("--single-quote", action="store_true", help="Uses single quotes instead of double quotes")
        self.add_argument("--no-headers", action="store_true", help="Removes all headers from the operation")
        self.add_argument("--no-cookies", action="store_true", help="Removes all cookies from the operation")
        self.add_argument("--compare", action="store_true",
                          help="Compares the previously generated files to the new files."
                          )
        self.add_argument("--parameters",
                          action="store_true",
                          help="Replaces hardcoded params, json, data, etc with parameters that have default values")
        args = self.parse_args()

        # resolves path
        self.__input = (Path(args.i) if args.input else Path.cwd()).resolve()
        self.__output = (Path(args.o) if args.output else Path.cwd()).resolve()
        self.__single_quote = args.single_quote
        self.__return_text = args.return_text
        self.__no_headers = args.no_headers
        self.__no_cookies = args.no_cookies
        self.__compare = args.compare
        self.__parameters_mode = args.parameters

        # dynamic tings from here on out
        self.__classes = []
        self.__input_files = []
        self.__output_files = []
        self.__has_written = False

    @property
    def input(self) -> PathType:
        return self.__input

    @property
    def output(self) -> PathType:
        return self.__output

    @property
    def single_quote(self) -> bool:
        return self.__single_quote

    @property
    def return_text(self) -> bool:
        return self.__return_text

    @property
    def no_headers(self) -> bool:
        return self.__no_headers

    @property
    def no_cookies(self) -> bool:
        return self.__no_cookies

    @property
    def compare(self) -> bool:
        return self.__compare

    @property
    def parameters_mode(self) -> bool:
        return self.__parameters_mode

    # dynamic

    @property
    def classes(self) -> List[Class]:
        return self.__classes

    @property
    def input_files(self) -> List[InputFile]:
        return self.__input_files

    @property
    def output_files(self) -> List[OutputFile]:
        return self.__output_files

    @property
    def has_written(self):
        return self.__has_written

    def load_local_files(self):
        self.parse_directory(self.input)

    def load_external_files(self):
        for output_file in self.output_files:
            if output_file.class_ and output_file.filepath != output_file.folder:
                if output_file.folder.is_dir():
                    self.parse_directory(output_file.folder)
                else:
                    output_file.folder.mkdir()

    def write(self):
        if self.has_written:
            return

        for output_file in self.output_files:
            # need to check changes before writing again
            if self.compare and output_file.python_file.is_file():
                output_file.write_changes()
            output_file.write()

        self.__has_written = True

    def move_into_class_folder(self):
        for file in self.input_files:
            class_name = file.method.class_name
            if self.output.name != class_name:
                file.rename(self.output / class_name / file.name)

    def print_results(self):
        if len(self.classes) == 0:
            print("No request data could be located.")
            return
        if not self.has_written:
            print("Modules haven't been written to the filesystem yet.")
            return
        num_classes = len(self.classes)
        num_methods = len(self.input_files)
        classes_noun = "classes" if num_classes > 1 else "class"
        methods_noun = "methods" if num_methods > 1 else "method"
        print(f"Successfully wrote {num_classes} {classes_noun} with a total of {num_methods} {methods_noun}.")

    def parse_directory(self, directory: Path):
        if not directory.is_dir():
            return
        for filename in directory.glob("*.txt"):
            file = InputFile(filename)
            method = file.method
            if method:
                class_name = file.method.class_name
                classes_search = [c for c in self.classes if c.name == class_name]

                if not classes_search:
                    class_object = Class(name=class_name,
                                         return_text=self.return_text,
                                         single_quote=self.single_quote,
                                         parameters_mode=self.parameters_mode)
                    self.classes.append(class_object)
                    self.output_files.append(OutputFile(self.output, class_object))
                else:
                    class_object = classes_search[0]

                # needs to be added first
                # modifying methods after adding it to the class is perfectly fine

                class_object.add_method(method)
                self.input_files.append(file)

                # maybe this could be optimized?
                # cpu is wasted calculating headers and cookies only to be deleted
                if self.no_headers:
                    file.method.headers = {}
                if self.no_cookies:
                    file.method.cookies = {}


def main():
    auto_requests = AutoRequests()
    auto_requests.load_local_files()
    auto_requests.load_external_files()
    auto_requests.write()
    auto_requests.move_into_class_folder()
    auto_requests.print_results()


if __name__ == "__main__":
    main()
