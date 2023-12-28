## 采用TDD(测试驱动开发)开发
基于单元测试的开发，将功能分解成阶段，每个阶段有多个任务，当任务之间发生交互(依赖)时，这些任务组成一个阶段
1. 先写test -> error
2. 修复error -> success run test
3. 重构 -> better
4. 重复以上
## 功能思路
用一个实例变量记录场景

场景对应任务

按**场景**封装逻辑方法,并且尽可能不使用sleep和while，嵌套在三层以内,不使用魔法数字

通过taskMap记录{任务名称:任务函数}默认需要执行的任务

### 例子
## TODO:
### Base 基础功能模块
- [x] [准备(是否退出战斗,是否更换阵容)](src/tasks/base/ready/task.py)
- [x] [结算(失败后是否再次挑战)](src/tasks/base/settle/task.py)
- [x] [阵容锁定/解锁(是否锁定)](src/tasks/base/LIneUpLock/task.py)
- [x] [阵容预设御魂更换(分组序号,预设序号,式神录图标【可选】)](src/tasks/base/changeSoul/task.py)

### 综合功能模块

