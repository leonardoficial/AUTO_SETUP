from tkinter  import *
from tkinter  import ttk

from datetime import datetime
from textwrap import fill as textwrap

# Classe para testes
#from TEST.TestProgressInstaller import TestProgressInstaller

from MainInstaller import Installer
from MainModel     import Model

class MainProgressInterface:

    def __init__(self, model):

        # Inicializa interface grafica
        self.window=Tk()
        self.window.title('AUTO_SETUP')
        self.window.resizable(False, False)

        # Ações a serem executadas
        self.actions = model.data["actions"]["total"]

        self.status = {
            "actions": {
                "total":     len(self.actions),
                "finished":  0
            },
            "time": {
                "expected": "00:00",
                "current":  datetime.now()
            }
        }

        # Valor da barra de progresso
        self.progress_value = DoubleVar()

        # Inicializa objecto instalador
        #self.installerController = TestProgressInstaller(self.actions, self)
        self.installerController  = Installer(model, self)


        self.render_section_title   (row=0, column=0, padx=10, pady=20)
        #ttk.Separator(window, orient=HORIZONTAL).grid(row=1, ipadx=140, pady=10)

        self.render_section_actions (row=0, column=1, padx=10)
        self.render_section_time    (row=0, column=2, padx=10)
        #ttk.Separator(window, orient=HORIZONTAL).grid(row=4, ipadx=140, pady=5)

        self.render_section_module      (row=2, column=0, padx=10)
        self.render_section_progressbar (row=2, column=1, padx=10, columnspan=3)

        self.render_section_cancel      (row=3, column=2, padx=(50, 0), pady=(10, 15))

        # Atualiza tempo e barra de progresso
        self.update()

        # Inicia processo de instalação
        self.installerController.start()

        # Mostra interface grafica
        self.window.mainloop()


    def render_section_title(self, **kwargs):
        self.label_title=Label(self.window, text="EXECUTANDO CONFIG", padx=10, pady=10, font="Helvetica 8 bold", borderwidth = 2, relief = "groove")
        self.label_title.grid(**kwargs)



    def render_section_actions(self, **kwargs):
        section=LabelFrame(self.window, borderwidth=0, padx=0, pady=0)
        section.grid(**kwargs)

        self.label_actions_total=Label(section, text=self.status["actions"]["total"] , padx=10, width=5)
        self.label_actions_total.grid(row=0, column=0, sticky="e")

        Label(section, text="TOTAL AÇÕES", padx=10, width=15, anchor="w").grid(row=0, column=1)

        self.label_actions_finished=Label(section, text="0", padx=10, width=5)
        self.label_actions_finished.grid(row=1, column=0, sticky="W")

        Label(section, text="EXECUTADAS", padx=10, width=15, anchor="w").grid(row=1, column=1)



    def render_section_time(self, **kwargs):
        section=LabelFrame(self.window, borderwidth=0, padx=0, pady=10)
        section.grid(**kwargs)

        self.label_time_total=Label(section, text="00:00", padx=10, width=5)
        self.label_time_total.grid(row=0, column=0, sticky="e")

        Label(section, text="TEMPO PREVISTO", padx=10, width=15, anchor="w").grid(row=0, column=1)

        self.label_time_left=Label(section, text=(self.status["time"]["expected"]), padx=10, width=5)
        self.label_time_left.grid(row=1, column=0, sticky="e")

        Label(section, text="TEMPO TOTAL", padx=10, width=15, anchor="w").grid(row=1, column=1)



    def render_section_module(self, **kwargs):
        section=Frame(self.window, borderwidth=0, padx=0, pady=10)
        section.grid(**kwargs)

        self.label_module_name=Label(section, text="", padx=10, font="Helvetica 8 bold")
        self.label_module_name.grid(row=0, column=0)

        self.label_action_desc=Label(section, text="", padx=10, width=20, height=3)
        self.label_action_desc.grid(row=1, column=0)



    def render_section_progressbar(self, **kwargs):
        section=Frame(self.window, padx=0, pady=10)
        section.grid(**kwargs)

        self.progress_bar=ttk.Progressbar(section, mode="determinate", maximum=100, length=370)
        self.progress_bar.pack(ipady=10)


    def render_section_cancel(self, **kwargs):
        # GROUP FINISH - PROGRESS BAR
        section=LabelFrame(self.window, borderwidth = 0, padx = 0, pady = 0)
        section.grid(**kwargs)
        # GROUP FINISH - BUTTONS
        button=Button(section, text = "CANCELAR", background = "LIGHTGRAY", borderwidth = 2, relief = "groove", height = 1, width = 15)
        #button.bind("<Button-1>", self.install)
        button.grid()

    def update(self):

        # VARIAVEIS UTEIS
        actions_total    = self.status["actions"]["total"]
        actions_finished = self.status["actions"]["finished"] + 1

        if actions_finished >= actions_total:
            print("DONE")
            return 1


        timenow  = datetime.now()
        ftimenow = timenow.strftime("%M:%S")

        diftime  = timenow - self.status["time"]["current"]
        fdiftime = ( str(diftime).split(".") )[0]

        # UPDATE LABEL - TIME
        self.label_time_left["text"] = fdiftime

        # UPDATE WINDOW
        self.window.update()

        self.window.after(1000, self.update)

    # UPDATE VIEW
    def log(self, status, action):

        if(status != 1):
            return 0

        # VARIAVEIS UTEIS
        actions_total    = self.status["actions"]["total"]
        actions_finished = self.status["actions"]["finished"] + 1

        bar_perc = (actions_finished / actions_total) * 100

        # UPDATE LABEL - ACITONS
        self.label_actions_finished["text"] = actions_finished
        # UPDATE LABEL - MODULE NAME
        self.label_module_name["text"] = action["module"]
        # UPDATE LABEL - DESC
        self.label_action_desc["text"] = textwrap(action["desc"], width=20)
        # UPDATE PROGRESS BAR
        self.progress_bar["value"] = bar_perc

        self.status["actions"]["finished"] = self.status["actions"]["finished"] + 1

        # UPDATE WINDOW
        self.window.update()

        #print("ACTION: " + str(actions_finished) )



# model = Model()
# model.data["vars"]["dynamics"]["DPTxxx"]["value"] = "001"
# model.update_paths("DPTxxx")
# #
# MainProgressInterface(model)
