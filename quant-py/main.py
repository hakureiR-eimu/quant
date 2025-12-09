"""
量化交易平台主程序
"""
from datetime import datetime
import schedule
import time

from biz.scan import run as scan_run

class QuantPlatform:
    def run(self):
        """运行平台主流程 - 每天15:55执行"""
        print("\n" + "=" * 60)
        print("定时任务模式")
        print("=" * 60)
        print("执行时间: 每天 15:05")
        print("按 Ctrl+C 停止程序")
        print("=" * 60 + "\n")
        
    def dev_run(self):
        """开发模式运行 - 立即执行一次策略任务"""
        print("\n" + "=" * 60)
        print("开发模式 - 立即执行")
        print("=" * 60 + "\n")
        
        scan_run()
        print("开发模式执行完成")


def main():
    """主函数"""
    platform = QuantPlatform()
    
    # 开发模式：立即执行一次
    platform.dev_run()
    
    # 生产模式：定时执行
    # platform.run()


if __name__ == "__main__":
    main()