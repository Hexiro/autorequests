from . import Method
from ..utils import format_dict, indent, unique_name, compare_dicts


# "class" is a reserved keyword so I can't name a file "class"


class Class:

    def __init__(self, name: str):
        self.__name = name
        self.__methods = []
        self.__cookies = {}
        self.__headers = {}

    @property
    def name(self):
        return self.__name

    @property
    def methods(self):
        return self.__methods

    @property
    def headers(self):
        return self.__headers

    @property
    def cookies(self):
        return self.__cookies

    @property
    def top(self):
        # technically the top of the file and not part of the class :shrug:
        return ("import requests\n"
                "\n"
                "\n"
                "# Automatically generated by https://github.com/Hexiro/autorequests.\n"
                "\n")

    @property
    def signature(self):
        return f"class {self.name}:"

    @property
    def constructor(self):
        signature = "def __init__(self):\n"
        code = "self.session = requests.Session()\n"
        if self.headers:
            code += "self.session.headers.update("
            code += format_dict(self.headers)
            code += ")\n"
        for cookie, value in self.cookies.items():
            code += f"self.session.cookies.set(\"{cookie}\", \"{value}\")\n"
        return signature + indent(code)

    def code(self, return_text: bool = False):
        code = self.top + self.signature
        # not actually two newlines; adds \n to end of previous line
        if self.headers or self.cookies:
            code += "\n\n"
            code += indent(self.constructor)
        for method in self.methods:
            code += "\n\n"
            code += indent(method.code(class_headers=self.headers,
                                       class_cookies=self.cookies,
                                       return_text=return_text))
        code += "\n"
        return code

    def add_method(self, method: Method):

        # there will only ever be one time where there are two methods with the same name,
        # and this right checks that and adds a _one after it
        # the unique_name function on the bottom will add a _two to that one, and so on.

        for old_method in self.methods:
            if old_method.name == method.name:
                old_method.name = old_method.name + "_one"
                break

        # this line showcases 3 instances of 'method.name' LOL
        method.name = unique_name(method.name, [method.name for method in self.methods])
        self.__methods.append(method)
        if len(self.methods) >= 2:
            self.__headers = compare_dicts([method.headers for method in self.methods])
            self.__cookies = compare_dicts([method.cookies for method in self.methods])
