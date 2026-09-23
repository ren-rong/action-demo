电商订单服务自动化测试与 CI 实践
一个面向测试开发工程师的实践项目，基于简化的电商订单业务，使用 Python + pytest + pytest-cov 构建自动化测试体系，并通过 GitHub Actions 实现持续集成。
项目简介
本项目围绕电商订单核心链路，抽象出可独立测试的业务模块，覆盖订单创建、库存校验、折扣计算、订单总价结算等关键路径。所有测试通过 GitHub Actions 在每次 push / pull request 时自动触发，并输出测试覆盖率报告。
技术栈
- Python 3.10 / 3.11 / 3.12
- pytest
- pytest-cov
- GitHub Actions
项目结构
.
├── .github/workflows/python-ci.yml   # GitHub Actions CI 工作流
├── order_service.py                  # 业务逻辑：订单服务
├── test_order_service.py             # pytest 自动化测试用例
├── requirements.txt                  # 项目依赖
└── README.md                         # 项目说明
业务模块
order_service.py 实现了电商订单的核心流程：
      函数
      功能
      create_order
      创建订单，校验商品非空
      validate_inventory
      校验库存是否充足
      calculate_subtotal
      计算商品小计
      apply_discount
      根据优惠码计算折扣后金额
      calculate_order_total
      计算最终总价（折扣 + 税费）
      confirm_order
      完整下单确认流程
测试覆盖
test_order_service.py 共包含 11 条测试用例，覆盖：
- 正常下单流程
- 空订单异常处理
- 库存充足 / 库存不足
- 无折扣 / 有效折扣 / 无效折扣
- 含税总价计算
- 完整订单确认成功 / 失败
覆盖率报告
CI 流水线会自动生成覆盖率报告。最近一次运行可在 Actions 日志的 "Run tests with pytest and coverage" 步骤中查看，典型输出如下：
Name              Stmts   Miss  Cover   Missing
-------------------------------------------------
order_service.py     34      0   100%
-------------------------------------------------
TOTAL                34      0   100%
快速开始
本地运行
pip install -r requirements.txt
pytest -v
查看覆盖率
pytest -v --cov=order_service --cov-report=term-missing
生成 HTML 覆盖率报告
pytest --cov=order_service --cov-report=html
报告生成在 htmlcov/index.html。
CI/CD 说明
.github/workflows/python-ci.yml 配置如下：
- 触发条件：push 到 main 分支 或 pull_request 到 main 分支
- 运行环境：Ubuntu Latest
- 测试矩阵：Python 3.10 / 3.11 / 3.12 并行执行
- 执行内容：安装依赖 → 运行 pytest → 输出测试覆盖率
备注 【如何迁移到自己的项目】模版
1. 将本仓库文件上传至你的 GitHub 仓库根目录；
2. 将 order_service.py 替换为你的业务模块；
3. 将 test_order_service.py 替换为对应测试用例；
4. 确保 .github/workflows/python-ci.yml 路径正确；
5. 提交代码，在 Actions 页面查看运行结果。
