#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网络设备日志分析工具
Network Device Log Analyzer

功能：
1. 分析华为设备日志
2. 识别常见异常（接口Flapping、CPU高、MAC漂移等）
3. 生成分析报告
"""

import argparse
import re
from datetime import datetime
from collections import Counter

# 常见异常模式
ANOMALY_PATTERNS = {
    '接口Flapping': r'Interface\s+(\S+)\s+has\s+flapped',
    'CPU使用率高': r'CPU\s+usage\s+exceeds\s+(\d+)%',
    'MAC地址漂移': r'MAC\s+address\s+(\S+)\s+has\s+moved',
    '链路震荡': r'Link\s+status\s+changed\s+to\s+(down|up)',
    '认证失败': r'Authentication\s+failed\s+for\s+user\s+(\S+)',
    '配置变更': r'Configuration\s+has\s+been\s+changed',
    'STP拓扑变化': r'STP\s+topology\s+changed',
    'OSPF邻居Down': r'OSPF\s+neighbor\s+(\S+)\s+down',
}

def parse_log_file(log_file):
    """解析日志文件"""
    logs = []
    with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            # 尝试提取时间戳和日志内容
            match = re.search(r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})', line)
            if match:
                timestamp = match.group(1)
                content = line[match.end():].strip()
                logs.append({
                    'timestamp': timestamp,
                    'content': content
                })
    return logs

def analyze_logs(logs):
    """分析日志，识别异常"""
    anomalies = {key: [] for key in ANOMALY_PATTERNS.keys()}
    severity_counter = Counter()
    
    for log in logs:
        content = log['content']
        
        # 检查异常模式
        for anomaly_name, pattern in ANOMALY_PATTERNS.items():
            if re.search(pattern, content, re.IGNORECASE):
                anomalies[anomaly_name].append({
                    'timestamp': log['timestamp'],
                    'content': content[:100]  # 截断过长内容
                })
        
        # 统计日志级别
        if 'Error' in content or 'ERROR' in content:
            severity_counter['ERROR'] += 1
        elif 'Warning' in content or 'WARNING' in content:
            severity_counter['WARNING'] += 1
        elif 'Info' in content or 'INFO' in content:
            severity_counter['INFO'] += 1
    
    return anomalies, severity_counter

def generate_report(anomalies, severity_counter, output_file):
    """生成分析报告"""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("="*60 + "\n")
        f.write("网络设备日志分析报告\n")
        f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*60 + "\n\n")
        
        # 日志级别统计
        f.write("【日志级别统计】\n")
        for level, count in severity_counter.most_common():
            f.write(f"  {level}: {count} 条\n")
        f.write("\n")
        
        # 异常检测结果
        f.write("【异常检测结果】\n")
        total_anomalies = 0
        for anomaly_name, occurrences in anomalies.items():
            if occurrences:
                f.write(f"\n⚠️  {anomaly_name}: 发现 {len(occurrences)} 次\n")
                total_anomalies += len(occurrences)
                # 显示前3条
                for i, occ in enumerate(occurrences[:3], 1):
                    f.write(f"    {i}. [{occ['timestamp']}] {occ['content']}\n")
                if len(occurrences) > 3:
                    f.write(f"    ... 还有 {len(occurrences)-3} 条\n")
        
        if total_anomalies == 0:
            f.write("  ✓ 未发现明显异常\n")
        
        f.write("\n" + "="*60 + "\n")
        f.write(f"总计发现 {total_anomalies} 个异常事件\n")
        f.write("="*60 + "\n")
    
    print(f"\n[+] 分析报告已生成: {output_file}")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='网络设备日志分析工具')
    parser.add_argument('--log-file', required=True, help='日志文件路径')
    parser.add_argument('--output', default='log_analysis_report.txt', help='输出报告文件')
    
    args = parser.parse_args()
    
    print("="*60)
    print("网络设备日志分析工具")
    print("="*60)
    
    # 解析日志
    print(f"\n[+] 正在解析日志文件: {args.log_file}")
    logs = parse_log_file(args.log_file)
    print(f"[+] 共解析 {len(logs)} 条日志")
    
    # 分析日志
    print("\n[+] 正在分析日志...")
    anomalies, severity_counter = analyze_logs(logs)
    
    # 生成报告
    generate_report(anomalies, severity_counter, args.output)
    
    # 显示摘要
    print("\n" + "="*60)
    print("分析完成!")
    print(f"日志总数: {len(logs)}")
    print(f"ERROR: {severity_counter['ERROR']}")
    print(f"WARNING: {severity_counter['WARNING']}")
    print(f"INFO: {severity_counter['INFO']}")
    print("="*60)

if __name__ == '__main__':
    main()
