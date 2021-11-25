# About

This tool can help you find out scripts that a python script depends on in a project.

In python development, as time goes on, there will be many py scripts in the project directory, and only a small part of them are needed when deploying. There are many unrelated scripts, which makes it very uncomfortable. It is troublesome to screen them one by one. Is there any tool that can automatically extract the relevant py scripts? If so, please let me know! 

# Quick start

To use this tool, you just need python3.

- Clone the repository

```
git clone https://github.com/wapping/DependPy.git
cd DependPy
```

- View and remove .pyc

   When running a python script, there will be .pyc files generated corresponding to the python scripts it depends on.

   - View all .pyc files in your project directory.

   `python find_depend_pyt.py --find your/directory`

   - Remove all .pyc files from your project directory.

   `python find_depend_py.py --remove your/directory`

- Find out scripts that the main program depends on in a project.

   1. Remove all .pyc files from your project directory.

   2. Run the main program

   3. View all .pyc files in your project directory.

- Copy the relevant scripts of the main program to a new directory

   Find out scripts that the main program depends on first, and then execute the following command.
   
   `python find_depend_py.py --copy your/directory new/directory`
