史努比计划
=============

### Snoop Project 最有前途的 OSINT 工具之一，用于搜索昵称
- [X] 这是考虑到 CIS 位置的最强大的软件。

<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/EN__snoop.png" />

是你的生活幻灯片吗？ 问史努比。  
Snoop 项目是在没有考虑 NSA 和他们的朋友的意见的情况下开发的，  
即普通用户可用 *（项目创建日期：2020 年 2 月 14 日）。*  

> Snoop 是一项在互联网上搜索和处理公共数据的研究开发工作（自己的数据库/关闭的 bugbounty）。  
根据 Snoop 的专业搜索，它有能力与传统搜索引擎竞争。  

数据库索引等工具的比较：  
<img src="https://img.shields.io/badge/Snoop-~3100+%20网站-success" width="50%" />  
<img src="https://img.shields.io/badge/Sherlock-~350 网站-yellowgreen" width="20%" />  
<img src="https://img.shields.io/badge/Spiderfoot-~350 网站-yellowgreen" width="20%" />  
<img src="https://img.shields.io/badge/Whatsmyname-~300 网站-yellowgreen" width="20%" />  
<img src="https://img.shields.io/badge/Namechk-~100 网站-red" width="15%" />  


| 操作系统平台              | 支持 |
|-----------------------|:---------:|
| <img src="https://raw.githubusercontent.com/snooppr/snoop/master/icons/Linux.png" width="5%" /> GNU/Linux             |     ✅    |
| <img src="https://raw.githubusercontent.com/snooppr/snoop/master/icons/Windows.png" width="5%" /> Windows 7/10 (32/64)  |     ✅    |
| <img src="https://raw.githubusercontent.com/snooppr/snoop/master/icons/Android.png" width="5%" /> Android (Termux)      |     ✅    |
| <img src="https://raw.githubusercontent.com/snooppr/snoop/master/icons/macOS.png" width="5%" /> macOS                 |     ❗️    |
| <img src="https://raw.githubusercontent.com/snooppr/snoop/master/icons/IOS.png" width="5%" /> IOS                   |     🚫    |
| <img src="https://raw.githubusercontent.com/snooppr/snoop/master/icons/WSL.png" width="5%" /> WSL                   |     🚫    |  


适用于操作系统 Windows 和 GNU/Linux 的 Snoop
==================================

**探听本地数据库**  
<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/EN_DB.png" />  
[Snoop 完整版数据库 3100+ 个网站 ⚡️⚡️⚡️](https://github.com/snooppr/snoop/blob/master/websites.md "数据库探听")  

## 发布
<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/snoop box.png" width="35%" />  

Snoop 带有现成的程序集（发布版），不需要依赖项（库）或 python3 安装，也就是说，它可以在装有 OS Windows 或 GNU/Linux 的干净机器上运行。  
┗━━ ⬇️[下载 Snoop 项目](https://github.com/snooppr/snoop/releases "下载适用于 Windows 和 GNU/Linux 的现成 SNOOP 程序集")  

<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/Run.gif"/>  

<details>
<summary> 🟣 Snoop 项目插件</summary>  

### 1. 插件中方法之一的演示——〘GEO_IP/domain〙  
<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/GEO_IP.gif" />  

$$$$

报告也可以在 csv/txt/CLI/maps 中找到  
<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/GEO_IPcsv.jpeg" />  

$$$$

### 2. Plugin中方法之一的演示——〘Yandex_parser〙  
<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/Yandex_parser.gif" />  

$$$$

搜索报告打用户名（插件 — Yandex_parser）  
<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/Yandex_parser 4.png" />  

$$$$

### 3. 插件中方法之一的演示——〘Reverse Vgeocoder〙  
https://github.com/snooppr/snoop/assets/61022210/aeea3c0e-0d1b-429e-8e42-725a6a1a6653  

Snoop 仅从脏数据*（数字、字母、特殊字符）*中选择地理坐标。  

</details>

<details>
<summary> 🟤 从源代码自建软件</summary>  

**本机安装**  
+ 注意：如果你想在 android/termux 上安装 snoop，请不要这样做
*（安装不同，请参阅下面的专用部分）。*
+ 注意：要求 Python 3.7+ 版本

```
# 克隆存储库
$ git clone https://github.com/snooppr/snoop

# 登录到工作目录
$ cd ~/snoop

# 安装 python3 和 python3-pip 如果没有安装
$ apt-get update && apt-get install python3 python3-pip

# 安装依赖项'要求'
$ pip install --upgrade pip
$ python3 -m pip install -r requirements.txt
# 如果不是以特殊混合方式显示国家国旗，请提供字体包，例如单色
$ apt-get install ttf-ancient-fonts 或颜色（推荐） $ apt-get install fonts-noto-color-emoji
# 在 Windows 操作系统上使用 CMD 或 PowerShell（从方便中选择），而不是 ~~WSL~~！
```
</details>

<details>
<summary> 🟢 使用</summary>  

```
usage: snoop_cli [search arguments...] nickname
or
usage: snoop_cli [service arguments | plugins arguments]


$ snoop_cli --help #手动 snoop 构建版本 GNU/Linux

Help

optional arguments:
  -h, --help            显示此帮助信息并退出

service arguments:
  --version, -V         OS 的打印版本； 窥探； Python 和许可证
  --list-all, -l        打印有关 Snoop 数据库的详细信息
  --donate, -d          捐赠给 Snoop 项目的开发，获取/购买 Snoop 完整版
  --autoclean, -a       删除所有报告，清理空间
  --update, -U          更新探听

plugins arguments:
  --module, -m          OSINT 搜索：使用各种插件 Snoop :: IP/GEO/YANDEX

search arguments:
  nickname              被通缉用户的昵称。 支持同时搜索多个名称。 名称中包含空格的昵称用引号引起来
  --verbose, -v         搜索'昵称'时，打印详细的语言描述
  --web-base, -w        连接以在更新的 web_DB（3100+ 多个网站）中搜索'昵称'。 在演示版本中，
                        该功能被禁用
  --site , -s <site_name> 
                        从数据库'--list-all'中指定站点名称。 在一个指定的资源上搜索'昵称'，
                        多次使用'-s'选项是可以接受的
  --exclude , -e <country_code> 
                        从搜索中排除所选区域，允许多次使用'-e'选项，例如，'-e RU -e WR'
                        从搜索中排除俄罗斯和世界
  --include , -i <country_code> 
                        仅在搜索中包括选定的区域，允许多次使用'-i'选项，例如，'-i US -i UA'
                        搜索美国和乌克兰
  --country-sort, -c    按国家而不是字母顺序打印和记录结果
  --time-out , -t <digit> 
                        设置等待服务器响应的最大时间分配（秒）。 影响搜索持续时间。 影响'超时错误：
                        '打开。 如果 Internet 连接速度较慢（默认为 9 秒），此选项是必需的
  --found-print, -f     仅打印找到的帐户
  --no-func, -n         ✓单色终端，不要在url中使用颜色
                        ✓禁用声音
                        ✓禁用打开网络浏览器
                        ✓禁止打印国旗
                        ✓禁用指示和进度状态
  --userlist , -u <file> 
                        指定一个包含用户列表的文件。 Snoop 将智能处理数据并提供额外的报告
  --save-page, -S       将找到的用户页面保存到本地文件
  --cert-on, -C         在服务器上启用证书验证。 默认情况下，服务器上的证书验证是禁用的，
                        这使您可以无误地处理有问题的站点
  --headers , -H <User-Agent> 
                        手动设置用户代理，代理用引号括起来，默认情况下为每个站点设置来自 
                        snoop 数据库的随机或覆盖的用户代理
  --quick, -q           快速而积极的搜索模式。 不重新处理坏资源，因此搜索速度加快，但 Bad_raw
                        也会增加。 不打印中间结果。 消耗更多资源。 该模式完整版有效
```

**例子**
```
# 仅搜索一个用户：
$ python3 snoop.py username1 #从源代码运行
$ snoop_cli username1 #从发行版 linux 运行
# 或者，例如，支持西里尔字母：
$ python3 snoop.py олеся #从源代码运行
# 要搜索包含空格的名称：
$ snoop_cli "bob dylan" #从发行版 linux 运行
$ snoop_cli dob_dylan #从发行版 linux 运行
$ snoop_cli bob-dylan #从发行版 linux 运行

# 在 Windows 操作系统上运行：
$ python snoop.py username1 #从源代码运行
$ snoop_cli.exe username1 从发布 Windows 运行
# 要搜索一个或多个用户：
$ snoop_cli.exe username1 username2 username3 username4 从发布 Windows 运行

# 搜索大量用户-按国家对结果的输出进行排序；
# 避免网站冻结（更常见的是"死区"取决于用户的 ip 地址）；
# 只打印找到的账户； 在本地保存找到的帐户页面；
# 指定一个包含所需帐户列表的文件；
# 连接到可扩展和更新的基于 Web 的 Snoop 进行搜索：
$ snoop_cli -с -t 6 -f -S -u ~/file.txt -w #从发行版 linux 运行
# 检查 Snoop 数据库：
$ snoop_cli --list all #从发行版 linux 运行
# 打印 Snoop 函数的帮助：
$ snoop_cli --help #从发行版 linux 运行

# 启用 Snoop 插件：
$ snoop_cli --module #从发行版 linux 运行
```
+ 'ctrl-c' — 中止搜索。  
+ 找到的账户将存储在 `~/snoop/results/nicknames/*{txt|csv|html}`.  
+ 在office中打开csv，字段分隔符**逗号**。  
+ 销毁**所有**搜索结果——删除 '~/snoop/results' 目录.  
或者 `snoop_cli.exe --autoclean` #从发布操作系统 Windows 运行。
```
# 更新 Snoop 以测试软件中的新功能
$ python3 snoop.py --update #需要安装 Git
```
</details>  

<details>
<summary> 🔵 Android 版探听</summary>  

 • [详细的英文手册](https://github.com/snooppr/snoop/blob/snoop_termux/README.en.md "Android 版探听")  

</details>

<details>
<summary> 🔴 基本错误</summary>

| 边        |                         问题                           | 求解    |
|:---------:| ------------------------------------------------------|:-------:|
| ========= |=======================================================| ======= |
| 客户       |使用主动保护防火墙阻止连接                                 |    1    |
|           |EDGE/3G 互联网连接速度不够                                |    2    |
|           |"-t"选项的值太低                                         |    2    |
|           |无效的用户名                                             |    3    |
|           |连接错误：[GipsysTeam; Nixp; Ddo; Mamochki]              |    7    |
| ========= |=======================================================| ======= |
| 供应商     |互联网审查                                               |    4    |
| ========= |=======================================================| ======= |
| 服务器     |该站点已更改其响应/API； CF/WAF 已更新                      |    5    |
|           |服务器屏蔽客户端的IP地址范围                                |    4    |
|           |触发/保护验证码资源                                       |    4    |
|           |部分站点暂时无法访问，技术工作                              |    6    |
| ========= |=======================================================| ======= |

解决：
1. 重新配置您的防火墙 *（例如，卡巴斯基阻止成人资源）。*

2. 检查您的互联网连接速度：  
`python3 snoop.py -v 用户名`  
如果任何网络参数以红色突出显示，Snoop 可能会在搜索过程中挂起。
在低速时，增加"--time-out x"选项的"x"值：  
`python3 snoop.py -t 15 用户名`。

3. 其实这并不是错误。 修复用户名  
*（例如，某些网站不允许使用西里尔字符；"空格"或"越汉编码"
在用户名中，为了节省时间：- 请求被过滤）。*

4. **更改您的IP地址**
审查是用户收到跳过错误/误报/在某些情况下"**唉**"的最常见原因。
从移动运营商提供商的 IP 地址使用 Snoop 时，速度**可能**会显着下降，具体取决于提供商。
例如，解决问题最有效的方法是**使用 VPN**，Tor 不太适合此任务。
规则：来自一个 ip 的一次扫描不足以充分利用 Snoop。

5. 在Github-e Issue/Pull request上打开Snoop仓库
*（将此通知开发人员）。*

6. 不注意，现场有时会去维修工作并恢复运营。

7. 在某些 GNU/Linux 发行版中，openssl 存在 [问题](https://wiki.debian.org/ContinuousIntegration/TriagingTips/openssl-1.1.1 "问题很简单且可解决")，还有问题 多年未更新的网站。 如果用户故意使用"--cert-on"选项开始侦听，就会出现这些问题。  
解决：
```
$ sudo nano /etc/ssl/openssl.cnf

# 编辑文件最底部的行：
[MinProtocol = TLSv1.2]
在
[MinProtocol = TLSv1]

[CipherString = DEFAULT@SECLEVEL=2]
在
[CipherString = DEFAULT@SECLEVEL=1]
```
</details>

<details>
<summary> 🟠 附加信息</summary>

 • [项目发展历程](https://raw.githubusercontent.com/snooppr/snoop/master/changelog.txt "变更日志").  

 • [执照](https://github.com/snooppr/snoop/blob/master/COPYRIGHT "License 的英文版本可以在 Snoop Build 的 EN 版本中找到").  

 • [文档/俄语](https://drive.google.com/open?id=12DzAQMgTcgeG-zJrfDxpUbFjlXcBq5ih).  

 • **公钥指纹：**	[076DB9A00B583FFB606964322F1154A0203EAE9D](https://raw.githubusercontent.com/snooppr/snoop/master/PublicKey.asc "pgp密钥").  

 • **公务员/RU 信息：** Snoop 项目包含在国内软件登记册中，声明代码：26.30.11.16 确保在操作搜索活动中执行既定操作的软件。
俄罗斯联邦交通部命令第 515 号注册号 7012。  

 • **Snoop 并不完美**：网站正在下降； 结束标签丢失； 网络正在被审查； 托管服务未按时付款。有时，有必要关注所有这些"网络摇滚"，因此欢迎捐款：
[例子关闭/坏网站](https://drive.google.com/file/d/1CJxGRJECezDsaGwxpEw34iJ8MJ9LXCIG/view?usp=sharing).  

 • **提交的可视化：**从项目诞生到 2023 年十三号星期五。  

https://user-images.githubusercontent.com/61022210/212534128-bc0e5779-a367-4d0a-86cb-c52503ee53c4.mp4  
</details>

【RU -> CN】 这是翻译的 [➰俄语自述文件](https://github.com/snooppr/snoop "如果你愿意，你可以改进（PR）这个页面在中国的机器翻译").
