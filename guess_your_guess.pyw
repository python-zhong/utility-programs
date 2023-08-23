from tkinter import *
from tkinter.ttk import *
from tkinter.font import Font
from tkinter.messagebox import showinfo
from tkinter.scrolledtext import ScrolledText
import random
import sys
if sys.platform == 'win32':
    try:
        import ctypes
        ctypes.OleDLL('shcore').SetProcessDpiAwareness(1)  # For High DPI on Windows
    except:
        pass
# Generate questions
def generate(questions: int) -> list[list[int]]:
    questions = int(questions)
    if questions < 1:
        return []
    res = []
    MAX = 2 ** questions
    for i in range(questions):
        numbers = []
        for num in range(1, MAX):
            if ('{:0>'+str(questions)+'b}').format(num)[-i-1] == '1':
                numbers.append(num)
        random.shuffle(numbers)
        res.append(numbers)
    return res

# Restore the answers to your guess
def restore_from_guesses(*each_answer: bool) -> int:
    string = ''
    for i in each_answer:
        string += str(int(i))
    return int(''.join(reversed(string)), base=2)

ASKED_QUESTIONS = 5
questions = generate(ASKED_QUESTIONS)
each_numbers = 2 ** (ASKED_QUESTIONS-1)
max_number = (2 ** ASKED_QUESTIONS) - 1
if (ASKED_QUESTIONS - 1) % 2 == 0:
    each_line = 2 ** int((ASKED_QUESTIONS - 1) / 2)
else:
    each_line = 2 ** int((ASKED_QUESTIONS - 2) / 2)

printed_questions = []
for question in questions:
    printed_question = []
    for index, num in enumerate(question):
        if index and index % each_line == 0:
            printed_question[-1] = printed_question[-1][:-1]
            printed_question.append('\n')
        printed_question.append(str(num)+' ')
    printed_questions.append(''.join(printed_question).strip())
    printed_question.clear()
tk = Tk(className='Guess Your Guess')

font = Font(tk, family='Consolas', size=20) # 15
DESTROYED = False
# ---------- Prompt User - Start ----------
def prompt_user():
    tk.withdraw()
    t = Toplevel(tk)
    t.title('Guess Your Guess')
    Label(t, text=f"Now, think about a number, range 0 - {max_number} (Don't tell the number to others)").pack(side=TOP)
    f1 = Frame(t)
    f1.pack(side=BOTTOM)
    def start():
        t.destroy()
        tk.deiconify()
    def destroy():
        t.destroy()
        tk.destroy()
        global DESTROYED
        DESTROYED = True
    Button(f1, text='Exit', command=destroy).pack(side=LEFT)
    Button(f1, text='OK', command=start).pack(side=RIGHT)
    t.resizable(False, False)
    t.mainloop()
# ---------- Prompt User - End ----------
# ---------- Page Config - Start ----------
def config_page():
    def next_question():
        nonlocal current_question
        answers[current_question] = bool(current_answer.get())
        if current_question >= ASKED_QUESTIONS - 1:
            showinfo('Guess Your Guess', f'You guessed: {restore_from_guesses(*answers)}')
            tk.destroy()
            return
        current_question += 1
        if current_question >= ASKED_QUESTIONS - 1:
            next_button.config(text='Submit')
        else:
            previous_button.config(state=NORMAL)
        current_answer.set(answers[current_question])
        text.config(state=NORMAL)
        text.delete('1.0', END)
        text.insert('1.0', printed_questions[current_question])
        text.config(state=DISABLED)
        var.set(f'Question {current_question+1}')
    def previous_question():
        nonlocal current_question
        answers[current_question] = bool(current_answer.get())
        current_question -= 1
        if current_question < 1:
            previous_button.config(state=DISABLED)
        next_button.config(text='Next')
        current_answer.set(answers[current_question])
        text.config(state=NORMAL)
        text.delete('1.0', END)
        text.insert('1.0', printed_questions[current_question])
        text.config(state=DISABLED)
        var.set(f'Question {current_question+1}')
    current_question = 0
    answers = [False] * ASKED_QUESTIONS
    current_answer = IntVar(tk, 0)
    control_frame = Frame(tk)
    control_frame.pack(side=TOP, fill=X)
    show_frame = Frame(tk)
    show_frame.pack(side=BOTTOM, fill=BOTH, expand=True)
    var = StringVar(tk, 'Question 1')
    Label(control_frame, textvariable=var).pack(side=LEFT)
    next_button = Button(control_frame, text='Next' if ASKED_QUESTIONS > 1 else 'Submit', command=next_question)
    next_button.pack(side=RIGHT)
    previous_button = Button(control_frame, text='Previous', command=previous_question, state=DISABLED)
    previous_button.pack(side=RIGHT)
    Checkbutton(show_frame, offvalue=OFF, onvalue=ON, text='My number is in this set.', variable=current_answer).pack(side=TOP)
    text_frame = Frame(show_frame)
    text_frame.pack(side=BOTTOM, expand=True, fill=BOTH)
    text = ScrolledText(text_frame, wrap=NONE, font=font, width=20, height=5)
    text.pack(side=TOP, fill=BOTH, expand=True)
    bar = Scrollbar(text_frame, command=text.xview, orient=HORIZONTAL)
    bar.pack(side=BOTTOM, fill=X)
    text.config(xscrollcommand=bar.set)
    text.delete('1.0', END)
    text.insert('1.0', printed_questions[current_question])
    text.config(state=DISABLED)
# ---------- Page Config - End ----------
# ---------- Start! ----------
config_page()
prompt_user()
if not DESTROYED:
    tk.mainloop()
