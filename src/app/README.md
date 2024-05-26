# 采用MVC架构
- Models 模型 --- 逻辑业务
- Views 视图 --- UI界面
- Controller 控制器 --- 请求处理‘

执行顺序
1. Controller收到ui界面的请求
2. 调用Service层的逻辑业务
   1. Service 进行业务处理
   2. 有需要的数据访问向数据库访问
3. 响应结果给Views

游戏脚本暂时不需要数据库访问，所以不需要DAO层
