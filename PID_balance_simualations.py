import serial
import serial.tools.list_ports
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque

# 🔹 Tự động tìm cổng COM
def find_com_port():
    ports = list(serial.tools.list_ports.comports())
    if not ports:
        print("Không tìm thấy cổng COM nào. Hãy kiểm tra kết nối USB!")
        return None
    for port in ports:
        print(f"Tìm thấy cổng: {port.device}")
    return ports[0].device  # Chọn cổng đầu tiên

# 🔹 Kết nối với Serial
com_port = find_com_port()
if com_port:
    ser = serial.Serial(com_port, 115200, timeout=1)
else:
    exit()

# 🔹 Khởi tạo dữ liệu vẽ đồ thị
time_window = 100  # Số điểm hiển thị trên đồ thị
data_p = deque([0] * time_window, maxlen=time_window)
data_i = deque([0] * time_window, maxlen=time_window)
data_d = deque([0] * time_window, maxlen=time_window)
data_pv = deque([0] * time_window, maxlen=time_window)
time_axis = deque(range(time_window), maxlen=time_window)

# 🔹 Tạo đồ thị
fig, ax = plt.subplots()
ax.set_ylim(-10, 10)  # Giới hạn giá trị PID (tùy chỉnh)
ax.set_xlim(0, time_window)
ax.set_xlabel("Thời gian")
ax.set_ylabel("Giá trị")
ax.set_title("PID Real-time Plot")

# 🔹 Khởi tạo đường vẽ
line_p, = ax.plot(time_axis, data_p, label="P", color="red")
line_i, = ax.plot(time_axis, data_i, label="I", color="green")
line_d, = ax.plot(time_axis, data_d, label="D", color="blue")
line_pv, = ax.plot(time_axis, data_pv, label="PV", color="orange")
ax.legend()

# 🔹 Hàm cập nhật dữ liệu từ Serial
def update(frame):
    global data_p, data_i, data_d, data_pv

    if ser.in_waiting:
        try:
            raw_data = ser.readline().decode("utf-8").strip()
            values = raw_data.split(",")  # Giả sử dữ liệu gửi dưới dạng "P,I,D,pv"
            if len(values) == 4:
                p, i, d, pv = map(float, values)
                data_p.append(p)
                data_i.append(i)
                data_d.append(d)
                data_pv.append(pv)
                time_axis.append(time_axis[-1] + 1)

                # Cập nhật đồ thị
                line_p.set_ydata(data_p)
                line_i.set_ydata(data_i)
                line_d.set_ydata(data_d)
                line_pv.set_ydata(data_pv)
                line_p.set_xdata(time_axis)
                line_i.set_xdata(time_axis)
                line_d.set_xdata(time_axis)
                line_pv.set_xdata(time_axis)
        except:
            pass  # Bỏ qua lỗi khi parsing

    return line_p, line_i, line_d, line_pv

# 🔹 Vẽ đồ thị động
ani = animation.FuncAnimation(fig, update, interval=100)
plt.show()
