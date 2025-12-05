from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.api import AstrBotConfig
import astrbot.api.message_components as Comp
from .data import SignData

@register("astrbot_plugin_sign", "呆小布", "QQ签到插件", "1.1.6", "https://github.com/diwang23/astrbot_plugin_sign-main.git")
class SignPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config
        logger.info(f"签到插件初始化完成，API地址: {self.config.get('api_url', '未设置')}")
        
        # 初始化数据处理类
        api_url = self.config.get('api_url', 'https://dmguo.cn')
        logger.info(f"成功获取API地址: {api_url}")
        cookie_expire = self.config.get('cookie_expire_minutes', 30)
        logger.info(f"成功获取cookie过期时间: {cookie_expire} 分钟")
        self.data_handler = SignData(api_url, cookie_expire)
    
    @filter.command("签到")
    async def sign_command(self, event: AstrMessageEvent):
        '''签到功能 - 发送 /签到 进行每日签到'''
        try:
            # 获取发送者的QQ号
            qq = event.get_sender_id()
            if not qq:
                yield event.plain_result("无法获取您的QQ号")
                return
            
            # 显示正在签到
            #yield event.plain_result(f"正在为 QQ: {qq} 执行签到操作...")
            
            # 1. 获取cookie
            logger.info(f"正在为QQ {qq} 获取cookie...")
            cookie = await self.data_handler.get_cookie(qq)
            
            if cookie in ["用户不存在", "请求异常"]:
                yield event.plain_result(f"获取cookie失败: {cookie}")
                return
            
            logger.info(f"成功获取cookie: {cookie[:50]}...")
            
            # 2. 发送签到请求
            logger.info(f"正在为QQ {qq} 发送签到请求...")
            result = await self.data_handler.post_sign(cookie)
            # 3. 格式化并返回结果
            formatted_result = self.data_handler.format_sign_result(result, qq)
            
            # 构建回复消息链
            chain = [
                Comp.At(qq=qq),
                Comp.Plain(" "),
                Comp.Plain(" " + formatted_result),
                Comp.Image.fromURL(f"http://q2.qlogo.cn/headimg_dl?dst_uin={qq}&spec=100")
            ]
            
            yield event.chain_result(chain)
            
        except Exception as e:
            logger.error(f"签到过程中出现错误: {e}")
            yield event.plain_result(f"签到失败，请稍后重试。错误: {str(e)}")
    
    @filter.command_group("sign")
    def sign_group(self):
        '''签到插件指令组'''
        pass
    
    @sign_group.command("help")
    async def sign_help(self, event: AstrMessageEvent):
        '''显示签到插件帮助'''
        help_text = """
        🎯 签到插件使用说明：
        
        /签到 - 进行每日签到
        /sign help - 显示此帮助
        
        📝 功能说明：
        1. 自动获取您的QQ号
        2. 调用API获取cookie
        3. 执行签到操作
        4. 返回签到结果
        """
        yield event.plain_result(help_text)
    
    @sign_group.command("status")
    async def sign_status(self, event: AstrMessageEvent):
        '''查看插件状态'''
        status_text = f"""
        📊 签到插件状态：
        
        API地址: {self.config.get('api_url', '未设置')}
        Cookie有效期: {self.config.get('cookie_expire_minutes', 30)} 分钟
        插件版本: 1.0.0
        运行状态: ✅ 正常
        """
        yield event.plain_result(status_text)
    
    async def terminate(self):
        '''插件卸载时调用'''
        logger.info("签到插件已卸载")