# GitHub Actions Python 企业级业务测试示例

这个项目演示了一个贴近真实业务的自动化测试流程：一个简化的电商订单服务。

## 业务模块

- `order_service.py`：订单核心逻辑
  - 创建订单
  - 库存校验
  - 折扣计算
  - 订单总价计算（含税费）
  - 完整下单确认流程

## 测试覆盖

- 正常下单流程
- 空订单异常
- 库存充足 / 库存不足
- 无折扣 / 有效折扣 / 无效折扣
- 含税总价计算
- 端到端订单确认成功 / 失败

## GitHub Actions 工作流

`.github/workflows/python-ci.yml`：

- 在 Ubuntu 环境中运行
- 使用矩阵策略同时测试 Python 3.10 / 3.11 / 3.12
- 自动安装 `requirements.txt` 依赖
- 运行 `pytest -v`

## 如何迁移到自己的仓库

1. 把本目录下的所有文件上传到你的 GitHub 仓库根目录。
2. 确保 `.github/workflows/python-ci.yml` 路径正确。
3. 在 GitHub 仓库页面点击 **Actions**，即可看到运行记录。

## 本地运行

```bash
pip install -r requirements.txt
pytest -v
```
