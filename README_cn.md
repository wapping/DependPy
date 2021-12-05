# 简介

在做python开发的时候，随着日积月累，工程目录下会有很多py脚本，而在部署的时候只需要用到其中一小部分，无关的脚本很多，感觉很不清爽，人为一个一个去筛吧，又很麻烦，有没有工具可以自动把相关的py脚本抽出来呢？如果有，请告诉我！我没有找到，但是仔细想一下好像可以自己实现。

在部署工程的时候，通常有个主程序（py脚本），但可能不光只有主程序，主程序一般会依赖其它模块（我指的是是自己写的py脚本，不是安装的那种）工程稍微大一点就会出现层层依赖，人为去查又很麻烦，怎么自动揪出主程序依赖的脚本呢？

假设有一个工程的目录结构如下

```
.
├── demo_main.py
├── demo_package	
    └── demo_module.py
```

`demo_main.py`是主程序，`demo_package`是一个文件夹，里面包含`demo_module.py`。主程序文件里有一句`from demo_package import demo_module`，也就是说它依赖`demo_module.py`。

执行`python demo_main.py`主程序之后，工程目录下生成一个子目录`__pycache__`，里面有一个.pyc文件，从名字可以看出来是与`demo_module.py`对应的。也就是，执行一个py脚本以后，它所依赖的py脚本会有一个对应的.pyc文件生成。不过主程序`demo_main.py`是没有对应的.pyc文件生成的哦。

```
.
├── demo_main.py
└── demo_package
    ├── __pycache__
    │   └── demo_module.cpython-37.pyc
    └── demo_module.py
```

.pyc文件的位置和命名是有规律的。`__pycache__`和`demo_module.py`在同一个目录下，`demo_module.cpython-37.pyc`和`demo_module.py`前缀相同。

那么，思路就很清晰啦。如果想把一个工程目录的主程序及其相关的py脚本移到一个新的目录，流程如下：

1. 清空工程目录下所有的.pyc文件。清空是为了避免无关.pyc文件的干扰。
2. 执行一下主程序。这时候工程目录下出现的.pyc文件就是与它相关的了。
3. 查找工程目录下生成的.pyc文件。
4. 根据.pyc文件的位置和名称推出py脚本的位置和名称。
5. 把py脚本copy到新的工程目录。
6. 把主程序也复制过去。

经过以上几个步骤，需要的python脚本就全复制到新目录啦。

# 快速开始

要使用这个工具，你得先安装python3，相信你已经安装了，否则应该不需要这个工具。

- 下载本工程

```
git clone https://github.com/wapping/DependPy.git
cd DependPy
```

- 查看或删除.pyc文件

   - 查看项目目录中的所有.pyc文件

   `python find_depend_pyt.py --find your/directory`

   - 删除项目目录中的所有.pyc文件

   `python find_depend_py.py --remove your/directory`

- 找出主程序依赖的脚本

   1. 从项目目录中删除所有 .pyc 文件。
   2. 运行主程序。
   3. 查看项目目录中的所有 .pyc 文件。

- 将主程序相关的脚本复制到新目录

    先找出主程序依赖的脚本（看上一条），然后执行以下命令。
    
     `python find_depend_py.py --copy your/directory new/directory`

