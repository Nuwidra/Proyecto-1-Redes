from tkinter import *

menu_window = Tk()

# set the title
menu_window.title("Protocol Selector")

# set the size
menu_window.geometry('300x100')

# create buttons to select protocol
sr_button = Button(menu_window, text="Selective Repeat")
sr_button.grid(column=0, row=0)

gbn_button = Button(menu_window, text="Go Back N")
gbn_button.grid(column=1, row=0)

utopia_button = Button(menu_window, text="Utopia")
utopia_button.grid(column=2, row=0)

# create button to exit
exit_button = Button(menu_window, text="Exit", command=menu_window.destroy)
exit_button.grid(column=1, row=1)

# action to be performed when selective repeat button is clicked
def sr_button_clicked():
    menu_window.destroy()
    import SelectiveRepeat.SRGUI    # import the GUI of selective repeat protocol




# run the main menu window
menu_window.mainloop()