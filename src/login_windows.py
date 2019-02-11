import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import account_types
import account
import question_type_select as instrWindow
import question_set_panel as studentWindow
from tkinter import *
# from winsound import * # This breaks on any non-windows platform

class LoginWindow(tk.Frame):
    '''A class to represent a login window; toplevel window which contains UI for logging in as users.'''

    def __init__(self, master):
        '''(LoginWindow, Tk) -> NoneType
        Initialize a new login window with the given parameters.
        '''
        super(LoginWindow, self).__init__()      
        self.master = master
        self.parent = self.master
        # Initial mainframe in which we place all other frames into.
        self._mainframe = ttk.Frame(root, padding="3 3 3 3")
        self._mainframe.grid(column=0, row=4, sticky=(tk.N, tk.W, tk.E, tk.S))
        self._mainframe.columnconfigure(100, weight=1)
        self._mainframe.rowconfigure(100, weight=1) 
        self.initUserLoginFrames()
        
        self._miscframe = ttk.Frame(root, padding="3 3 3 3")
        self._miscframe.grid(column=0, row=5, sticky=(tk.N, tk.W, tk.E, tk.S), columnspan=1)
        
        '''
        # for music
        play = lambda: PlaySound('sound\shrek_2_all_star_theme_song.wav', SND_FILENAME)
        button = ttk.Button(root, text = 'Play Green Goblin Theme Song', command = play)
        button.grid(row=5, column=0, sticky=(tk.E, tk.W), columnspan=2)
		'''
		
        # for logo
        logo_filepath = "graphics/green_goblin_symbol.gif"
        img = tk.PhotoImage(file = logo_filepath)
        logo = tk.Label(root, image=img)
        logo.photo = img
        logo.grid(row=1, column=0, rowspan=1, columnspan=1)

        
        # for title with image
        logo_filepath = "graphics/green-goblin-title.gif"
        img = tk.PhotoImage(file = logo_filepath)
        logo = tk.Label(root, image=img)
        logo.photo = img
        logo.grid(row=0, column=0, rowspan=1, columnspan=1)        
        
        # for fade button
        fadebutton = tk.Button(root, text="Click to fade away", command=self.quit)
        fadebutton.grid(row=6, column=0, sticky=(tk.E, tk.W), columnspan=3)

    # the following two functions are for the fade effect/button
    def quit(self):
        self.fade_away()

    def fade_away(self):
        alpha = self.parent.attributes("-alpha")
        if alpha > 0:
            alpha -= .1
            self.parent.attributes("-alpha", alpha)
            self.after(100, self.fade_away)
        else:
            self.parent.destroy()         

    def initUserLoginFrames(self):
        '''(LoginWindow) -> NoneType
        Initialize the intro frame, as well as student and instructor login 
        frames.
        '''
        # Dict to store the frames.
        self._subframes = {}

        # Create all frames and store them in a dict so we can grab them when
        # we need them.
        self._subframes["intro"] = IntroFrame(self._mainframe, self)
        self._subframes["intro"].grid(row=0, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self._subframes["loginStudent"] = LoginFrame(self._mainframe, self, account_types.AccountType.S)
        self._subframes["loginStudent"].grid(row=0, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self._subframes["loginInstructor"] = LoginFrame(self._mainframe, self, account_types.AccountType.I)
        self._subframes["loginInstructor"].grid(row=0, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))

        # This is the initially shown frame.
        self.showFrame("intro")

    def showFrame(self, frameName):
        '''(LoginWindow, str) -> NoneType
        Raises the frame mapping from the given name to top level visibility.
        '''
        frame = self._subframes[frameName];
        frame.tkraise()

    def returnToLogin(self, oldWindow):
        '''(LoginWindow, Frame) -> NoneType
        This is used by child classes to prompt a logout, then cleanup and
        return to this login screen.
        '''
        # Warn the user that they are logging out.
        if messagebox.askyesno("Logging Out", 
                               "Are you sure you want to log out?"):    
            oldWindow.destroy()
            self.master.deiconify()

class IntroFrame(tk.Frame):
    '''A class to represent an intro frame that asks users to specify what type of user they are logging in as.'''

    def __init__(self, parent, controller):
        '''(IntroFrame, parent, controller) -> NoneType
        Initialize a new intro frame with the given parameters.
        '''        
        tk.Frame.__init__(self, parent, relief='raised', borderwidth=10, background="green")
        self.controller = controller

        # Widget declaration.
        userSelectLabel = ttk.Label(self, text="Are you signing in as an Instructor or Student?", font=("Tahoma", 12), 
                                    background="lightgreen")
        logoLabel = ttk.Label(self, text="Green Goblins Software Solutions 2017 Ltd.", font=("Tahoma", 6), 
                              background="lightgreen")
        introSeparator = ttk.Separator(self, orient=tk.HORIZONTAL)
        studentLoginBtn = ttk.Button(self, text="Login as a Student", 
                                     command=lambda: self.controller.showFrame("loginStudent"))
        instrLoginBtn = ttk.Button(self, text="Login as an Instructor", 
                                   command=lambda: self.controller.showFrame("loginInstructor"))

        # For title, parent is specially set to root so it won't change with the frames.
        title = tk.Label(root, text="The Green Goblin's Homework App", font=("Arial", 12))
        title.grid(row=0, column=0, sticky=(tk.N, tk.S), columnspan=2)

        # Grid management for widgets.
        userSelectLabel.grid(row=2, column=0, sticky=(tk.N, tk.S), columnspan=2)
        introSeparator.grid(row=3, column=0, sticky=(tk.E, tk.W), columnspan=2)
        studentLoginBtn.grid(row=4, column=0, sticky=(tk.E, tk.W))
        instrLoginBtn.grid(row=4, column=1, sticky=(tk.E, tk.W))
        logoLabel.grid(row=5, column=0, columnspan=2)    

        # Global padding so widgets aren't too close.
        for child in self.winfo_children():
            child.grid_configure(padx=3, pady=9)        

class LoginFrame(tk.Frame):
    '''A class to represent a frame dynamically containing and redirecting users to correct windows based on login credentials and user type. Also handles login verification logic.'''

    def __init__(self, parent, controller, userType):
        '''(LoginFrame, parent, controller, AccountType Enum) -> NoneType
        Initialize a new login frame with the given parameters.
        '''
        tk.Frame.__init__(self, parent)
        self.controller = controller  
        self.username = tk.StringVar()
        password = tk.StringVar()

        # Shave off the 's' when we display the enum so it looks nicer.
        userTypeLabel = ttk.Label(self, text=(userType.value[:-1] + " Login"), font=("Tahoma", 14))
        namePromptLabel = ttk.Label(self, text="Username :")
        passPromptLabel = ttk.Label(self, text="Password :")

        # Entry box prompts we read user/pass from.
        self.userNameEntry = ttk.Entry(self, textvariable=self.username)
        self.userPassEntry = ttk.Entry(self, textvariable=password)

        # Buttons which redirect to appropriate toplevels or frames.
        backBtn = ttk.Button(self, text="Return to Menu", command=lambda: self.controller.showFrame("intro"))
        loginBtn = ttk.Button(self, text="Login", command=lambda: self.try_login(self.username.get(),
                                                                                 password.get(),
                                                                                 userType))
        registBtn = ttk.Button(self, text="Register as New User",
                               command=lambda: self.try_register_account(self.username.get(),
                                                                         password.get(),
                                                                         userType))

        # Grid management.
        userTypeLabel.grid(row=0, column=0, sticky=(tk.E, tk.W), columnspan=2)
        namePromptLabel.grid(row=1, column=0, sticky=(tk.E))
        passPromptLabel.grid(row=2, column=0, sticky=(tk.E))
        self.userNameEntry.grid(row=1, column=1, sticky=(tk.E, tk.W))
        self.userPassEntry.grid(row=2, column=1, sticky=(tk.E, tk.W))
        backBtn.grid(row=3, column=0, sticky=(tk.E, tk.W))
        loginBtn.grid(row=3, column=1, sticky=(tk.E, tk.W))
        registBtn.grid(row=4, column=0, sticky=(tk.E, tk.W), columnspan=2)

        # More global padding.
        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)
            
    def try_login(self, givenName, givenPass, userType):
        '''(LoginFrame, str, str, AccountType Enum) -> NoneType
        Use given userType and given information currently in the username and
        password boxes and try to match a record.
        If they do, open the relevant user window. Otherwise, display a message
        box with explanation.
        '''
        potentialAccount = account.Account()
        # Check if account exists at all.
        if potentialAccount.readAccountInfo(givenName, userType):
            # Check if account credentials are valid.
            if potentialAccount.auth(givenPass):
                # Pass along the right user window to open.
                self.openUserWindow(userType)
            else:
                messagebox.showerror("Incorrect Password Combination", 
                                     "Invalid User/Password Combination")
        else:
            messagebox.showerror("No such account", 
                                 "Couldn't find an account with that username")

    def try_register_account(self, givenName, givenPass, userType):
        '''(LoginFrame, str, str, AccountType Enum) -> NoneType
        Try to write out a new account with the given information.
        Display a messagebox describing whether writing succeeded.
        '''
        accountOut = account.Account(givenName, givenPass, userType)
        if accountOut.writeAccountInfo():
            messagebox.showinfo("Created new account", 
                                "New account registered\nYou may now log in")
        else:
            messagebox.showerror("Could not register", 
                                 "Given username or password is invalid"
                                 + " or account of same name already exists")

    def openUserWindow(self, userType):
        '''(LoginFrame, AccountType Enum) -> NoneType
        Given a user type as AccountType Enum, open the appropriate top level
        window for them.
        '''
        # TODO: Umm, code smells we can strategy pattern this instead.
        if userType == account_types.AccountType.I:
            sourceFile = instrWindow.generateMainWindow(self.controller)
        elif userType == account_types.AccountType.S:
            sourceFile = studentWindow.questionSetPanel(self.username.get())
        self.clearInfo()

    def clearInfo(self):
        '''(LoginFrame) -> NoneType
        Clears login info that exists within the username/password fields.
        '''
        self.userNameEntry.delete(0, 'end')
        self.userPassEntry.delete(0, 'end')

if __name__ == "__main__":      
    root = tk.Tk()
    root.title("Welcome!")
    root.minsize(320, 150)
    root.resizable(False, False)
    loginWindow = LoginWindow(root)
    loginWindow.grid(row=8, column=0, sticky=(tk.E, tk.W))
    root.mainloop() 
