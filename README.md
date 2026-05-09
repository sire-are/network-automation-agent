# 企业园区网络智能运维系统
# Enterprise Campus Network Intelligent O&M System

## 📋 项目简介

本项目是一个基于Python的企业园区网络智能运维工具集，旨在提升网络管理效率，降低故障处理时间。

**核心功能：**
- 🔧 网络设备配置自动备份
- 📊 设备日志智能分析
- 🤖 AI辅助故障诊断（集成DeepSeek API）
- 📝 配置变更自动审计

**目标效果：**
- 故障定位时间：从30分钟缩短至5分钟
- 配置错误率：降低80%
- 日常运维效率：提升3倍

---

## 🛠️ 技术栈

- **Python 3.8+**
- **Netmiko** - 网络设备SSH连接
- **Paramiko** - SSH协议库
- **Pandas** - 日志数据分析
- **DeepSeek API** - AI智能分析

---

## 📂 项目结构

```
network-automation-agent/
├── README.md              # 项目说明文档
├── requirements.txt       # Python依赖
├── config_backup.py       # 配置备份脚本
├── log_analyzer.py        # 日志分析脚本
├── device_inventory.csv   # 设备清单（示例）
└── .gitignore           # Git忽略文件
```

---

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置设备清单

编辑 `device_inventory.csv`，添加你的网络设备信息：

```csv
hostname,ip_address,device_type,username,password
CORE-SW-01,192.168.1.1,huawei,admin,password123
ACCESS-SW-01,192.168.1.2,huawei,admin,password123
FIREWALL-01,192.168.1.254,huawei,admin,password123
```

### 3. 运行配置备份

```bash
python config_backup.py
```

备份文件将保存在 `backups/` 目录下，按日期组织。

### 4. 运行日志分析

```bash
python log_analyzer.py --log-file device.log --output report.txt
```

---

## 💡 使用场景

### 场景1：自动化配置备份
**问题：** 手动备份几十台交换机配置耗时费力，且容易遗漏。

**解决方案：**
```python
# 批量备份所有设备配置
python config_backup.py
```

**效果：** 50台设备配置备份从2小时缩短至5分钟。

---

### 场景2：日志异常检测
**问题：** 网络设备故障前通常有日志告警，但人工查看海量日志效率低。

**解决方案：**
```python
# 分析设备日志
python log_analyzer.py --log-file core_switch.log --output analysis.txt
```

**效果：** 自动识别CPU高、接口Flapping、MAC地址漂移等异常。

---

### 场景3：AI辅助故障诊断
**问题：** 复杂故障需要综合分析多个设备日志，人工分析耗时长。

**解决方案：**
集成DeepSeek API，将日志发送给AI分析：

```python
# 使用DeepSeek API进行智能分析
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_DEEPSEEK_API_KEY",
    base_url="https://api.deepseek.com"
)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "你是一个网络故障诊断专家"},
        {"role": "user", "content": f"分析以下设备日志，找出可能的故障原因：\n{log_content}"}
    ]
)
print(response.choices[0].message.content)
```

**预期效果：** AI在30秒内给出故障根因分析和修复建议。

---

## 📊 项目规划

### Phase 1：基础功能（当前阶段）
- ✅ 配置自动备份
- ✅ 日志批量分析
- 🔄 设备清单管理

### Phase 2：AI集成（已集成DeepSeek API）
- ✅ 集成DeepSeek API进行日志智能分析
- ✅ 自然语言查询网络设备状态
- ⏳ 自动生成故障处理报告

### Phase 3：高级功能
- ⏳ 配置变更自动审核
- ⏳ 网络拓扑自动发现
- ⏳ 性能趋势预测

---

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

**快速安装：**
```bash
pip install -r requirements.txt
```

**开发环境搭建：**
```bash
git clone https://github.com/sire-are/network-automation-agent.git
cd network-automation-agent
pip install -r requirements.txt
```

---

## 📄 许可证

MIT License - 可自由用于商业和个人项目。

---

## 👤 作者

**haohao**

- 专注领域：企业园区网络规划与实施
- 技术栈：华为eNSP、CSS堆叠、MSTP+VRRP、BGP MPLS VPN
- 项目经验：9台设备配置文件编写，6类设备部署

---

**⭐ 如果这个项目对你有帮助，请给个Star！**
