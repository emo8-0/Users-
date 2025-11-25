#!/usr/bin/env python3
"""
TikTok Username Availability Checker
أداة فحص يوزرات تيك توك - إصدار محسن ومنظم
"""

import requests
import threading
import random
import time
import sys
import os
from colorama import Fore, Style, init

# تهيئة الألوان
init(autoreset=True)

class TikTokChecker:
    def __init__(self):
        self.session = requests.Session()
        self.results = {
            'available': [],
            'taken': [],
            'errors': []
        }
        self.setup_headers()
    
    def setup_headers(self):
        """إعداد الهيدرات للطلبات"""
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "ar,en;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
        }
        self.session.headers.update(self.headers)
    
    def display_banner(self):
        """عرض البانر الجميل"""
        banner = f"""
{Fore.CYAN}
╔══════════════════════════════════════╗
║            TIKTOK CHECKER            ║
║          أداة فحص اليوزرات           ║
║              Version 2.0             ║
╚══════════════════════════════════════╝
{Fore.YELLOW}
👤 المطور: emo
📟 GitHub: github.com/emo8-0
🎯 الوظيفة: فحص يوزرات تيك توك المتاحة
{Style.RESET_ALL}
        """
        print(banner)
    
    def check_username(self, username):
        """فحص اسم المستخدم على TikTok"""
        try:
            url = f'https://www.tiktok.com/@{username}'
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                if 'user-detail' in response.text or 'userInfo' in response.text:
                    print(f"{Fore.RED}❌ مأخوذ: {username}{Style.RESET_ALL}")
                    self.results['taken'].append(username)
                    return False
                else:
                    print(f"{Fore.GREEN}✅ متاح: {username}{Style.RESET_ALL}")
                    self.results['available'].append(username)
                    return True
            else:
                print(f"{Fore.GREEN}✅ متاح: {username}{Style.RESET_ALL}")
                self.results['available'].append(username)
                return True
                
        except requests.exceptions.RequestException as e:
            print(f"{Fore.YELLOW}⚠️  خطأ شبكة: {username}{Style.RESET_ALL}")
            self.results['errors'].append(username)
            return False
    
    def generate_username(self):
        """إنشاء أسماء مستخدمين عشوائية"""
        patterns = [
            # أسماء قصيرة
            lambda: ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=4)),
            lambda: ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=5)),
            lambda: ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=6)),
            
            # أسماء بأرقام
            lambda: ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=3)) + ''.join(random.choices('0123456789', k=3)),
            lambda: ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=4)) + ''.join(random.choices('0123456789', k=2)),
            
            # أسماء بشرطة سفلية
            lambda: ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=3)) + '_' + ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=3)),
            lambda: 'user_' + ''.join(random.choices('0123456789', k=4)),
            
            # أسماء بنقاط
            lambda: ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=3)) + '.' + ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=3)),
        ]
        return random.choice(patterns)()
    
    def start_auto_check(self, threads=2, count=50):
        """بدء الفحص التلقائي"""
        print(f"\n{Fore.CYAN}🚀 بدء الفحص التلقائي...{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}📊 عدد الثريدات: {threads}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}🎯 عدد اليوزرات للفحص: {count}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}────────────────────────────────────────────{Style.RESET_ALL}")
        
        checked = 0
        
        def worker():
            nonlocal checked
            while checked < count:
                username = self.generate_username()
                self.check_username(username)
                checked += 1
                time.sleep(0.5)  # تقليل الضغط على الخوادم
        
        # إنشاء الثريدات
        thread_pool = []
        for i in range(threads):
            thread = threading.Thread(target=worker)
            thread.daemon = True
            thread.start()
            thread_pool.append(thread)
        
        # الانتظار حتى الانتهاء
        try:
            for thread in thread_pool:
                thread.join()
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}⏹️  تم إيقاف البرنامج{Style.RESET_ALL}")
        
        self.show_results()
    
    def check_specific_user(self):
        """فحص يوزر محدد"""
        print(f"\n{Fore.CYAN}🎯 فحص يوزر محدد{Style.RESET_ALL}")
        username = input(f"{Fore.WHITE}➤ ادخل اسم المستخدم: {Style.RESET_ALL}").strip()
        
        if username:
            self.check_username(username)
            self.show_results()
        else:
            print(f"{Fore.RED}❌ لم تدخل اسم مستخدم{Style.RESET_ALL}")
    
    def show_results(self):
        """عرض النتائج النهائية"""
        print(f"\n{Fore.CYAN}📊 النتائج النهائية:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✅ اليوزرات المتاحة: {len(self.results['available'])}{Style.RESET_ALL}")
        print(f"{Fore.RED}❌ اليوزرات المأخوذة: {len(self.results['taken'])}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}⚠️  اليوزرات التي فشل فحصها: {len(self.results['errors'])}{Style.RESET_ALL}")
        
        if self.results['available']:
            print(f"\n{Fore.GREEN}🎯 اليوزرات المتاحة:{Style.RESET_ALL}")
            for username in self.results['available'][:10]:  # عرض أول 10 فقط
                print(f"   {username}")

def main():
    """الدالة الرئيسية"""
    checker = TikTokChecker()
    checker.display_banner()
    
    while True:
        print(f"\n{Fore.CYAN}🎮 اختر وضع التشغيل:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}1. الوضع التلقائي (فحص عشوائي){Style.RESET_ALL}")
        print(f"{Fore.BLUE}2. فحص يوزر محدد{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}3. الخروج{Style.RESET_ALL}")
        
        choice = input(f"\n{Fore.WHITE}➤ اختر رقم الخيار: {Style.RESET_ALL}").strip()
        
        if choice == '1':
            try:
                threads = input(f"{Fore.WHITE}➤ عدد الثريدات (2): {Style.RESET_ALL}") or "2"
                count = input(f"{Fore.WHITE}➤ عدد اليوزرات للفحص (50): {Style.RESET_ALL}") or "50"
                checker.start_auto_check(int(threads), int(count))
            except ValueError:
                print(f"{Fore.RED}❌ الرجاء إدخال أرقام صحيحة{Style.RESET_ALL}")
        
        elif choice == '2':
            checker.check_specific_user()
        
        elif choice == '3':
            print(f"{Fore.YELLOW}👋 مع السلامة!{Style.RESET_ALL}")
            sys.exit(0)
        
        else:
            print(f"{Fore.RED}❌ خيار غير صحيح!{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
