from wasmer import engine, Store, Module, Instance, ImportObject

# 加载 Wasm 字节码
with open('./main.wasm', 'rb') as wasm_file:
    wasm_bytes = wasm_file.read()

# 使用 JIT 引擎创建存储
store = Store(engine.JIT())

# 创建模块
module = Module(store, wasm_bytes)

# 创建实例
import_object = ImportObject()
instance = Instance(module, import_object)

# 调用 "encode" 函数
result = instance.exports.encode(1231243124, 312431423214)

print("Result:", result)