<div align="center">

# 🤖 RepoInsight-AI

**AI驱动的GitHub仓库智能分析工具**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/gitstq/RepoInsight-AI)](https://github.com/gitstq/RepoInsight-AI/stargazers)

[简体中文](#简体中文) | [繁體中文](#繁體中文) | [English](#english)

</div>

---

## 简体中文

### 🎉 项目介绍

RepoInsight-AI 是一款**AI驱动的GitHub仓库智能分析工具**，旨在帮助开发者快速洞察开源项目的代码质量、社区健康度与发展趋势。

**核心价值：**
- 🔍 深度分析任意GitHub仓库的核心指标
- 📊 智能评估项目活跃度与维护状态
- 💡 提供专业的技术选型建议
- ⚡ 零配置，开箱即用

**灵感来源：** 在日常开发中，我们经常需要评估第三方库的质量和可靠性。现有的工具要么过于复杂，要么信息不够全面。RepoInsight-AI 通过简洁的CLI界面，将关键指标一目了然地呈现出来。

### ✨ 核心特性

- 🎯 **智能分析** - 自动计算Star增速、社区健康度、活跃度评分
- 📈 **趋势洞察** - 识别项目维护状态（积极维护/缓慢维护/可能弃用）
- 🏥 **健康评估** - 综合评估代码质量、社区活跃度、文档完整性
- 🔥 **热门发现** - 支持按语言筛选热门仓库
- 🎨 **精美输出** - 使用Rich库打造终端可视化体验
- 🌐 **多语言支持** - 原生支持中英文输出
- ⚡ **轻量快速** - 单文件设计，依赖精简

### 🚀 快速开始

#### 环境要求
- Python 3.8+
- GitHub Personal Access Token（可选，但推荐）

#### 安装步骤

```bash
# 克隆仓库
git clone https://github.com/gitstq/RepoInsight-AI.git
cd RepoInsight-AI

# 安装依赖
pip install -r requirements.txt

# 或本地安装
pip install -e .
```

#### 配置Token（推荐）

```bash
# 设置环境变量
export GITHUB_TOKEN=your_github_token_here
```

获取Token：[GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)

#### 使用示例

```bash
# 分析指定仓库
repoinsight analyze facebook/react

# 分析仓库URL
repoinsight analyze https://github.com/torvalds/linux

# 查看Python热门仓库
repoinsight trending Python -n 10

# 查看帮助
repoinsight --help
```

### 📖 详细使用指南

#### 分析仓库

```bash
# 基础分析
repoinsight analyze owner/repo

# 使用Token（提高API限制）
repoinsight analyze owner/repo --token YOUR_TOKEN
```

输出包含：
- 📋 基本信息（语言、协议、大小）
- 📈 社区指标（Stars、Forks、Issues）
- 🏥 健康度评估（活跃度、维护状态）
- 💡 智能建议（是否适合生产使用）

#### 查看热门仓库

```bash
# 查看JavaScript热门仓库 Top 10
repoinsight trending JavaScript

# 查看Go语言热门仓库 Top 20
repoinsight trending Go -n 20
```

#### 配置检查

```bash
# 查看当前配置状态
repoinsight config
```

### 💡 设计思路与迭代规划

**技术选型：**
- **Python 3.8+**: 广泛兼容，生态丰富
- **Click**: 强大的CLI框架，支持命令嵌套
- **Rich**: 终端美化，提供表格、面板、进度条
- **Requests**: 简洁的HTTP客户端

**设计理念：**
- 简单至上：一条命令完成分析
- 信息密度：在终端有限空间展示关键信息
- 智能化：自动计算衍生指标，提供建议

**后续迭代计划：**
- [ ] 支持导出JSON/CSV/HTML报告
- [ ] 添加仓库对比功能
- [ ] 集成AI代码质量分析
- [ ] 支持GitLab/Gitee等平台
- [ ] Web界面版本

### 📦 打包与部署

```bash
# 构建分发包
python setup.py sdist bdist_wheel

# 上传到PyPI
twine upload dist/*
```

### 🤝 贡献指南

欢迎提交Issue和PR！请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情。

### 📄 开源协议

本项目采用 [MIT License](LICENSE) 开源协议。

---

## 繁體中文

### 🎉 專案介紹

RepoInsight-AI 是一款**AI驅動的GitHub倉庫智能分析工具**，幫助開發者快速洞察開源專案的程式碼品質、社群健康度與發展趨勢。

**核心價值：**
- 🔍 深度分析任意GitHub倉庫的核心指標
- 📊 智能評估專案活躍度與維護狀態
- 💡 提供專業的技術選型建議
- ⚡ 零配置，開箱即用

### ✨ 核心特性

- 🎯 **智能分析** - 自動計算Star增速、社群健康度、活躍度評分
- 📈 **趨勢洞察** - 識別專案維護狀態
- 🏥 **健康評估** - 綜合評估程式碼品質、社群活躍度
- 🔥 **熱門發現** - 支援按語言篩選熱門倉庫
- 🎨 **精美輸出** - 使用Rich庫打造終端視覺化體驗

### 🚀 快速開始

#### 安裝步驟

```bash
git clone https://github.com/gitstq/RepoInsight-AI.git
cd RepoInsight-AI
pip install -r requirements.txt
```

#### 使用範例

```bash
# 分析指定倉庫
repoinsight analyze facebook/react

# 查看Python熱門倉庫
repoinsight trending Python -n 10
```

### 📄 開源協議

[MIT License](LICENSE)

---

## English

### 🎉 Introduction

RepoInsight-AI is an **AI-powered GitHub repository intelligent analysis tool** that helps developers quickly gain insights into open source projects' code quality, community health, and development trends.

**Core Values:**
- 🔍 Deep analysis of any GitHub repository's key metrics
- 📊 Intelligent assessment of project activity and maintenance status
- 💡 Professional technology selection advice
- ⚡ Zero configuration, ready to use out of the box

### ✨ Key Features

- 🎯 **Smart Analysis** - Auto-calculate star velocity, community health, activity score
- 📈 **Trend Insights** - Identify project maintenance status
- 🏥 **Health Assessment** - Comprehensive evaluation of code quality and community activity
- 🔥 **Trending Discovery** - Filter popular repositories by language
- 🎨 **Beautiful Output** - Rich terminal visualization experience

### 🚀 Quick Start

#### Installation

```bash
git clone https://github.com/gitstq/RepoInsight-AI.git
cd RepoInsight-AI
pip install -r requirements.txt
```

#### Usage

```bash
# Analyze a repository
repoinsight analyze facebook/react

# View trending Python repositories
repoinsight trending Python -n 10
```

### 📄 License

[MIT License](LICENSE)

---

<div align="center">

**Made with ❤️ by gitstq**

</div>
