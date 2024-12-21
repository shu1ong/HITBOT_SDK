import serial
import serial.tools.list_ports
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
import struct

def float_to_registers(float_value):
    """将浮点数转换为两个寄存器值
    Args:
        float_value: 输入的浮点数
    Returns:
        list: 包含两个无符号短整型的列表
    """
    packed = struct.pack('>f', float_value)  # 转换为大端序字节
    registers = struct.unpack('>HH', packed)  # 解包为两个无符号短整型
    return list(registers)

def registers_to_float(registers):
    """将两个寄存器值转换为浮点数
    Args:
        registers: 包含两个寄存器值的列表或元组
    Returns:
        float: 转换后的浮点数
    """
    raw_data = struct.pack('>HH', registers[0], registers[1])
    return struct.unpack('>f', raw_data)[0]

class ZEFG60150Tool:
    def __init__(self):
        self.master = None
        self.status_dict = {
            0: '到位',
            1: '运动中', 
            2: '夹持中',
            3: '掉落'
        }
    
    #################
    # 通用功能 
    #################
    
    def searchCom(self):
        """查询可用的串口"""
        return [str(port[0]) for port in list(serial.tools.list_ports.comports())]

    def serialOperation(self, com, baudRate=115200, status=True):
        """串口操作
        Args:
            com: 串口号
            baudRate: 波特率
            status: 开关状态（打开：True，关闭：False）
        Returns:
            int or str: 成功返回1，失败返回异常信息
        """
        try:
            if status:
                self.master = modbus_rtu.RtuMaster(
                    serial.Serial(port=com, 
                                baudrate=int(baudRate), 
                                bytesize=8, 
                                parity='N', 
                                stopbits=1))
                self.master.set_timeout(0.1)
                self.master.set_verbose(True)
            else:
                self.master._do_close()
            return 1
        except Exception as exc:
            return str(exc)

    def _check_connection(self):
        """检查通讯连接状态"""
        if not self.master:
            raise ConnectionError("通讯未连接")

    #################
    # 控制功能
    #################

    def initialize(self, salveId):
        """手动初始化
        Args:
            salveId: 夹爪站点id
        """
        try:
            self._check_connection()
            self.master.execute(salveId, cst.WRITE_SINGLE_REGISTER, 0x0000, output_value=1)
            return 1
        except Exception as exc:
            return str(exc)

    def setPosition(self, salveId, position):
        """设置夹持位置
        Args:
            salveId: 夹爪站点id
            position: 目标位置(0-60mm)
        """
        try:
            self._check_connection()
            value = float_to_registers(float(position))
            self.master.execute(salveId, cst.WRITE_MULTIPLE_REGISTERS, 0x0002, output_value=value)
            return 1
        except Exception as exc:
            return str(exc)

    def setSpeed(self, salveId, speed):
        """设置夹持速度
        Args:
            salveId: 夹爪站点id
            speed: 运行速度(2-200mm/s)
        """
        try:
            self._check_connection()
            value = float_to_registers(float(speed))
            self.master.execute(salveId, cst.WRITE_MULTIPLE_REGISTERS, 0x0004, output_value=value)
            return 1
        except Exception as exc:
            return str(exc)

    def setCurrent(self, salveId, current):
        """设置夹持电流
        Args:
            salveId: 夹爪站点id
            current: 夹持电流(0.25-0.5A)
        """
        try:
            self._check_connection()
            value = float_to_registers(float(current))
            self.master.execute(salveId, cst.WRITE_MULTIPLE_REGISTERS, 0x0006, output_value=value)
            return 1
        except Exception as exc:
            return str(exc)

    #################
    # 状态反馈功能
    #################

    def getStatus(self, salveId):
        """获取夹持状态
        Args:
            salveId: 夹爪站点id
        Returns:
            str: 状态描述
        """
        try:
            self._check_connection()
            readBuf = self.master.execute(salveId, cst.READ_HOLDING_REGISTERS, 0x0041, 1)
            return self.status_dict[readBuf[0]]
        except Exception as exc:
            return str(exc)

    def getPosition(self, salveId):
        """获取当前位置
        Args:
            salveId: 夹爪站点id
        Returns:
            float: 当前位置值
        """
        try:
            self._check_connection()
            readBuf = self.master.execute(salveId, cst.READ_HOLDING_REGISTERS, 0x0042, 2)
            position = registers_to_float(readBuf)
            return round(position, 2)
        except Exception as exc:
            return str(exc)

    def getCurrent(self, salveId):
        """获取当前电流
        Args:
            salveId: 夹爪站点id
        Returns:
            float: 当前电流值
        """
        try:
            self._check_connection()
            readBuf = self.master.execute(salveId, cst.READ_HOLDING_REGISTERS, 0x0046, 2)
            return registers_to_float(readBuf)
        except Exception as exc:
            return str(exc)

    #################
    # 参数配置功能
    #################

    def setSalveId(self, oldId, newId):
        """修改夹爪站点ID
        Args:
            oldId: 当前ID
            newId: 新ID(1-247)
        """
        try:
            self._check_connection()
            self.master.execute(oldId, cst.WRITE_SINGLE_REGISTER, 0x0080, output_value=newId)
            return 1
        except Exception as exc:
            return str(exc)

    def setBaudRate(self, salveId, baudrate):
        """设置波特率
        Args:
            salveId: 夹爪站点ID
            baudrate: 波特率代码(0-6)
                0: 9600
                1: 19200
                2: 38400
                3: 57600
                4: 115200
                5: 153600
                6: 256000
        """
        try:
            self._check_connection()
            self.master.execute(salveId, cst.WRITE_SINGLE_REGISTER, 0x0081, output_value=baudrate)
            return 1
        except Exception as exc:
            return str(exc)

    def saveParams(self, salveId):
        """保存参数"""
        try:
            self._check_connection()
            self.master.execute(salveId, cst.WRITE_SINGLE_REGISTER, 0x0084, output_value=1)
            return 1
        except Exception as exc:
            return str(exc)

    def restoreDefault(self, salveId):
        """恢复默认参数"""
        try:
            self._check_connection()
            self.master.execute(salveId, cst.WRITE_SINGLE_REGISTER, 0x0085, output_value=1)
            return 1
        except Exception as exc:
            return str(exc)