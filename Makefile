.PHONY: install test clean build lint format

# 安装依赖
install:
	pip install -r requirements.txt

# 安装开发依赖
dev-install:
	pip install -r requirements.txt
	pip install pytest pytest-cov black flake8

# 运行测试
test:
	python -m pytest tests/ -v

# 运行测试并生成覆盖率报告
test-cov:
	python -m pytest tests/ -v --cov=repoinsight --cov-report=html --cov-report=term

# 代码格式化
format:
	black repoinsight.py tests/

# 代码检查
lint:
	flake8 repoinsight.py tests/

# 构建分发包
build:
	python setup.py sdist bdist_wheel

# 清理构建产物
clean:
	rm -rf build/ dist/ *.egg-info/ .pytest_cache/ .coverage htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# 本地安装
local-install:
	pip install -e .

# 运行示例
example:
	python repoinsight.py analyze facebook/react

# 帮助
help:
	@echo "可用命令:"
	@echo "  make install      - 安装依赖"
	@echo "  make dev-install  - 安装开发依赖"
	@echo "  make test         - 运行测试"
	@echo "  make test-cov     - 运行测试并生成覆盖率报告"
	@echo "  make format       - 格式化代码"
	@echo "  make lint         - 检查代码"
	@echo "  make build        - 构建分发包"
	@echo "  make clean        - 清理构建产物"
	@echo "  make local-install- 本地安装"
	@echo "  make example      - 运行示例"
