# python code style check script
## Introduction
- This script mainly realizes the following functions:
1. **get_changed_files**: this will get files list that contains most recently committed files have changed.
2. **get_all_python_files**: as name denotes, all python files path will be found in this directory.
3. **find_conf_files**: configure file will be found in first two levels of drectorys.
4. **run_pylint**: uses plugins "pylint_json2html" that transforms json (pylint generates) into jsonextended format.
5. **pylint_json2html**: transforms jsonextended format to html.

## Tools
- **Pylint**
  - **Introduction**
    
    Pylint is a Python code analysis tool that analyzes errors in Python code, finds code that does not comply with code style standards (the default code style used by Pylint is PEP 8) and potentially problematic code.
  - **Features**
    1. Pylint is a Python tool. In addition to the functions of ordinary code analysis tools, it provides more functions: such as checking the length of a line of code, whether variable names comply with naming standards, whether a declared interface is actually implemented, etc.
    2. One of the great benefits of Pylint is that it is highly configurable, highly customizable, and it is easy to write small plugins to add functionality.
    3. If you run Pylint twice, it will show both the current and last run results, so you can see if the code quality has improved.
      
- **Pylint_json2html**
  - **Link**: https://pypi.org/project/pylint-json2html/
 
