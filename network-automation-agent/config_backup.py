#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网络设备配置自动备份工具
Network Device Configuration Backup Tool

功能：
1. 批量备份华为网络设备配置
2. 按日期组织备份文件
3. 支持多设备类型（华为、思科等）
"""

import csv
import os
import time
from datetime import datetime
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, AuthenticationException

# 配置
INVENTORY_FILE = 'device_inventory.csv'
BACKUP_DIR = 'backups'
TIMESTAMP = datetime.now().strftime('%Y%m%d_%H%M%S')

def create_backup_dir():
    """创建备份目录"""
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
    date_dir = os.path.join(BACKUP_DIR, datetime.now().strftime('%Y-%m-%d'))
    if not os.path.exists(date_dir):
        os.makedirs(date_dir)
    return date_dir

def read_device_inventory():
    """读取设备清单"""
    devices = []
    with open(INVENTORY_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            devices.append(row)
    return devices

def backup_device_config(device, backup_dir):
    """备份单个设备配置"""
    print(f"\n[+] 正在备份设备: {device['hostname']} ({device['ip_address']})")
    
    try:
        # 连接设备
        net_connect = ConnectHandler(
            device_type=device['device_type'],
            host=device['ip_address'],
            username=device['username'],
            password=device['password'],
            timeout=10
        )
        
        # 获取配置
        if device['device_type'] == 'huawei':
            output = net_connect.send_command('display current-configuration')
        elif device['device_type'] == 'cisco_ios':
            output = net_connect.send_command('show running-config')
        else:
            print(f"[-] 不支持的设备类型: {device['device_type']}")
            return False
        
        # 保存配置
        filename = f"{device['hostname']}_{TIMESTAMP}.txt"
        filepath = os.path.join(backup_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# 设备: {device['hostname']}\n")
            f.write(f"# IP: {device['ip_address']}\n")
            f.write(f"# 备份时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"# {'='*60}\n\n")
            f.write(output)
        
        print(f"[+] 配置已保存: {filepath}")
        net_connect.disconnect()
        return True
        
    except NetmikoTimeoutException:
        print(f"[-] 连接超时: {device['ip_address']}")
        return False
    except AuthenticationException:
        print(f"[-] 认证失败: {device['ip_address']}")
        return False
    except Exception as e:
        print(f"[-] 错误: {str(e)}")
        return False

def main():
    """主函数"""
    print("="*60)
    print("网络设备配置自动备份工具")
    print("Network Device Configuration Backup Tool")
    print("="*60)
    
    # 创建备份目录
    backup_dir = create_backup_dir()
    print(f"\n[+] 备份目录: {backup_dir}")
    
    # 读取设备清单
    try:
        devices = read_device_inventory()
        print(f"[+] 读取到 {len(devices)} 台设备")
    except FileNotFoundError:
        print(f"[-] 找不到设备清单文件: {INVENTORY_FILE}")
        print(f"[-] 请先创建 {INVENTORY_FILE}")
        return
    
    # 备份所有设备
    success_count = 0
    fail_count = 0
    
    for device in devices:
        if backup_device_config(device, backup_dir):
            success_count += 1
        else:
            fail_count += 1
        time.sleep(1)  # 避免过快连接
    
    # 统计
    print("\n" + "="*60)
    print("备份完成!")
    print(f"成功: {success_count} 台")
    print(f"失败: {fail_count} 台")
    print("="*60)

if __name__ == '__main__':
    main()
