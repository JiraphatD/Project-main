from tkinter import *
from tkinter import messagebox
from random import choices


box, item, rate_box, sr_ssr_box, sr_ssr_rate, ssr_box, ssr_rate, grade = [], [], [], [], [], [], [], []


def clears():
    """function clear""" #ฟังก์ชันที่ใช้ในการลบข้อความที่แสดงการรับค่าและเปิดปุ่ม get เพื่อป้องกันการกดที่ผิดพลาด
    text_label.destroy() #ลบข้อความที่แสดงผลว่ารับค่าแล้ว
    button_get['state'] = NORMAL #เปิดปุ่ม Get


def get():
    """function get value""" #เป็นฟังก์ชันที่ใช้ในการเก็บค่าที่รับมาเพื่อใช้ในการคำวนวณ
    global text_label

    tier = tier_t.get()
    if tier == 1:
        tier = "R"
    elif tier == 2:
        tier = "SR"
    elif tier == 3:
        tier = "SSR"
    elif tier == 4:
        tier = "None"
    elif tier == 0:
        messagebox.showerror("Error Tier", "Please select tier")

    if item_t.get() == "":
        messagebox.showerror("Error Item", "Please enter item")

    if tier != 0 and item_t.get() != "":
        text_label = Label(root, text="Save    Item:  %s      Tier:  %s       Rate:  %s"%(item_t.get(), tier, rate_t.get()), font = 'dubai 12 bold', fg = 'salmon')
        print("Get values    Item:  %s      Tier:  %s       Rate:  %s"%(item_t.get(), tier, rate_t.get()))

        box.append(item_t.get())
        rate_box.append(float(rate_t.get()))
        grade.append(tier)


        if tier == "SR" or tier == "SSR":#ประกัน 10
                    sr_ssr_box.append(item_t.get())
                    sr_ssr_rate.append(float(rate_t.get()))
                    if tier == "SSR": #ประกันใหญ่
                        ssr_box.append(item_t.get())
                        ssr_rate.append(float(rate_t.get()))

        item_t.delete(0, END) #ลบส่วนที่กรอบใน item
        rate_t.delete(0, END) #ลบส่วนที่กรอบใน rate
        text_label.pack()

        sampling_get['state'] = NORMAL #เปิดปุ่ม Sampling
        button_get['state'] = DISABLED #ปิดปุ่ม Get ป้องกันการกดผิด


def sampling_option():
    """Sampling Option""" #ใช้ในการเลือกรูปแบบของการ sampling
    global garuntee_button
    global normal_button
    normal_button = Button(root, text=' Normal  ', font = 'dubai 10 bold', command=sampling_n, bg = 'oldlace', fg = 'salmon', width=10)
    normal_button.pack()
    garuntee_button = Button(root, text='Guarantee', font = 'dubai 10 bold', command=sampling_g, bg = 'tomato', fg = 'snow', width=10)
    garuntee_button.pack()


def sampling_n():
    """Normal Sampling""" #ฟังก์ชัน การสุ่มแบบทั่วไป โดยไม่มีเงื่อนไขมาเกี่ยวข้อง
    garuntee_button['state'] = DISABLED #ปิดปุ่ม garuntee
    Label(root, text="Normal Random", font = 'dubai 10 bold', fg = 'salmon').pack()

    def sampling_calculate_n():
        """Normal calculate"""
        get = []

        roll_all = int(roll_t.get())

        count = 0
        keeper = []
        printer = []


        for _ in range(1, roll_all+1):
            get.append(choices(box, weights=rate_box, k=1))


        for unit in get:
            if unit not in keeper:
                keeper.append(unit)
        for j in keeper:
            for k in get:
                if j == k:
                    count += 1
            printer.append(count)
            count = 0
        keeper = [i[0] for i in keeper]
        for l in range(len(keeper)):
            print("Get   %s"%keeper[l], end = " ")
            print("  %s"%printer[l]+'  piece')


    Label(root, text="How many roll?", font = 'dubai 10 bold', fg = 'salmon').pack()
    roll_t = Entry(root)
    roll_t.pack()

    normal_submit = Button(root, text='Submit', font = 'dubai 10 bold', command=sampling_calculate_n,  bg = 'tomato', fg = 'snow', width=10)
    normal_submit.pack()


def sampling_g():
    """Garuntee Sampling""" #ฟังก์ชัน การสุ่มแบบมีเงื่อนไขมาเกี่ยวข้อง โดยจะเป็น รูปแบบ R, SR, SSR โดยการสุ่มทุก 10 ครั้งจะรับประกัน SR หรือ SSR 1 อัน
    normal_button['state'] = DISABLED #ปิดปุ่ม ์normal
    Label(root, text="Guarantee Random", font = 'dubai 10 bold', fg = 'salmon').pack()


    def sampling_calculate_g():
        """Garuntee calculate"""
        if len(sr_ssr_box) == 0 :
            messagebox.showerror("Error SR", "Please enter SR")
        elif len(ssr_box) == 0:
            messagebox.showerror("Error SSR", "Please enter SSR")
        else:
            get = []

            garuntee = 0
            garuntee_option = int(garuntee_option_t.get())
            roll_all = int(roll_t.get())

            count = 0
            keeper = []
            printer = []

            roll_garuntee = 10 #การสุ่มทุก 10 ครั้งจะรับประกัน SR หรือ SSR 1 อัน สามารถปรับเปลี่ยนได้


            for roll in range(1, roll_all+1):
                garuntee += 1
                if roll % roll_garuntee != 0:
                    if garuntee == garuntee_option: #ได้ SSR แน่นอน การันตีจะรีกับไปที่ 0
                        get.append(choices(ssr_box, weights=ssr_rate, k=1)) # สุ่ม SSR
                        garuntee = 0
                    else:
                        roll_correct = choices(box, weights=rate_box, k=1)
                        get.append(roll_correct)
                        if roll_correct in ssr_box: #ถ้าได้ SSR การันตีจะรีกับไปที่ 0
                            garuntee = 0
                else:
                    if garuntee == garuntee_option: #ได้ SSR แน่นอน การันตีจะรีกับไปที่ 0
                        get.append(choices(ssr_box, weights=ssr_rate, k=1)) # สุ่ม SSR
                        garuntee = 0
                    else:
                        roll_correct = choices(sr_ssr_box, weights=sr_ssr_rate, k=1)
                        get.append(roll_correct) # สุ่ม SR
                        if roll_correct in ssr_box: #ถ้าได้ SSR การันตีจะรีกับไปที่ 0
                            garuntee = 0


            for unit in get:
                if unit not in keeper:
                    keeper.append(unit)
            for j in keeper:
                for k in get:
                    if j == k:
                        count += 1
                printer.append(count)
                count = 0
            keeper = [i[0] for i in keeper]
            for l in range(len(keeper)):
                print("Get   %s"%keeper[l], end = " ")
                print("  %s"%printer[l]+'  piece')



    Label(root, text="Guarantee Option", font = 'dubai 10 bold', fg = 'salmon').pack()
    garuntee_option_t = Entry(root)
    garuntee_option_t.pack()

    Label(root, text="How many roll?", font = 'dubai 10 bold', fg = 'salmon').pack()
    roll_t = Entry(root)
    roll_t.pack()

    garuntee_submit = Button(root, text='Submit', command=sampling_calculate_g, font = 'dubai 10 bold', bg = 'tomato', width=10,fg = 'snow')
    garuntee_submit.pack()


#ส่วนที่ใช้ในการตั้งชื่อและปรับขนาด
root = Tk()
root.title("Gacha_simulator")
root.geometry("500x800")


#ส่วนของการกรอก Item
Label(root, text="Item", font = 'dubai 12 bold', fg = 'salmon').pack()
item_t = Entry(root, width=40)
item_t.pack()


#่ส่วนของการกรอก Rate
Label(root, text="Rate", font = 'dubai 12 bold', fg = 'salmon').pack()
rate_t = Entry(root, width=40)
rate_t.pack()


#ส่วนของการเลือก Tier ถ้าเราต้องการสุ่มแบบทั่วไปโดยไม่มีเงื่อนไข ให้เลือก None
tier_t = IntVar()

Label(root, text="Tier", font = 'dubai 12 bold', fg = 'salmon').pack()
Radiobutton(root, text='    R    ', variable=tier_t, value=1, font = 'dubai 10 bold', fg = 'salmon').pack()
Radiobutton(root, text='   SR   ', variable=tier_t, value=2, font = 'dubai 10 bold', fg = 'salmon').pack()
Radiobutton(root, text='  SSR  ', variable=tier_t, value=3, font = 'dubai 10 bold', fg = 'salmon').pack()
Radiobutton(root, text='None ', variable=tier_t, value=4, font = 'dubai 10 bold', fg = 'salmon').pack()


Label(root, text=" ").pack()


#ปุ่ม Get
button_get = Button(root, text=' Get  ', font = 'dubai 10 bold', command = get, bg = 'tomato', fg = 'snow', width=10)
button_get.pack()

#ปุ่ม Clear
button_clear = Button(root, text='Clear', font = 'dubai 10 bold', command = clears, bg = 'oldlace', width=10, fg = 'salmon')
button_clear.pack()


Label(root, text=" ").pack()


#ปุ่ม Sampling
sampling_get = Button(root, text='Sampling', font = 'dubai 10 bold', command = sampling_option, bg = 'tomato', fg = 'snow', width=10)
sampling_get['state'] = DISABLED
sampling_get.pack()


root.mainloop()
