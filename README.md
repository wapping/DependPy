检测一个python脚本依赖的python脚本，听起来有点绕，先说一下背景吧。

在做python开发的时候，随着日积月累，工程目录下会有很多py脚本，而在部署的时候只需要用到其中一小部分，无关的脚本很多，感觉很不清爽，人为一个一个去筛吧，又很麻烦，有没有工具可以自动把相关的py脚本抽出来呢？如果有，请告诉我！我没有找到，但是仔细想一下好像可以自己实现。

在部署工程的时候，通常有个主程序（py脚本），但光有主程序还不够，主程序一般会依赖其它模块，有些是自己写的py脚本，工程稍微大一点就会出现层层依赖，人为去查又很麻烦，文章标题的意思就是，怎么自动揪出主程序依赖的脚本呢？

要揪出来的是那些自己开发的脚本（或者是搬运过来的），反正不是那些安装的模块。因为安装的模块不需要找，部署的时候自然会安装。

假设有一个工程的目录结构如下

```
.
├── demo_main.py
├── demo_package	
    └── demo_module.py
```

`demo_main.py`是主程序，`demo_package`是一个文件夹，里面包含`demo_module.py`。主程序文件里有一句`from demo_package import demo_module`，它依赖`demo_module.py`。

`python demo_module.py`执行主程序之后，工程目录下生成一个子目录`__pycache__`，里面有一个.pyc文件，从名字可以看出来是与`demo_module.py`对应的。也就是，执行一个py脚本以后，它所依赖的py脚本会有一个对应的.pyc文件生成。

```
.
├── demo_main.py
└── demo_package
    ├── __pycache__
    │   └── demo_module.cpython-37.pyc
    └── demo_module.py
```

而且，.pyc文件的位置和命名是有规律的。`__pycache__`和`demo_module.py`在同一个目录下，`demo_module.cpython-37.pyc`和`demo_module.py`前缀相同。

那么，思路就有了：

1. 执行一下主程序
2. 找到工程目录下生成的.pyc文件
3. 根据.pyc文件的位置和名称推出py脚本的位置和名称
4. 把py脚本copy到新的工程目录
5. 把主程序也复制过去

这样，需要的py脚本就全复制到新目录了，再把其它相关文件复制过去，干净清新的新工程就诞生了。