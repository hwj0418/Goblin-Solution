from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
import os
import os.path
import shutil
import questionSetReader

def readQuestionSet(filePath):
    '''(str) -> list of str
    Return a list of question sets, sans extensions, from a given file path.
    '''
    questionSetList = []

    for file in os.listdir(filePath):
        # Append only the name of the file to the list.
        questionSetList.append(file.rsplit('.', 1)[0])
    # arrays begin from 0
    return questionSetList[0:]


class QuestionSetGridView:
    '''A class to handle all aspects of the student question set grid view.'''

    def __init__(self, master, parent):
        '''(QuestionSetGridView, Tk) -> NoneType
        Create the appropriate labels for each queston set and also generate
        values and buttons for questions sets as appropriate
        '''
        # we need this so we can interact with the window this view exists in
        self._windowHandle = master
        self.parent = parent

        # TODO sometime soon we may want to agree on somekind of unified column system/class.
        # Configure grid for main window.
        Grid.rowconfigure(master, 0, weight=1)
        Grid.columnconfigure(master, 0, weight=1)
        self.frame = Frame(master, bg='white')
        self.frame.grid(row=0, column=0, sticky='NSWE')
        # Create table headers for question set information.
        self.nameLabel = Label(self.frame, text='Homework Set', fg='black')
        self.numQuestionsLabel = Label(self.frame,
                                       text='Questions In This Set',
                                       fg='black')
        self.dueDateLabel = Label(self.frame, text='Due Date', fg='black')
        self.highestMarkLabel = Label(self.frame, text='Highest Mark',
                                      fg='black')
        self.statusLabel = Label(self.frame, text='Status', fg='black')
        self.attemptLabel = Label(self.frame, text='Attempt This Set',
                                  fg='black')

        # Configure grid columns to adjust when window size is changed.
        for columnIndex in range(6):
            Grid.columnconfigure(self.frame, columnIndex, weight=1)

        # Configure grid for table headers.
        self.nameLabel.grid(row=0, column=0, sticky='NSEW')
        self.numQuestionsLabel.grid(row=0, column=1, sticky='NSEW')
        self.dueDateLabel.grid(row=0, column=2, sticky='NSEW')
        self.highestMarkLabel.grid(row=0, column=3, sticky='NSEW')
        self.statusLabel.grid(row=0, column=4, sticky='NSEW')
        self.attemptLabel.grid(row=0, column=5, sticky='NSEW')
        rowCounter = 1

        # TODO I think it'd be a lot cleaner for this to be in its own function
        # but let's wait until we finalize what this class/func does
        for questionSetName in readQuestionSet('Question Sets'):
            # Look in the directory for question sets and generate rows for
            # each.
            # Create a label for each question set in the list.
            self.questionSetLabel = Label(self.frame, text=questionSetName,
                                          fg='black', bg='white')
            self.questionSetLabel.grid(row=rowCounter, column=0)

            # Format due date for comparison.
            dueDate = datetime.strptime(self.getDueDate(questionSetName), '%b %d %Y %I:%M%p')

            # Create a button allowing the user to attempt a set, Open new
            # window on left click
            attemptButton = Button(self.frame, text="Attempt " +
                                        questionSetName)

            # TODO: Having trouble configuring a widget without an event. Make this it's own function later.
            if datetime.now() >= dueDate:
                attemptButton.configure(text = "Due Date Has Passed")
                attemptButton.configure(state = DISABLED)

            attemptButton.grid(row=rowCounter, column=5, sticky='NSEW')

            # Configure grid for question set names.
            Grid.rowconfigure(self.frame, rowCounter, weight=1)

            # Highlight on hover.
            attemptButton.bind('<Enter>', self.highlight)
            # Unhighlight on non-hover.
            attemptButton.bind('<Leave>', self.unhighlight)
            # we must explicitly bind like this in order to be able to redirect the user properly
            # TODO temp hardcoded to always look at alice until we can get account redirects working
            attemptButton.bind('<Button-1>', lambda event,
                                    student_name = "Alice",
                                    arg=questionSetName:
                                    self.openQuestionSet(event, student_name,
                                                         arg))
            rowCounter += 1

        # filling number of questions fields
        rowCounter = 1

        # TODO what is the purpose of this? It's blatantly copy-pasted from above
        for questionSetName in readQuestionSet('Question Sets'):

            # Gets the current working directory
            d = os.getcwd()
            # holding absolute path in a variable
            path = d + '/Question Sets/' + questionSetName + '.txt'
            f = open(path)
            lines = f.readlines()
            try:
                num_of_questions = lines[0]
            except:
                IndexError(
                    "Number of questions not stated in question set file")

            # Look in the directory for question sets and generate rows for
            # each.
            # Create a label for each question set in the list.
            self.questionSetLabel = Label(self.frame, text=num_of_questions,
                                          fg='black', bg='white')
            self.questionSetLabel.grid(row=rowCounter, column=1)

            rowCounter += 1
        # filling due date fields
        rowCounter = 1

        # TODO once again, why the **** is this consecutively repeated for the third time
        for questionSetName in readQuestionSet('Question Sets'):

            # Gets the current working directory
            d = os.getcwd()
            # holding absolute path in a variable
            path = d + '/Question Sets/' + questionSetName + '.txt'

            f = open(path)
            lines = f.readlines()
            try:
                num_of_questions = lines[1]
            except:
                IndexError(
                    "Number of questions not stated in question set file")

            # Look in the directory for question sets and generate rows for
            # each.
            # Create a label for each question set in the list.
            self.questionSetLabel = Label(self.frame, text=num_of_questions,
                                          fg='black', bg='white')
            self.questionSetLabel.grid(row=rowCounter, column=2)

            rowCounter += 1

    def highlight(self, event):
        '''(QuestionSetGridView, event) -> NoneType
        Event to hightlight labels, as well as change cursor upon hover.
        '''
        if event.widget['state'] == NORMAL:
            event.widget.config(relief='groove')
            # TODO: SET A PROPER CURSOR. SOME CURORS TK ARE ALREADY MAPPED TO
            # DEFAULT WINDOWS OR MAC CURSORS.
            event.widget.config(cursor='pencil')

    def unhighlight(self, event):
        '''(QuestionSetGridView, event) -> NoneType
        Event to unhightlight labels upon non-hover.
        '''
        event.widget.config(relief='raised')

    # Because we don't have a getter for this yet.
    def getDueDate(self, questionSetName):
        '''(QuestionSetGridview, str) -> str
        Returns the due date of a question set.
        '''        
        fp = open("./Question Sets/" + questionSetName + '.txt', "r")
        questionSet = fp.read().splitlines()

        return questionSet[1]      

    def openQuestionSet(self, event, student_name, questionSetName):
        '''(QuestionSetGridview, event, string, string) -> NoneType
        Event to open a question set. Creates a new window.
        '''
        if event.widget['state'] == NORMAL:
            # We are creating a new window, so it's a good idea to hide the old one
            self._windowHandle.withdraw()
            self._questionSetWindow = Tk()
            # override default closing behaviour so we can cleanup
            self._questionSetWindow.protocol('WM_DELETE_WINDOW',
                                             self.onQuestionSetClose)
            self._questionSetWindow.title(questionSetName)
            self._questionSetWindow.configure(bg = 'white')
            self._questionSetWindow.minsize(300, 200)
            question_set = []
            student_mark = 0
            fp = open("./Question Sets/" + questionSetName + '.txt', "r")
            if self.check_progress(student_name, questionSetName):
                if messagebox.askyesno("unfinished work found", "Resume your \
                work?"):
                    fp = open(os.getcwd() + "Students/" + student_name +
                              "/" + questionSetName + '.txt', "r")
                    student_mark = question_set[1]
            question_set = fp.read().splitlines()
            # throws index error for malformed files
            try:
                self.process_questions(self._questionSetWindow, question_set[2:],
                                       student_mark, questionSetName)
            except (IndexError):
                messagebox.showerror("Errors while reading", "Error reading file: Unexpected format")

    def check_progress(self, student_name, question_set_name):
        """() -> Boolean"""
        res = False
        des_dir = os.getcwd() + "Students/" + student_name + "/" + question_set_name
        if os.path.exists(des_dir):
            fp = open(os.getcwd() + "Students/" + student_name +
                          "/" + questionSetName + '.txt', "r")
            print(fp.read().splitlines())
            length = len(fp.read().splitlines())
            if length > 2:
                res = True
        return res

    def process_questions(self, currentQuestion, questionSet, student_mark,
                          title):
        '''(QuestionSetGridview, Tk, list, int) -> None
        Tries to convert the given list of raw question set data from file into
        a readable sequence of questions in the UI
        '''
        mcButtons = list()
        index = 0
        # current question label here
        questionLabel = Label(currentQuestion, text=questionSet[index],
                              bg='white')
        questionLabel.grid(row = index + 1, column = 0, sticky='W')
        saveProgress = Button(currentQuestion, text = 'Save Progress',
                                  bg = 'white')
        index += 1
        # multiple choice buttons here
        for index in range(index, index + 4):
            mcButton = Button(currentQuestion, text=questionSet[index])
            mcButton.grid(row=index + 1, column=0, sticky='W')
            mcButtons.append(mcButton)
        # correct answer
        index += 1
        correct_ans = questionSet[index]
        index += 1
        saveProgress.grid(row=index+1, column=2, sticky='W')
        # TODO big hunkajunk code ahead rife with hardcoding and temp values
        saveProgress.bind('<Button-1>', lambda event, 
                          current_window=currentQuestion,
                          questionSet=questionSet,
                          student_mark=student_mark, student_name="Alice",
                          question_set_name=title:
                          self.save_progress(event, current_window,
                                             questionSet, student_mark,
                                             student_name, question_set_name))
        for button in mcButtons:
            button.bind('<Button-1>', lambda event,
                        currentQuestion=currentQuestion,
                        questionSet=questionSet[index:],
                        student_ans=button['text'], correct_ans=correct_ans,
                        student_mark=student_mark,
                        mcButtons=mcButtons, title=title:
                        self.check_ans(event, currentQuestion,
                                       questionSet, student_ans,
                                       correct_ans, student_mark,
                                       mcButtons, title))

    def save_progress(self, event, current_window, questionSet, student_mark,
                      student_name, question_set_title):
        des_dir = os.getcwd() + '/'  + "Students/"+ student_name
        if not os.path.exists(des_dir):
            os.makedirs(des_dir)
        os.chdir(des_dir)
        if os.path.isfile(des_dir + question_set_title + '.txt'):
            fp = open(question_set_title + '.txt', 'a')
            fp.write(student_mark + '\n')
        else:
            fp = open(question_set_title + '.txt', 'w+')
            fp.write('highest score: ' + str(student_mark) + '\n')
            fp.write(str(student_mark) + '\n')
        for line in questionSet:
            fp.write(line + '\n')
        fp.close()
        messagebox.showinfo("Save Progress", "Your work has been saved to: " +
                            os.getcwd())
        current_window.withdraw()

    def result(self, mark):
        '''(QuestionSetGridview, int) -> None
        '''
        if messagebox.askyesno("Result for this question set",
                               "Your final mark is: " +
                               str(mark) + "\nBut can you beat that?"):
            # TODO do some things, winners don't do drugs
            pass
        else:
            # we no longer need this window as we are done the set
            self._questionSetWindow.destroy()
            # make sure to make the old window visible again
            self._windowHandle.deiconify()

    # TODO holy telescoping function, batman! this needs to be broken up ASAP
    def check_ans(self, event, currentQuestion, questionSet, student_ans,
                  correct_ans, student_mark, mcButtons, title):
        '''(QuestionSetGridview, event, Tk, list, str, str, int) -> int
        '''
        for button in mcButtons:
            button.config(state = DISABLED)

        feedback = questionSet[0]
        if student_ans == correct_ans:
            res = "correct"
            student_mark += 1
        else:
            res = "wrong"
        messagebox.showinfo("result", "Your answer is " + str(res) +
                            ".\n" + feedback)
        # process next question
        if questionSet[1:] == []:
            # reach the end of question set, report final mark
            self.result(student_mark)
        else:
            # output result for current question
            currentQuestion.withdraw()
            nextQuestion = Tk()
            nextQuestion.title(title)
            nextQuestion.minsize(300, 200)
            self.process_questions(nextQuestion, questionSet[1:], student_mark,
                                   title)

    def onQuestionSetClose(self):
        """ (QuestionSetGridView) -> NoneType
        Special function block executed when the question set window is
        forcibly closed via the 'x'
        """
        # warn the user their information is not saved yet
        if messagebox.askyesno(
                "Return to Question Sets?",
                "You have not yet completed this question set." +
                "\nAre you sure you want to abandon this attempt?"):
            self._questionSetWindow.destroy()
            # make sure to make the old window visible again
            self._windowHandle.deiconify()

    def check_highest_mark(self, name, question_set, student_mark):
        ''' (QuestionSetGridView, String, String, int) -> NoneType
        This function is called after a question set has been completely answered
        that checks if the students previous highest mark was beaten
        '''
        # open student file and check if student_mark is the highscore
        f = open('./Students/{0}/{1}.txt'.format(name, question_set), 'r+')
        highscore = int(f.readline()[11:])
        if (student_mark > highscore):
            f.seek(0)
            f.write('highscore: {0}'.format(student_mark))
        f.close()

def generateMainWindow(oldWindow):
    '''
    Withdraw the given window handle and display the main window of this class
    '''
    # TODO set behaviour on close
    oldWindow.master.withdraw()
    top = Toplevel()
    top.title("Welcome to the World of Tomorrow!")
    top.minsize(800, 100)
    top.resizable(False, True)
    newLabels = QuestionSetGridView(top, oldWindow)
    # annoyingly, doesn't run on cancel as well...
    newLabels._windowHandle.protocol('WM_DELETE_WINDOW', lambda: oldWindow.returnToLogin(top))    

if __name__ == "__main__":
    root = Tk()
    root.title('Fantastic Questions Await Thee')
    root.configure(bg = 'white')
    root.minsize(800, 100)
    root.resizable(False, True)
    newLabels = QuestionSetGridView(root, None)

    root.mainloop()
