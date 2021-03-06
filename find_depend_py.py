# -*- coding: utf-8 -*-
"""
Description : Find dependent python scripts of a python script in a project directory.

Authors     : warpin
CreateDate  : 2021/11/23
"""
import os
import sys
import shutil
from argparse import ArgumentParser


pyc_dir_name = '__pycache__'


def find_pyc_files(dire):
    """Find all .pyc file in the given directory recursively."""
    pyc_files = []
    for file in os.listdir(dire):
        fp = os.path.join(dire, file)
        if os.path.isdir(fp):
            if file == pyc_dir_name:
                pyc = [os.path.join(fp, f) for f in os.listdir(fp) if f.endswith('.pyc')]
                pyc_files += pyc
            else:
                pyc_files += find_pyc_files(fp)
    return pyc_files


def rm_pyc_files(dire):
    """Remove all .pyc file in the given directory recursively."""
    pyc_files = find_pyc_files(dire)
    for fp in pyc_files:
        print(f"Removing {fp}")
        os.remove(fp)
    print(f"{len(pyc_files)} .pyc were removed.")


def find_dependent_py_scripts(dire):
    """Find all dependent .py scripts in the given directory.
    Args:
        dire: The given directory.
    Returns:
        dep_pys: The dependent python scripts.
        miss_pys: There may be some pyc files without corresponding py files.
    Notes: The dependent .py scripts are detected by the corresponding .pyc files.
    """
    pyc_files = find_pyc_files(dire)
    dep_pys = []
    miss_pys = []
    for fp in pyc_files:
        path, name = os.path.split(fp)
        idx = name.find('.cpython')
        if idx < 0:
            miss_pys.append(fp)
            continue

        py_name = name[:idx] + '.py'
        py_dir = os.path.split(path)[0]
        py_fp = os.path.join(py_dir, py_name)
        if not os.path.isfile(py_fp):
            miss_pys.append(fp)
            continue
        dep_pys.append(py_fp)
    return dep_pys, miss_pys


def copy_useful_py_to_dir(src, dst, replace):
    """ Copy useful .py scripts from one directory to another.
    Args:
        src: Source directory.
        dst: Destination directory.
        replace: If replace the destination files.
    """
    useful_pys, miss_pys = find_dependent_py_scripts(src)
    print('='*25 + f'{len(useful_pys)} useful python scripts' + '=' * 25)
    for fp in useful_pys:
        print(fp)

    print('='*25 + f'{len(miss_pys)} missing python scripts' + '=' * 25)
    for fp in miss_pys:
        print(fp)

    if not os.path.isdir(dst):
        os.makedirs(dst)

    abs_src = os.path.abspath(src)
    n_levels = len(abs_src.strip(os.sep).split(os.sep))
    n_succeed, n_fail = 0, 0
    for fp in useful_pys:
        abs_fp = os.path.abspath(fp)
        levels = abs_fp.strip(os.sep).split(os.sep)
        rel_levels = levels[n_levels:]
        n_rel_levels = len(rel_levels)
        src_p = src
        des_p = dst
        for i in range(n_rel_levels):
            src_p = os.path.join(src_p, rel_levels[i])
            des_p = os.path.join(des_p, rel_levels[i])
            if i + 1 >= n_rel_levels:
                if os.path.isfile(des_p):
                    if replace:
                        shutil.copy(src_p, des_p)
                        n_succeed += 1
                        print(f"{des_p} was replaced by {src_p}")
                    else:
                        n_fail += 1
                        print(f"WARNING - {src_p} was blocked by {des_p}")
                else:
                    shutil.copy(src_p, des_p)
                    n_succeed += 1
                    print(f"{src_p} -> {des_p}")
            else:
                if not os.path.isdir(des_p):
                    os.makedirs(des_p)
    print(f"{n_succeed} succeed, {n_fail} failed.")


if __name__ == '__main__':
    parser = ArgumentParser('find_dependent_py')
    parser.add_argument('--find', '-f', type=str, help="Find dependent python scripts in the given directory.")
    parser.add_argument('--remove', '-rm', type=str, help="Remove .pyc files from the given directory recursively.")
    parser.add_argument('--copy', '-c', type=str, nargs='+', help="Copy dependent python scripts from src to dst.")
    parser.add_argument('--replace', '-r', action='store_true', help="If replace the destination files when src and dst have the same name.")
    args = parser.parse_args()

    f, copy, rm = args.find, args.copy, args.remove

    if f is not None:
        if not os.path.isdir(f):
            print(f"ERROR - {f} is not a directory.")
            sys.exit()
        useful_pys, miss_pys = find_dependent_py_scripts(f)
        print('=' * 25 + f'{len(useful_pys)} dependent python scripts' + '=' * 25)
        for fp in useful_pys:
            print(fp)

        print('=' * 25 + f'{len(miss_pys)} missing python scripts' + '=' * 25)
        for fp in miss_pys:
            print(fp)

    if rm is not None:
        if not os.path.isdir(rm):
            print(f"ERROR - {rm} is not a directory.")
            sys.exit()
        rm_pyc_files(rm)

    if copy is not None:
        assert len(copy) == 2, 'The length of --copy must be 2.'
        if not os.path.isdir(copy[0]):
            print(f"ERROR - {copy[0]} is not a directory.")
            sys.exit()
        if not os.path.isdir(copy[1]):
            print(f"ERROR - {copy[1]} is not a directory.")
            sys.exit()
        copy_useful_py_to_dir(copy[0], copy[1], args.replace)
