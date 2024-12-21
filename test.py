import time
from zefg60150_sdk import ZEFG60150Tool

def test_gripper():
    # 创建夹爪对象
    gripper = ZEFG60150Tool()
    
    # 测试串口查找
    print("=== 查找可用串口 ===")
    com_list = gripper.searchCom()
    print(f"可用串口列表: {com_list}")
    
    if not com_list:
        print("未找到可用串口")
        return
        
    # 选择第一个可用串口
    selected_com = com_list[1]
    
    # 测试串口连接
    print("\n=== 测试串口连接 ===")
    result = gripper.serialOperation(selected_com, baudRate=115200)
    if result != 1:
        print(f"串口连接失败: {result}")
        return
    print("串口连接成功")
    
    # 设置夹爪ID
    slave_id = 1
    
    try:
        # # 初始化夹爪
        # print("\n=== 初始化夹爪 ===")
        # result = gripper.initialize(slave_id)
        # if result != 1:
        #     print(f"初始化失败: {result}")
        #     return
        # print("初始化成功")
        # time.sleep(2)  # 等待初始化完成
        
        # 测试基本参数设置
        print("\n=== 测试基本参数设置 ===")
        
        # 设置速度
        print("设置速度为 50mm/s")
        result = gripper.setSpeed(slave_id, 30)
        if result != 1:
            print(f"设置速度失败: {result}")
            return
        
        # 设置电流
        print("设置电流为 0.4A")
        result = gripper.setCurrent(slave_id, 0.4)
        if result != 1:
            print(f"设置电流失败: {result}")
            return
        
        # 测试夹爪控制和状态获取
        print("\n=== 测试夹爪控制和状态获取 ===")
        
        # 测试序列：打开->获取状态->夹紧->获取状态
        test_positions = [60, 30, 0, 45]  # 测试不同位置
        
        for pos in test_positions:
            print(f"\n移动到位置 {pos}mm")
            result = gripper.setPosition(slave_id, pos)
            if result != 1:
                print(f"设置位置失败: {result}")
                continue
                
            # 等待运动完成
            time.sleep(2)
            
            # 获取状态信息
            status = gripper.getStatus(slave_id)
            position = gripper.getPosition(slave_id)
            current = gripper.getCurrent(slave_id)
            
            print(f"当前状态: {status}")
            print(f"当前位置: {position}mm")
            print(f"当前电流: {current}A")
            
    except Exception as e:
        print(f"测试过程中出现错误: {str(e)}")
    
    finally:
        # 关闭串口连接
        print("\n=== 关闭串口连接 ===")
        gripper.serialOperation(selected_com, status=False)
        print("测试完成")

if __name__ == "__main__":
    test_gripper()