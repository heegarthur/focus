import tkinter as tk
import threading
import time
import os

COUNTDOWN_SECONDS = int(input("how many seconds"))
shutdown_triggered = False

def shutdown():
    print("[!] SYSTEM SHUTDOWN [!]")
    os.system("shutdown /s /t 1") 

def start_shutdown_countdown():
    global shutdown_triggered
    if shutdown_triggered:
        return
    shutdown_triggered = True

    def countdown():
        for i in range(COUNTDOWN_SECONDS, 0, -1):
            print(f"[!] Shutdown in {i} seconden...")
            timer_label.config(text=f"⚠️ SYSTEM IS CLOSING IN {i} SECONDS")
            time.sleep(1)
        shutdown()

    threading.Thread(target=countdown, daemon=True).start()

def check_focus_loop():
    once = 0
    while True:
        time.sleep(1)
        if shutdown_triggered:
            break
        try:
            if not root.focus_displayof():  
                print("[!] FOCUS LOSED")
                shutdown()
                break
        except:
            break
        if once == 0:
            once = 1
            start_shutdown_countdown()

def on_close_attempt():
    print("[!] DETECTED CLOSING TRY, SHUTDOWN")
    shutdown()

def alt_f4_handler(event):
    print("[!] ALT+F4 DETECTED, SHUTDOWN")
    shutdown()
    return "break"  



root = tk.Tk()
root.title("FOCUS SECURED")
root.configure(bg="black")
root.attributes("-fullscreen", True)
root.state('zoomed')
root.attributes('-topmost', True) 
root.protocol("WM_DELETE_WINDOW", on_close_attempt)
root.bind("<Alt-F4>", alt_f4_handler)

info_label = tk.Label(root,
    text="🛑 don't close this window\nlose focus = shutdown.",
    fg="white", bg="black", font=("Arial", 24)
)
info_label.pack(pady=40)

timer_label = tk.Label(root, text="", fg="red", bg="black", font=("Arial", 32, "bold"))
timer_label.pack()

threading.Thread(target=check_focus_loop, daemon=True).start()

root.mainloop()

