import tkinter as tk

window = tk.Tk()

window.geometry("480x350")
window.title("YouTube")

main_screen_frame = tk.Frame(window, width=450, height=253, bd=0, highlightbackground="black",
                             highlightcolor="black", highlightthickness=1)
main_screen_frame.pack(padx=15, pady=15)

buttons_frame = tk.Frame(window, width=450, bg="grey")
buttons_frame.pack()

window.mainloop()
