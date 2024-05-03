# blog-auto-publishing-tools博客自动发布工具
博客自动发布工具，一键把你的博客发到CSDN,简书,掘金,知乎,头条,51blog,腾讯云,阿里云等等

觉得有用的朋友，请给个star! ![Github stars](https://img.shields.io/github/stars/ddean2009/blog-auto-publishing-tools.svg)

# 介绍

在数字化时代，内容创作与传播的速度与广度对于个人或企业品牌的建设至关重要。然而，许多博客作者和内容创作者在发布内容时，面临着跨平台发布的繁琐与不便。每个平台都有其独特的发布规则和操作流程，手动发布不仅耗时耗力，而且容易因为重复劳动而出现错误。为了解决这一痛点，我开发了这款博客自动发布工具。

我的原则就是能自动的，绝不手动。

这款博客自动发布工具，旨在帮助用户实现一键式多平台发布。

用户只需在工具中编写或导入博客内容，选择想要发布的平台（如CSDN、简书、掘金、知乎、头条、51blog、腾讯云、阿里云等），点击发布按钮，即可将内容快速推送到各个平台。

只需要编写好Markdown格式的博客即可，同时能够根据各平台的规则自动调整格式，确保内容在不同平台上的展示效果一致。

# 功能列表

目前支持从浏览器自动发布博客。

因为直接后台接口发布博客比较麻烦，有些博客平台可能有些接口加密的操作，看大家的后续需求反馈，再决定是否实现。

## 从浏览器自动发布

- [x] 支持简书
- [x] 支持cnblogs
- [x] 支持alicloud
- [x] 支持51cto
- [x] 支持infoq
- [x] 支持掘金
- [x] 支持oschina
- [x] 支持segmentfault
- [x] 支持头条
- [x] 支持txcloud
- [x] 支持知乎

目前从浏览器发布博客的方式无法模拟自动上传封面图片。

这是浏览器模拟的限制，目前还没想到解决办法。

## 后台自动发布

TODO

# 支持的浏览器


| 浏览器 | 支持情况 |
| --- |---|
| Chrome | ✔️ |
| Firefox | ❌ |
| Safari | ❌️ |
| Edge | ❌ |
| Internet Explorer | ❌ |

# 使用方法

1. 下载并安装 [Chrome](https://www.google.com/chrome/)。
2. 下载chrome Driver [Chrome Driver](https://googlechromelabs.github.io/chrome-for-testing/)。
3. chrome 以debug模式启动

如果是mac电脑，那么可以先给chrome设置一个alias

```bash
alias chrome="/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome"
```
以debug模式启动

```bash
chrome --remote-debugging-port=9222
```
> !!!! 注意！！！
> chrome启动之后，一定要新开一个空白tab页，或者随便打开一个网站，否则后面的selenium可能会出现假死的情况

在命令行你会看到类似下面的内容：

>DevTools listening on ws://127.0.0.1:9222/devtools/browser/d4d05dd2-5b74-4380-b02d-12baa123445
> 

这行ws很重要，我们把它记下来。

如果你是windows，那么在chrome的快捷方式后面加上 --remote-debugging-port=9222 参数。

![image-20240503190824756](https://flydean-1301049335.cos.ap-guangzhou.myqcloud.com/img/202405031908055.png)



启动chrome，输入chrome://version 检测 --remote-debugging-port=9222 是否出现在页面上。

![image-20240503190854471](https://flydean-1301049335.cos.ap-guangzhou.myqcloud.com/img/202405031908887.png)



然后输入：

> http://localhost:9222/json/version

获得 webSocketDebuggerUrl：



![image-20240503190939248](https://flydean-1301049335.cos.ap-guangzhou.myqcloud.com/img/202405031909990.png)




4. 修改配置文件

修改config/common.yaml 里面的内容：

```yaml
# chrome driver地址
service_location: /Users/wayne/Downloads/work/chromedriver-mac-arm64/chromedriver
# chrome调试地址
debugger_address: localhost:9222/devtools/browser/4aab2b8b-112c-48a3-ba38-12baa123445
```

把service_location和debugger_address修改为你自己本机的配置。

```yaml
enable:
  csdn: True
  jianshu: True
  juejin: True
  segmentfault: True
  oschina: True
  cnblogs: True
  zhihu: True
  cto51: True
  infoq: True
  toutiao: True
  alicloud: True
  txcloud: True
```

这些按照你自己的需求开启。

修改各个平台对应的yaml文件内容。有些平台的配置比较复杂，比如需要配置集合名字，tag名字，标签等等信息。

大家可以参考我的系列教程来进行配置。

或者直接看配置文件，我都写好注释了。直接进行对应的修改即可。

5. 运行程序

安装python依赖：

```python
pip install -r requirements.txt 
```

本工具使用了pandoc  https://www.pandoc.org/  来进行markdown 到html的转化。

有些博客平台不支持markdown格式，所以需要安装pandoc。

如果你的博客平台支持markdown的，可以不需要这个工具。

运行open_all.py 可以自动打开所有的博客网站。

运行publish_all.py 可以自动发布博客内容。

> 切记，在发布博客之前，一定要先保证你的账号是登录状态，否则无法发送博客。





# 系列教程

> 注意，在使用工具之前一定要确保你阅读过下面的教程，更改了必要的配置，否则有可能发布失败。
> 
> 

[一键自动化博客发布工具,用过的人都说好(简书篇)](http://www.flydean.com/blog/projects/001-auto-blog-publish-tool-jianshu/)







