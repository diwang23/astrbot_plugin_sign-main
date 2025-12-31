<div align="center">
  欢迎使用
  <h1>QQ 签到</h1>
</div>
AstrBot WordPress 签到插件
一个为 AstrBot 框架设计的 WordPress 子比主题签到插件，允许用户通过QQ群发送指令进行每日签到。

https://img.shields.io/badge/%E7%89%88%E6%9C%AC-v1.1.6-blue
https://img.shields.io/badge/Python-3.8+-green
https://img.shields.io/badge/AstrBot-%E2%9C%93-success

✨ 功能特性
📅 每日签到：通过QQ群指令 /签到 完成每日签到

🔐 安全认证：使用Token验证机制，确保API调用安全

🍪 自动Cookie管理：自动获取和管理用户Cookie

📊 结果格式化：美观的签到结果展示

🔧 配置灵活：支持自定义API地址和过期时间

📱 多平台支持：完美适配WordPress子比主题

🚀 快速开始
环境要求
Python 3.8+

AstrBot 框架

WordPress 站点（需安装子比主题签到插件）

安装步骤
安装插件到AstrBot：

bash
# 将插件文件夹放入AstrBot的plugins目录
cp -r astrbot_plugin_dmguoprcs-main /path/to/astrbot/plugins/
配置WordPress插件：

在WordPress后台安装并激活子比签到插件

生成API Token并配置相关设置

配置AstrBot插件：
在AstrBot配置文件中添加：

json
{
  "astrbot_plugin_sign": {
    "api_url": "https://your-wordpress-site.com",
    "api_key": "your_generated_token",
    "cookie_expire_minutes": 30
  }
}
📖 使用说明
可用指令
指令	描述	示例
/签到	进行每日签到	/签到
/sign help	显示帮助信息	/sign help
/sign status	查看插件状态	/sign status
签到流程
用户在QQ群发送 /签到 指令

插件获取用户QQ号

调用WordPress API获取Cookie

发送签到请求到WordPress

返回格式化签到结果

⚙️ 配置参数
参数	类型	默认值	说明
api_url	string	必填	WordPress站点地址
api_key	string	必填	WordPress插件生成的Token
cookie_expire_minutes	int	30	Cookie过期时间（分钟）
🏗️ 项目结构
text
astrbot_plugin_dmguoprcs-main/
├── __init__.py          # 插件主文件
├── data.py              # 数据处理类
├── _conf_schema.json    # 配置架构
├── README.md            # 说明文档
└── requirements.txt     # 依赖列表
🔧 核心类说明
SignPlugin - 插件主类
处理所有指令和事件

管理配置和数据处理器

提供帮助和状态查询功能

SignData - 数据处理类
负责与WordPress API通信

管理Cookie获取和存储

处理签到请求和响应

🔌 API接口
插件需要WordPress站点提供以下API：

1. 获取Cookie接口
text
GET /wp-json/taoxi/v1/terminal
参数：
  email: QQ号@qq.com
  expire_minutes: Cookie过期时间
  token: API Token
2. 签到接口
text
POST /wp-admin/admin-ajax.php
参数：
  action: user_checkin
头部：
  Cookie: 获取的Cookie字符串
🐛 故障排除
常见问题
签到失败：用户不存在

检查WordPress用户邮箱是否与QQ号匹配

确认API Token是否正确

获取Cookie失败

验证WordPress插件是否已正确安装并启用

检查API地址是否正确

响应解析错误

确认WordPress站点返回的数据格式

检查网络连接是否正常

日志查看
插件会输出详细的操作日志，可以在AstrBot日志中查看：

初始化信息

API调用详情

签到过程状态

错误信息

🤝 贡献指南
欢迎提交Issue和Pull Request！贡献前请：

Fork本仓库

创建功能分支 (git checkout -b feature/amazing-feature)

提交更改 (git commit -m 'Add amazing feature')

推送到分支 (git push origin feature/amazing-feature)

开启Pull Request

📄 许可证
本项目基于 MIT 许可证开源 - 查看 LICENSE 文件了解详情。

🙏 致谢
AstrBot - 优秀的机器人框架

WordPress 子比主题 - 提供签到功能基础

所有贡献者和用户

📞 支持与反馈
作者：呆小布

仓库：GitHub

问题反馈：Issues

星星此项目 ⭐ 如果你觉得这个插件有用！

