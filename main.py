# author 贾治宝
# python version 3.7
import tkinter as tk
from tkinter.messagebox import showinfo
from windnd import hook_dropfiles
import os
import fitz

# 未处理问题：1、未将转换后的图片存储在相应文件夹。2、窗口图标未设置。3.打包为1个exe无法设置应用图标。4、菜单未设置。5、界面未优化。

# pdf列表
pdf_list = []


# 获取文件夹下所有PDF
def get_file(dir_name):
    docs = os.listdir(dir_name)
    print(dir_name + '文件夹下有以下文件：')
    print(docs)
    for doc in docs:
        doc_name = dir_name + '\\' + doc
        print('文件名：' + doc_name)
        if os.path.isdir(doc_name):
            print(f"{doc_name!r}文件夹类型，开始转子文件夹下所有PDF为JPG")
            get_file(doc_name)
        elif os.path.isfile(doc_name):
            if os.path.splitext(doc_name)[1] == '.pdf' or os.path.splitext(doc_name)[1] == '.PDF':  # 目录下包含.pdf的文件
                pdf_list.append(doc_name)
        else:
            print("文件夹下文件")
    print(pdf_list)


# 转换单个PDF为JPG。未解决问题：暂未存入相应文件夹。
def pdf2jpg(pdf_path):
    print('开始转换' + pdf_path)
    # 打开PDF，使用完毕要进行关闭
    pdf = fitz.open(pdf_path)

    print(os.path.splitext(pdf_path))
    pdf_name = os.path.splitext(pdf_path)[0]
    print('文件名：' + pdf_name + '页数:%d' % pdf.pageCount)
    # 创建文件夹目录
    if not os.path.exists(pdf_name):
        print(pdf_name + '不存在，开始创建')
        os.makedirs(pdf_name)

    # 将jpg存入文件夹
    for pg in range(pdf.pageCount):
        page = pdf[pg]
        rotate = int(0)
        # 每个尺寸的缩放系数为2，这将为我们生成分辨率提高四倍的图像。
        zoom_x = 2.0
        zoom_y = 2.0
        trans = fitz.Matrix(zoom_x, zoom_y).prerotate(rotate)
        pm = page.get_pixmap(matrix=trans, alpha=False)
        # 存入同PDF同名文件夹下。未解决问题PDF文件名需要为PDF名+数字
        pm.save('%s%d.jpg' % (pdf_name, pg + 1))
    # 关闭PDF
    pdf.close()


# 拖拽获取文件列表
def draggetfiles(files):
    print('拖拽文件字节流：%r' % files)
    # 获取文件名
    for file in files:
        # 文件名字节流转为GBK可读文件名
        path = ''.join(file.decode('gbk'))
        # 判断文件类型是否为文件夹
        if os.path.isdir(path):
            print(path + "是文件夹类型，开始转文件夹下所有PDF为JPG")
            get_file(path)
        # 判断文件类型是否为普通文件
        elif os.path.isfile(path):
            print(path + "是普通文件类型")
            # 判断文件类型是否为PDF
            if path.endswith('.PDF') or path.endswith('.pdf'):
                # 将PDF文件加入pdf_list
                pdf_list.append(path)
                print(path + '加入pdf_list')
            else:
                print(path + '非pdf格式文件，系统进行忽略操作')
        else:
            print(path + '是特殊文件类型，无法执行转换')

    for p in pdf_list:
        pdf2jpg(p)
    print(type(pdf_list))
    # 清空列表
    pdf_list.clear()
    showinfo('提示', '全部转换完毕')

# 程序入口
if __name__ == '__main__':
    root = tk.Tk()  # 创建窗口
    root.update()
    root.title("PDF转JPG V1.1.0")  # 设置标题
    root.geometry('320x300')  # 设置大小
    root.iconbitmap('pdf2img.ico')  # 设置窗口图标
    # 创建一个Canvas，设置其背景色为白
    theLabel = tk.Label(root, text="\n\n\n拖拽PDF到此\n转换为JPG\n\n\n乌审旗人民法院贾治宝制作", justify=tk.CENTER, compound=tk.CENTER,
                        font=("宋体", 18), fg="black")
    theLabel.pack()

    # 拖拽响应，获取PDF列表。
    hook_dropfiles(root, func=draggetfiles)  # 拖拽，回调
    print('拖拽功能已经设置')
    # 转换PDF列表为JPG
    root.mainloop()
