"""
量化交易平台主程序
"""
from datetime import datetime
import schedule
import time
import os
from biz.scan import run as scan_run

class QuantPlatform:
    def execute_strategy_task(self):
        """执行策略任务"""
        print(f"\n开始执行策略任务 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        scan_run()
        print(f"策略任务执行完成 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    def run(self):
        """运行平台主流程 - 每天15:05执行（A股收盘后）"""
        print("\n" + "=" * 60)
        print("定时任务模式")
        print("=" * 60)
        print("执行时间: 每天 15:05 (A股收盘后)")
        print("按 Ctrl+C 停止程序")
        print("=" * 60 + "\n")
        
        # 设置定时任务：每天15:05执行
        schedule.every().day.at("15:05").do(self.execute_strategy_task)
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # 每分钟检查一次
        except KeyboardInterrupt:
            print("\n" + "=" * 60)
            print("用户停止程序")
            print("=" * 60)
    
    def dev_run(self):
        """开发模式运行 - 立即执行一次策略任务"""
        print("\n" + "=" * 60)
        print("开发模式 - 立即执行")
        print("=" * 60 + "\n")
        
        self.execute_strategy_task()
        
        print("开发模式执行完成")


def main():
    """主函数"""
    platform = QuantPlatform()
    
    # 开发模式：立即执行一次
    # platform.dev_run()
    
    # 生产模式：定时执行
    platform.run()


if __name__ == "__main__":
    main()