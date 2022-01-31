<h1 align=center>AutoRequests</h1>
<p align=center>
  <span>Automatically create a simple Python API wrapper from request data generated by your browser</span>
  <br>

  <a title="PyPI - Version" href="https://pypi.org/project/autorequests/" target="_blank">
    <img src="https://img.shields.io/pypi/v/autorequests?color=390099&style=for-the-badge"/>
  </a>

  <a title="PyPI - Python Version" href="https://www.python.org/downloads/" target="_blank">
     <img src="https://img.shields.io/pypi/pyversions/autorequests?color=B80068&style=for-the-badge&logo=python&logoColor=fff"/>
  </a>

  <a title="License - MIT" href="LICENSE" target="_blank">
    <img src="https://img.shields.io/github/license/Hexiro/autorequests?style=for-the-badge&color=390099&labelColor=474747">
  </a>

  <img alt="GitHub Workflow Status" src="https://img.shields.io/github/workflow/status/Hexiro/autorequests/tests?logo=github&style=for-the-badge&label=tests">
  <br>
</p>

### 📺 Demo

<img alt="Demo" src="https://user-images.githubusercontent.com/42787085/137994635-cadbafad-4371-4c22-892a-7e9a82785c56.gif"/>

### 💼 Example Use Cases

* Creating a foundation for an API wrapper
* Recreating a request outside the browser
* Testing what cookies or headers are required for a server to understand your request

### ✂️ How to Copy

1. Inspect Element
2. Go to `Network` tab
3. Find web request
4. Right-Click
5. Copy
6. Choose one of the following:
    1. Powershell
    2. Node.js fetch

## 📦 Installation

install the package with pip

```
$ pip install autorequests
```

or download the latest development build from GitHub

```
$ pip install -U git+https://github.com/Hexiro/autorequests
```

## 🖥️ Command Line

```console
$ autorequests --help
```

directory options

```console
  -i, --input           Input Directory
  -o, --output          Output Directory
```

generation options

```
  --return-text         Makes the generated method's responses return .text instead of .json()
  --no-headers          Removes all headers from the operation
  --no-cookies          Removes all cookies from the operation
  --parameters          Replaces hardcoded params, json, data, etc with parameters that have default values
```

## 🚩 Known Issues

* Method names are parsed from the url, but if the URL doesn't have any paths with a valid method name, an invalid
  method name will be used.
* Sometimes when copying from the browser, important headers aren't included which causes the resulting API wrapper to
  fail requests.
* Parsing multipart/form-data when copying with the powershell mode isn't supported

## 🐞 Contributing

see [CONTRIBUTING.md](./CONTRIBUTING.md)

## 📅 # TODO

* better unit test coverage
* more cli options
* better cli output
* better input files
* AST / better code generation