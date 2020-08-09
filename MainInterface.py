from tkinter import *
from tkinter import ttk

# DADOS
from MainModel import Model
# Installaer GUI
from MainProgressInterface import MainProgressInterface

class MainInterface:

    def __init__(self, window):

        #
        self.model   = Model()
        self.window  = window
        self.modules = self.model.modules

        # Nomes dos modulos carregados
        self.modules_names = self.model.modules_names

        # IDENTIFICA VARIAVEIS NÃO INICIALIZADAS
        self.uninitialized_vars  = self.model.data["vars"]["dynamics"]
        # IDENTIFICA CAMINHOS DINÂMICOS
        self.uninitialized_paths = self.model.data["paths"]["dynamics"]

        # VARIAVEIS PARA FACILITAR IDENTIFICACOES NO TREEVIEW
        self.selected_var = None

        # VARIAVEIS...
        self.ignore_var  = BooleanVar()
        self.logging_var = BooleanVar()

        # VARIAVEL PARA INDENTIFICAR MODULO SELECIONADO
        self.selectedModule=StringVar(self.window)
        self.selectedModule.set("SYSTEM")

        # RENDER SECTIONS

        self.render_menu()

        # SECTION 1
        self.render_section_info       (row=0, column=0, padx=10, pady=(18, 10))

        self.render_section_vars       (row=1, column=0, padx=10, pady=0)

        ttk.Separator(self.window, orient=HORIZONTAL).grid(row=0, column=1, padx=10, ipady=180, rowspan=2)

        self.render_section_module_info       (row=0, column=2, padx=10, pady=10)
        self.render_section_module_selection  (row=0, column=3, padx=10, pady=10)
        self.render_section_module_checkboxes (row=0, column=4, padx=10, pady=10)
        # SECTION 2

        self.render_section_module     (row=1, column=2, padx=10, pady=(20, 10), columnspan=3, rowspan=2)
        # SECTION 3
        #self.render_section_actions    (row=2, column=0, padx=10, pady=20)


    def render_menu(self):

        menubar=Menu(self.window)

        filemenu=Menu(menubar, tearoff=0)

        filemenu.add_command(label="Importar configuração")
        filemenu.add_command(label="Exportar configuração")

        filemenu.add_separator()

        filemenu.add_command(label="Sair", command=self.window.quit)

        menubar.add_cascade(label="ARQUIVO", menu=filemenu)

        self.window.configure(menu=menubar)



    def render_section_info(self, **kwargs):
        # GROUP FILE - FRAME
        section=Frame(self.window, padx=0, pady=0, background="#FFFFFF")
        section.grid(kwargs)

        sub_section = Frame(section, padx=0, pady=0, background="#FFFFFF")
        sub_section.grid(row=0, column=0, columnspan=6)

        # GROUP FILE - LABELS
        Label(sub_section, text="{", width=2,    pady=8, font='Helvetica 12', borderwidth=2, relief="groove", background="#FFF", fg="#0078C7").grid(row=0, column=0, pady=2)
        Label(sub_section, text="RIOONIBUS_x64", pady=8, width=39, font='Helvetica 8 bold', background="#FFF").grid(row=0, column=1, pady=2)
        Label(sub_section, text="}", width=2,    pady=8, font='Helvetica 12', borderwidth=2, relief="groove", background="#FFF", fg="#0078C7").grid(row=0, column=2, pady=2)

        ttk.Separator(section, orient=HORIZONTAL).grid(row=1, column=0, pady=10, columnspan=6, ipadx=166)

        # Label(section, text="A",             pady=3, width=2, font='Helvetica 12 bold', borderwidth=2, relief="groove", fg="#5bc0de", background="WHITE").grid(row=2, column=0, pady=5)
        # Label(section, text="TEC EMBARCADA", padx=13, pady=3, width=39, font='Helvetica 8',  background="WHITE").grid(row=2, column=1, pady=5)

        # Label(section, text="V",        pady=3, width=2, font='Helvetica 12 bold', borderwidth=2, relief="groove", fg="#5cb85c", background="WHITE").grid(row=3, column=0, pady=5)
        # Label(section, text="1.0.0.0",  padx=39, pady=3, width=2, font='Helvetica 8', background="WHITE").grid(row=3, column=1)

        #Label(section, text="D",          pady=6, width=2, font='Helvetica 12 bold', borderwidth=2, relief="groove", fg="#f0ad4e", background="WHITE").grid(row=2, column=4, pady=5)
        #Label(section, text="01/01/2020", padx=13, pady=6, width=6, font='Helvetica 8',  background="WHITE").grid(row=2, column=5, pady=5)




    def render_section_module_info(self, **kwargs):
        # GROUP SELECT - MAIN FRAME
        section=LabelFrame(self.window, padx=0, pady=0, borderwidth=1, relief="solid")
        section.grid(**kwargs)

        label=Label(section, text="SELECIONAR MODULO", padx=0, pady=6,  width=19, background="#0078C7", fg="white", font=("Verdana", 8, "bold"), borderwidth = 0, relief = "solid")
        label.grid(row=0, column=0, pady=0)

        #
        self.optionsMenu=OptionMenu(section, self.selectedModule, *self.modules_names, command=self.onChangeOptions)
        self.optionsMenu.config(height=2, width=13, borderwidth = 1, relief = "solid", background="#f7f7f7", font=("Verdana", 8, "bold"))
        self.optionsMenu.grid(row=1, column=0, ipady=5, pady=2)


    def render_section_module_selection(self, **kwargs):
        # GROUP SELECT - MAIN FRAME
        section=Frame(self.window, padx=0, pady=0,  borderwidth=1, relief="solid")
        section.grid(**kwargs)

        label=Label(section, text="DADOS MODULO", padx=0, pady=6,  width=21, background="#0078C7", fg="white", font=("Verdana", 8, "bold"), borderwidth = 0, relief = "solid")
        label.grid(row=0, column=0, pady=0, columnspan=2)

        # Modulo atual

        module_index   = self.modules_names.index( self.selectedModule.get() )
        module_current = self.modules[ module_index ]
        module_version = module_current["version"]

        # GROUP SELECT - LABELS
        Label(section, text="TIPO",   padx=0, pady=5, width=10, background="#f7f7f7", font=("Verdana", 8, "bold")).grid(row=2, column=0, pady=0)
        Label(section, text="VERSÃO", padx=0, pady=5, width=10, background="#f7f7f7", font=("Verdana", 8, "bold")).grid(row=1, column=0, pady=0)

        self.label_module_type=Label   (section, text="BUILT-IN",     padx=5, pady=5, width=10, background="#f7f7f7", font=("Verdana", 8))
        self.label_module_version=Label(section, text=module_version, padx=5, pady=5, width=10, background="#f7f7f7", font=("Verdana", 8))

        self.label_module_type.grid(row=2, column=1, pady=0)
        self.label_module_version.grid(row=1, column=1, pady=0)




    def render_section_module_checkboxes(self, **kwargs):
        # GROUP CHECKBOXES - FRAME
        bg = "#f7f7f7"
        section=LabelFrame(self.window, padx = 0, pady=0, borderwidth = 1, relief = "solid", background=bg)
        section.grid(kwargs)

        label=Label(section, text="CONFIGURAR MODULO", padx=4, pady=6,  width=20, background="#0078C7", fg="white", font=("Verdana", 8, "bold"), borderwidth = 0, relief = "solid")
        label.grid(row=0, column=0, pady=0, columnspan=2)

        # GROUP CHECKBOXES - IGNORE
        self.ignoreButton=Checkbutton(section, text=" Ignorar Modulos", variable=self.ignore_var,  onvalue=True, offvalue=False, width=20, anchor="w", command=self.onChangeIgnore, background=bg)
        self.ignoreButton.grid(row=1, column=0, pady=(0,3))
        # GROUP CHECKBOXES - LOGGING
        self.loggingButton=Checkbutton(section, text=" Gerar Logs",    variable=self.logging_var, onvalue=True, offvalue=False, width=20, anchor="w", background=bg)
        self.loggingButton.grid(row=2, column=0, pady=(0,3))



    def render_section_vars(self, **kwargs):
        # GROUP VARS - FRAME
        #text = "Inicializar variaveis"
        section=Frame(self.window, padx = 0, pady = 0, borderwidth = 1, relief = "solid", background='#FFF')
        section.grid(kwargs)

        label=Label(section, text="INICIALIZAR VARIAVEIS", padx=3, pady=8,  width=41, background="#0078C7", fg="white", font=("Verdana", 8, "bold"), borderwidth = 0, relief = "solid")
        label.grid(row=0, column=0, pady=(0, 8), columnspan=2, columns=3)

        # GROUP INFO  fg="#d9534f",
        Label(section, text="4", width=3, background="WHITE", font=("Verdana", 8, "bold"), borderwidth = 1, relief = "solid").grid(row=1, column=0, stick="W", ipady=5, padx=(11,2))
        Label(section, text="N INICIALIZADAS", width=17, background="WHITE", borderwidth = 1, relief = "solid").grid(row=1, column=1, stick="W", ipady=4)



        # GROUP VARS - LISTBOX
        self.listbox_vars=Listbox(section, height=7, borderwidth = 1, relief = "solid", width=27)
        self.listbox_vars.bind("<<ListboxSelect>>", self.changeInputVar)
        #
        for index, var in enumerate(self.uninitialized_vars):
            #
            self.listbox_vars.insert(index, self.uninitialized_vars[var]["name"])

        self.listbox_vars.grid(row = 2, rowspan=5, columnspan=2, column=0, padx=10, pady=8, sticky="W")

        # GROUP VARS - ENTRY
        self.input_var=Entry(section, width = 21, borderwidth = 1, relief = "solid")
        self.input_var.grid(row = 1, column = 2, ipady = 4, pady=5, columns=2)

        # GROUP VARS - BUTTON
        self.button_var=Button(section, text = "SETAR", background = "LIGHTGRAY", padx = 10, pady = 0, width = 15, borderwidth = 1, relief = "solid")
        self.button_var.bind("<Button-1>", self.setVarValue)
        self.button_var.grid(row=2, column=2, padx=8, ipady=6, pady = (9,5))

        btn=Button(section, text = "RESETAR", background = "#eee", padx = 10, pady = 0, width = 15, borderwidth = 1, relief = "solid")
        btn.grid(row = 3, column = 2, padx = 8, ipady=2, pady = 5)

        btn=Button(section, text = "RESETAR TODAS", background = "#eee", padx = 10, pady = 0, width = 15, borderwidth = 1, relief = "solid")
        btn.grid(row = 4, column = 2, padx = 8, ipady=2, pady = 5)



    def render_section_actions(self, **kwargs):
        # GROUP ACTIONS - FRAME
        section=Frame(self.window, padx=0, pady=0, borderwidth = 1, relief="solid", background='#FFF')
        section.grid(kwargs)

        # label=Label(section, text="AÇÕES FINAIS", padx=3, pady=8,  width=40, background="#0078C7", fg="white", font=("Verdana", 8, "bold"), borderwidth = 0, relief = "solid")
        # label.grid(row=0, column=0, pady=(0, 10), columnspan=3)

        # GROUP FINISH - BUTTONS
        button1=Button(section, text = "VALIDAR", background = "LIGHTGRAY", borderwidth = 1, relief = "solid", height=2, width=10)
        button1.grid(row=1, column=0, padx=11, pady=10)

        button1=Button(section, text = "TESTAR", background = "LIGHTGRAY", borderwidth = 1, relief = "solid", height=2, width=10)
        button1.grid(row=1, column=1, padx=10, pady=10)

        button2=Button(section, text = "INSTALAR",  background = "LIGHTGRAY", borderwidth = 1, relief = "solid", height=2, width=10)
        button2.bind("<Button-1>", self.install)
        button2.grid(row=1, column=2, padx=11, pady=10)


    def render_section_module(self, **kwargs):
        # MAPEIA O ATRIBUTO QUE DESCREVE/IDENTIFICA UM OBJETO DENTRO DE VARS, PATHS E ACTION
        self.mapping = {
            "vars":     "value",
            "paths":    "value"
        }
        # GROUP TREE - FRAME
        section=Frame(self.window, padx=0, pady=0)
        section.grid(kwargs)

        self.treeview = ttk.Treeview(section, columns=('VALOR'))

        self.treeview.heading("#0",     text='SECÇÃO')
        self.treeview.heading('VALOR',  text='VALOR')

        self.treeview.column('#0',     width=120)
        self.treeview.column('VALOR',  width=420)

        # Constroi treeview com base no modulo atual
        module_name    = self.selectedModule.get()
        module_index   = self.modules_names.index( module_name )
        module_current = self.modules[ module_index ]

        self.render_treeview( module_current )

    def render_treeview(self, module):
        # Propriedades do modulo
        module_name = module["name"]

        # Constroi treeview com base no modulo atual
        for section, keydesc in self.mapping.items():
            # TREEVIEW para secção
            section_id = (module_name + section)
            #
            self.treeview.insert( '', 'end', section_id, text=section.upper() )
            #
            for index, module_section in enumerate(module[section]):
                #
                value = module_section[keydesc]
                # identificador
                value_id = ( section_id + keydesc + str( module_section['micro_index']) )
                # TREEVIEW para valores da secção
                self.treeview.insert( section_id, 'end', value_id, values=( value, ) )
        #
        self.treeview.pack()


    def onChangeIgnore(self):
        status = self.ignore_var.get()

        # Modulo atual
        module_name    = self.selectedModule.get()
        module_current = self.model.get_module(module_name)

        # Muda valor do ignore
        module_current["ignore"] = status


    def onChangeOptions(self, event):
        # Modulo atual
        module_name    = self.selectedModule.get()
        module_current = self.model.get_module(module_name)
        module_version = module_current["version"]
        module_ignore  = module_current["ignore"]
        #
        self.clear_tree()
        self.render_treeview( module_current )

        # UPDATE LABELS
        self.label_module_version["text"] = module_version

        # UPDATE CHECKBOXES
        self.ignore_var.set(module_ignore)

    def changeInputVar(self, event):
        #
        index = event.widget.curselection()
        #
        if not bool(index):
            return 0

        #
        key = event.widget.get(index[0])
        var = self.uninitialized_vars[key]
        val = var["value"]

        # Seta o valor da variavel no input
        self.input_var.delete(0, END)
        self.input_var.insert(0, val)

        self.selected_var = var

    def setVarValue(self, event):
        var = self.selected_var

        if var == None:
            return 0

        # Valor novo da variavel
        new_value = self.input_var.get()

        # Atualiza valor da variavel
        var["value"] = new_value

        # Atualiza o valor da variavel no TREEVIEW
        self.update_tree("vars", var)

        # Se houver caminhos dinamicos dependentes dessa variavel, atualizar eles
        if var["name"] in self.uninitialized_paths:
            # lista de caminhos modificados
            modified_paths = self.model.update_paths( var["name"] )
            #
            for key in modified_paths:
                # referencia
                path = self.model.data["paths"]["total"][key]
                # Atualiza o valor do caminho no TREEVIEW
                self.update_tree("paths", path)

    def update_tree(self, section, object):
        #
        keydesc = self.mapping[section]
        # Modulo atual selecionado
        module_name = self.selectedModule.get()
        # se objecto informado não pertencer ao modulo atual, não precisa atualizar a treeview.
        if module_name != object["module"]:
            return 0

        # Propriedades usadas para encontrar a variavel dentro do treeview
        section_id = module_name + section
        object_id  = object["micro_index"]
        value_id   = section_id + keydesc + str( object_id )
        #
        new_value  = object[keydesc]

        # Remove o antigo valor da varaivel no treeview e adiciona novo
        self.treeview.delete( value_id )
        self.treeview.insert( section_id, object_id, value_id, values=(new_value,) )

    def clear_tree(self):
        self.treeview.delete( *self.treeview.get_children() )

    def exit(self):
        self.window.quit()

    def install(self, event):
        self.window.after(1, self.window.destroy)

        # ROTINAS NECESSÁRIAS ANTES DE PASSAR MODULOS A FRENTE
        # 1 - Remove todos os modulos e ações ignoradas
        self.model.clear()
        # 2 - Valida se todas as variáveis foram setadas
        # self.model.validate

        installerGUI = MainProgressInterface(self.model)
        print(self.modules)



window=Tk()
window.title(' MERCURY SETUP')
window.resizable(False, False)
window.iconbitmap('riocardmais.ico')
window.configure(background="white")
window.style=ttk.Style()
#window.style.theme_use("clam")

MainInterface(window)

# INIT
window.mainloop()
