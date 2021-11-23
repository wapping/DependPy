# -*- coding: utf-8 -*-
"""
Description : Find dependent python scripts of a python script in a project directory. You need to
1) Run the python script whose dependencies you want to find. This will generate .pyc corresponding to these dependent python scripts.
2) Run this script. You can just view the dependent scripts or copy then to a given directory.

Authors     : warpin
CreateDate  : 2021/11/23
"""
import os
import shutil
from argparse import ArgumentParser


pyc_dir_name = '__pycache__'


def find_pyc_files(dire):
    """Find all .pyc file in the given directory."""
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
    """Remove all .pyc file in the given directory."""
    pyc_files = find_pyc_files(dire)
    for fp in pyc_files:
        os.remove(fp)


def find_useful_py_scripts(dire):
    """Find all dependent .py scripts in the given directory."""
    pyc_files = find_pyc_files(dire)
    useful_pys = []
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
        useful_pys.append(py_fp)
    return useful_pys, miss_pys


def copy_useful_py_to_dir(src, dst, replace):
    """ Copy useful .py scripts from one directory to another.
    Args:
        src: Source directory.
        dst: Destination directory.
        replace: If replace the destination files.
    """
    useful_pys, miss_pys = find_useful_py_scripts(src)
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
                        print(f"{src_p} was blocked by {des_p}")
                else:
                    shutil.copy(src_p, des_p)
                    n_succeed += 1
                    print(f"{src_p} -> {des_p}")
            else:
                if not os.path.isfile(des_p):
                    os.makedirs(des_p)
    print(f"{n_succeed} succeed, {n_fail} failed.")


if __name__ == '__main__':
    parser = ArgumentParser('find_dependent_py')
    parser.add_argument('--dir', '-d', type=str, help="Where to find dependent python scripts.")
    parser.add_argument('--copy', '-c', type=str, nargs='+', help="Copy dependent python scripts from src to dst.")
    parser.add_argument('--replace', '-r', action='store_true', help="If replace the destination files when src and dst have the same name.")
    args = parser.parse_args()

    d, copy = args.dir, args.copy

    if copy is not None:
        assert len(copy) == 2, 'The length of --copy must be 2.'
        copy_useful_py_to_dir(copy[0], copy[1], args.replace)
    else:
        d = d if d is not None else '.'
        useful_pys, miss_pys = find_useful_py_scripts(d)
        print('=' * 25 + f'{len(useful_pys)} useful python scripts' + '=' * 25)
        for fp in useful_pys:
            print(fp)

        print('=' * 25 + f'{len(miss_pys)} missing python scripts' + '=' * 25)
        for fp in miss_pys:
            print(fp)
