import httpx
import json
from urllib.parse import urlencode
from typing import Dict, Any, List

class SignData:
    """签到数据处理类"""
    
    def __init__(self, api_url: str, cookie_expire_minutes: int = 30):
        self.api_url = api_url.rstrip('/')
        self.cookie_expire_minutes = cookie_expire_minutes
    
    async def get_cookie(self, qq,key:str) -> str:
        """
        获取cookie
        参数：
            qq: QQ号码
        返回：
            cookie字符串 或 错误信息
        """
        try:
            url = f"{self.api_url}/wp-json/taoxi/v1/terminal?email={qq}@qq.com&expire_minutes={self.cookie_expire_minutes}&token={key}"
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url,
                    headers={'Accept': 'application/json'}
                )
                data = response.json()
                if not data.get('success', True) or response.status_code != 200:
                    return data.get('message', "请求失败")
                
                # 获取所有Set-Cookie头
                set_cookie_headers = response.headers.get_list('set-cookie')
                return self._extract_cookies_from_headers(set_cookie_headers)
                
        except Exception as e:
            print(f"获取cookie失败: {e}")
            return "请求异常"
    
    def _extract_cookies_from_headers(self, cookie_headers: list) -> str:
        """
        从HTTP头中提取并合并cookie字符串
        """
        if not cookie_headers:
            return ""
        
        cookies = []
        for header in cookie_headers:
            # 分割每个cookie头，取第一个分号前的内容（键值对部分）
            cookie_parts = header.split(';')
            if cookie_parts:
                cookies.append(cookie_parts[0].strip())
        
        # 使用分号和空格合并所有cookie
        return '; '.join(cookies)
    
    async def post_sign(self, cookie: str, qq: str = "") -> str:
        """
        发送签到请求并直接返回响应内容
        参数：
            cookie: cookie字符串
            qq: QQ号码（可选，用于日志记录）
        返回：
            响应内容字符串
        """
        try:
            url = f"{self.api_url}/wp-admin/admin-ajax.php"
            data = {
                'action': 'user_checkin'
            }
            
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Cookie': cookie,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0'
            }
            
            # 使用httpx替换aiohttp
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url,
                    data=data,  # httpx会自动进行form编码
                    headers=headers
                )
                
                # 直接返回响应内容
                return response.text
                
        except Exception as e:
            print(f"签到请求失败: {e}")
            return json.dumps({
                'success': False,
                'message': f'请求异常: {str(e)}'
            }, ensure_ascii=False)
    
    def format_sign_result(self, result: str, qq: str) -> str:
        """
        格式化签到结果
        """
        try:
            result_data = json.loads(result)
            msg_content = result_data['msg']
        
           # 直接解码
            return msg_content
        except json.JSONDecodeError:
            # 如果不是JSON，直接返回原始内容
            return f"签到响应（原始内容）:\nQQ: {qq}\n响应: {result}"