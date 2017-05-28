---
title: scrapy入门—从抓取静态页面开始
date: 2017-05-26 20:12:08
tags: "Python"
categories: "技术"
---

这几天花了不少心思折腾这个博客，终于被我折腾起来了。本博客使用的hexo+next，被寄托在GitHub上，打算在这儿记录自己的学习历程，欢迎看到的朋友多多交流，共同进步。
博客建起后第一篇文章就以scrapy开始吧，很多人接触Python都是从爬虫入门的，我也不例外。相比于Request和urllib，scrapy更注重于“爬虫”。本文以爬取前程无忧中以“Python”为搜索词的结果，并将爬取结果以csv格式导出。

## 安装scrapy
scrapy的安装方法网上教程很多，这里不再赘述。仅简述一个Windows下较为简单的办法。首先安装[anaconda](https://www.continuum.io/downloads/),安装完成后打开cmd控制台输入
```
> conda install scrapy
```
conda会自动安装scrapy所需要的一些依赖，耐心等待安装结束后，在控制台输入，
```
> python
```
然后进入`python`控制台中，输入
```
> import scrapy
```
如果没有报错说明scrapy已经正常安装。

## scrapy常用命令

windows下使用`win`+`R`呼出CMD控制台，使用`cd`命令和`dir`命令进入想要保存项目的目录。
然后输入
```
scrapy startproject <工程名>
```
工程名是我们自己定义的。`startproject`命令是scrapy命令的一种，用于创建工程，其他还有很多有用的命令，如：

```
scrapy genspider mydomain mydomain.com         #创建一个名为mydomain的spider,mydomain是指这个爬虫的顶级域名
scrapy -h                                      #scrpay帮助命令
scrapy settings                                #显示scrapy的setting信息，如果在非工程目录下就显示默认信息，在工程下则显示这个工程的setting信息
scrapy runspider                               #运行一个spider.py脚本，相当于一个执行文件，不需要创建工程
scrapy shell [url]                             #进入scrapy的调试界面 
scrapy fetch [url]                             #运行一个spider将从url得到的东西标准化输出
scrapy view <url>                              #从浏览器中打开这个url，可以验证返回的页面是不是我们想要的
scrapy version                                 #显示scrapy当前版本
```
这些都是scrapy的全局命令，意味着这些命令不需要在工程目录下就可以直接运行。
下面这些命令称为scrapy的工程命令，只能在所创建工程的目录下运行：
```
scrapy crawl  #后面接一个爬虫名，并使用这个spider开始爬取
scrapy list  #显示当前工程所有的spiders
scrapy parse #使用一个callback函数去解析所给的url
```
这些命令具体用法参见[scrapy document](https://doc.scrapy.org/en/latest/topics/commands.html)

## 首先确定url：

这里我使用scrapy爬取51job上以Python为关键词搜索出的所有结果。
步骤：

打开[51job](http://www.51job.com/)，输入搜索词Python，复制得到的新网页的链接：http://search.51job.com/list/080200,000000,0000,00,9,99,Python,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=。
![2.png](2.png)
+ 到指定目录下打开命令行输入：
```
scrapy startproject jobspider 
```
## 创建工程
 进入jobspider工程目录下创建spider:
```
cd jobspider
scrapy genspider jobspider1 "http://search.51job.com/list/080200,000000,0000,00,9,99,Python,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare="
```
运行完得到如下结果：
```
Created spider 'jobspider1' using template 'basic' in module:
  jobspider.spiders.jobspider1
```
然后打开：工程目录\spiders\下的jobspider1.py，使用任意文本编辑器即可，推荐sublime。
![1.png](1.png)

## 编写爬虫
接下来处理`jobspider1.py`文件：
首先可以注释掉allowed_domains这一行，然后将start_urls中的http去重。
![3.png](3.png)
重头戏来了，开始编写parse函数，可以使用`scrapy shell`帮助我们：
首先打开cmd命令行,输入：
```
> scrapy shell "http://search.51job.com/list/080200,000000,0000,00,9,99,python,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare="
```
看到一长串命令不知道是什么的东东后得到如下结果（以后会知道这些是爬虫的日志文件）：
![3.png](4.png)
然后可以看到Available scrapy objects有很多，我们先使用
```
In [1]: view(respone)
```
发现返回true，并浏览器自动打开了一个页面，但是奇怪的是这个页面和我们之前的页面复制url的页面不一样，可以很明显的发现这是一个手机端的页面，原来是咱们的`user_agent`还没有设置。
+ 设置`user_agent`：
打开jobspider目录下的settings.py文件，使用查找找到`USER_AGENT`，去掉这项注释，并把后面的内容改成我们这前浏览器打开网页的USER_AGENT。（使用谷歌浏览器，按F12打开开发者工具，在network中找到这个网页的Request header信息，然后复制USER_AGENT信息）,接着把ROBOTSTXT_OBEY后面的true改成False。
结果如下：
![3.png](5.png)
回到scrapy shell控制台，`ctrl+d`先退出，然后重复以上：
```
> scrapy shell "http://search.51job.com/list/080200,000000,0000,00,9,99,python,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare="
```
接着：
```
view(reponse)
```
bingo！！！和我们之前看到的一样。
下面开始解析网页内容。
这里使用css选择器，熟悉xpath的同学更推荐使用xpath。
打开chrome+F12，使用`Ctrl+shift+c`选择要提取的内容，可以看到他们所在位置
![3.png](6.png)
## 改写items.py
添加所要爬取的5个内容，分别是标题，公司名称，位置，薪水，发布时间。
![3.png](7.png)
改写parse函数：
![3.png](8.png)
然后在命令行输入:
```
> scrapy crawl jobspider1 -o joblist.json
```
命令行会出现爬取的过程，看着很爽有木有！
![3.png](9.png)
结果将以json格式输出保存在jobspider根目录下。
![3.png](10.png)
将40页的内容全部爬下了。
bingo！

## 总结
爬取静态页面很简单，下次讲爬取动态页面（其实也很简单）。
过程总结如下：
1. 创建项目以及spider；
2. 定义item；
3. 解析网页内容；
4. 编程以及调试debug；
5. 完成。
json输出可能有编码问题，解决办法：在settings.py文件中加入一行:
`FEED_EXPORT_ENCONDING = 'utf-8'`
