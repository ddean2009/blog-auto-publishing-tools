- [blog-auto-publishing-tools博客自动发布工具](#blog-auto-publishing-tools博客自动发布工具)
- [介绍](#介绍)
- [功能列表](#功能列表)
  - [从浏览器自动发布](#从浏览器自动发布)
  - [后台自动发布](#后台自动发布)
- [支持的浏览器](#支持的浏览器)
- [使用方法](#使用方法)
  - [使用chrome](#使用chrome)
  - [使用firefox](#使用firefox)
  - [设置封面](#设置封面)
  - [其他配置](#其他配置)
  - [运行程序](#运行程序)
- [系列教程](#系列教程)


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

> 好消息！！！！
> 最新版本 在某些博客平台已经可以模拟自动上传封面图片了。

## 后台自动发布

TODO

# 支持的浏览器


| 浏览器 | 支持情况 |
| --- |--|
| Chrome | ✔️ |
| Firefox | ✔️ |
| Safari | ❌️ |
| Edge | ❌ |
| Internet Explorer | ❌ |

# 使用方法

## 使用chrome 

1. 下载并安装 [Chrome](https://www.google.com/chrome/)。
2. 下载chrome Driver [Chrome Driver](https://googlechromelabs.github.io/chrome-for-testing/)。(可以从这里下载chrome for testing版本，专门用来自动化测试。)
3. chrome 以debug模式启动

如果是mac电脑，那么可以先给chrome设置一个alias

```bash
alias chrome="/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome"
```

如果你是google chrome for testing版本，那么可以这样设置：

```bash
alias chrome="/Applications/Google\ Chrome\ for\ Testing.app/Contents/MacOS/Google\ Chrome\ for\ Testing"
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

> 你也可以使用简单版本的 debugger_address: localhost:9222
>
> 我在windows环境下测试过是可以连接的。
>
> 在mac环境下有时可以连接，有时候不能连接，大家可以自行测试。(如果连不上，可以下载chrome for testing版本)

## 使用firefox
1. 下载并安装 [Firefox](https://www.mozilla.org/en-US/firefox/new/)。
2. 下载[**geckodriver**](https://github.com/mozilla/geckodriver/releases) 驱动.下载与你的Firefox浏览器版本相对应的geckodriver。确保你下载的是与你的操作系统和Firefox版本相匹配的版本。

3. 在firefox的启动命令之后加上： ` -marionette -start-debugger-server 2828`

![image-20240504120509315](https://flydean-1301049335.cos.ap-guangzhou.myqcloud.com/img/202405041205192.png)

如果你是mac，那么可以执行下面的命令：

```bash
alias firfox=/Applications/Firefox.app/Contents/MacOS/firefox
firfox  -marionette -start-debugger-server 2828
```

> 注意，这里的端口一定要是2828,不能自定义。

这时候你如果打开firefox,就会看到导航栏变成了红色，表示你已经启动了远程调试模式。

![image-20240504120607831](https://flydean-1301049335.cos.ap-guangzhou.myqcloud.com/img/202405041206516.png)

输入`about:config`

可以看到marionette.port的端口就是2828。

4. 修改配置文件

修改config/common.yaml 里面的内容：

```yaml
# firefox driver地址
service_location: "D:\\downloads\\geckodriver-v0.34.0-win32\\geckodriver.exe"
```

把driver_type修改为firefox。

```python
#driver_type: "chrome"
driver_type: "firefox"
```

## 设置封面

文章的封面图片是在markdown博客文件的yaml front matter中设置的。如下所示：

![image-20240507154807745](https://flydean-1301049335.cos.ap-guangzhou.myqcloud.com/img/202405071548984.png)

## 其他配置

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

## 运行程序

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

[一键自动化博客发布工具,chrome和firfox详细配置](http://www.flydean.com/blog/projects/002-auto-blog-publish-tool-chrome-firfox)

[一键自动化博客发布工具,用过的人都说好(segmentfault篇)](http://www.flydean.com/blog/projects/003-auto-blog-publish-tool-segmentfault)

[一键自动化博客发布工具,用过的人都说好(oschina篇)](http://www.flydean.com/blog/projects/004-auto-blog-publish-tool-oschina)

[一键自动化博客发布工具,用过的人都说好(阿里云篇)](https://www.flydean.com/blog/projects/005-auto-blog-publish-tool-alicloud)

[一键自动化博客发布工具,用过的人都说好(infoq篇)](https://www.flydean.com/blog/projects/007-auto-blog-publish-tool-infoq)

[一键自动化博客发布工具,用过的人都说好(cnblogs篇)](https://www.flydean.com/blog/projects/006-auto-blog-publish-tool-cnblogs)




