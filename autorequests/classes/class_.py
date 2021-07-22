from ..utils import format_dict, indent, unique_name, compare_dicts


# "class" is a reserved keyword so I can't name a file "class"


class Class:

    def __init__(self, name: str,
                 return_text: bool = False,
                 single_quote: bool = False,
                 parameters_mode: bool = False):
        self.__name = name
        self.__methods = []
        self.__cookies = {}
        self.__headers = {}

        self.__return_text = return_text
        self.__single_quote = single_quote
        self.__parameters_mode = parameters_mode

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
    def return_text(self):
        return self.__return_text

    @property
    def single_quote(self):
        return self.__single_quote

    @property
    def parameters_mode(self):
        return self.__parameters_mode

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

    @property
    def code(self):
        code = self.signature
        # not actually two newlines; adds \n to end of previous line
        if self.headers or self.cookies:
            code += "\n\n"
            code += indent(self.constructor)
        for method in self.methods:
            code += "\n\n"
            code += indent(method.code)
        code += "\n"
        if self.single_quote:
            # replace unescaped 's with escaped 's
            code = code.replace("'", "\\'")
            # replace escaped "s with escaped 's
            code = code.replace("\\\"", "\\'")
            # replace all "s with 's
            code = code.replace("\"", "'")
        return code

    def add_method(self, method):
        """
        :type method: Method
        """
        method.class_ = self

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
