import tkinter as tk
import threading
import time
import os

# === Instellingen ===
COUNTDOWN_SECONDS = 10
shutdown_triggered = False

# === Shutdown-functie die je kunt vervangen tijdens testen ===
def shutdown():
    print("[!] SYSTEM SHUTDOWN [!]")
    os.system("shutdown /s /t 1")  # Zet deze aan als je klaar bent

# === Countdown-functie ===
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

# === Focus-verlies detectie loop ===
def check_focus_loop():
    while True:
        time.sleep(1)
        if shutdown_triggered:
            break
        try:
            if not root.focus_displayof():  # Verlies van focus
                print("[!] FOCUS LOSED")
                shutdown()
                break
        except:
            break

# === Sluitpoging (Alt+F4 of muis) ===
def on_close_attempt():
    print("[!] DETECTED CLOSING TRY, SHUTDOWN")
    shutdown()

# === GUI Setup ===
root = tk.Tk()
root.title("FOCUS SECURED")
root.configure(bg="black")
root.attributes("-fullscreen", True)
root.protocol("WM_DELETE_WINDOW", on_close_attempt)

info_label = tk.Label(root,
    text="🛑 don't close this window\nlose focus = shutdown.",
    fg="white", bg="black", font=("Arial", 24)
)
info_label.pack(pady=40)

timer_label = tk.Label(root, text="", fg="red", bg="black", font=("Arial", 32, "bold"))
timer_label.pack()

# Start focus-check in achtergrond
threading.Thread(target=check_focus_loop, daemon=True).start()

# Start GUI loop
root.mainloop()
