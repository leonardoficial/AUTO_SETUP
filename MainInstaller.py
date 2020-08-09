
# Modulos do sistema

from shutil   import copy2    as copy_file, copytree as copy_folder
from shutil   import rmtree   as remove_folder
from os       import system   as execute, path

# DADOS
from MainModel import Model

class Console(object):

    def log(self, count, action):
        if count == 1:
            pass

# Plugins

class Installer(object):

  def __init__(self, model, console):

    #
    self.vars     = model.data["vars"]["total"]
    self.paths    = model.data["paths"]["total"]
    self.actions  = model.data["actions"]["total"]
    self.modules  = model.modules

    # Interface que recebera feedback das operações realizadas
    self.console  = console

    # Checa integridade dos arquivos no FILES
    # Checa arquitetura do sistema operacional.

    self.check()

    # Inicia sistema

    self.boot()

  """

  """
  def check(self):
    pass

  """

  """
  def boot(self):

    # CRIA ARQUIVOS TEMPORARIOS A SEREM EDITADOS
    # - BUG
    try:

      conf_root = self.paths["conf_root"]["value"]
      conf_temp = self.paths["conf_temp"]["value"]

      # LOG da acao [START]
      #self.console.log("9.1")

      # LOG da acao [PROGRESS]
      #self.console.log("9.2")

      self._copy_folder(conf_root, conf_temp)

      # LOG da acao [END]
      #self.console.log("9.3")

    except:
      pass
      # LOG da acao [ERROR]
      #self.console.error("9.9")

  """

  """
  def finish(self):

    try:
      # LOG da acao [START]
      #self.console.log("8.1")

      # LOG da acao [PROGRESS]
      #self.console.log("8.2")

      remove_folder(self.paths["conf_temp"]["value"])

      # LOG da acao [END]
      #self.console.log("8.3")

    except:
      pass
      # LOG da acao [ERROR]
      #self.console.error("8.9")

    #self.console.finish()

  """

  """
  def start(self):

    for action in self.actions:

      if(action["type"] == "COPY"):
        self.copy(action)

      if(action["type"] == "EDIT"):
        self.edit(action)

      if(action["type"] == "QUERY"):
        self.query(action)

      if(action["type"] == "EXEC"):
        self.exec(action)

    self.finish()


  """
    Substitui as variaveis dentro do arquivo
    pelos seus respectivos valores armazenados.

    Ex: substitui OSxxx pelo valor Windows NT
  """
  def edit(self, action):

    # LOG da acao [START]
    self.console.log(1, action)

    # LOG da acao [PROGRESS]
    self.console.log(2, action)

    try:
      with open(action["path"], "r", encoding="utf-8") as r_file:
        data = r_file.read()

        for rule in action["rules"]:
          value = self.vars[rule]["value"]
          data  = data.replace(rule, value)

      with open(action["path"], "w", encoding="utf-8") as w_file:
        w_file.write(data)

      action["status"] = "SUCCESS"

    except:
      action["status"] = "ERROR"

    # LOG da acao [END]
    self.console.log(3, action)


  """
    Copia o arquivo especificado para o diretorio
  """
  def copy(self, action):

    # LOG da acao [START]
    self.console.log(1, action)

    # LOG da acao [PROGRESS]
    self.console.log(2, action)

    try:
      for rule in action["rules"]:

        fpath = self.paths[rule]["value"]

        # Caso seja diretorio
        if("isFolder" in action and action["isFolder"] == True):
          self._copy_folder( action["path"], path.join(fpath, action["file"]) )

        # Caso seja arquivo
        else:
          copy_file(action["path"], fpath)

    except:
      action["status"] = "ERROR"

    # LOG da acao [END]
    self.console.log(3, action)

  """

  """
  def exec(self, action):

    # LOG da acao [START]
    self.console.log(1, action)

    # LOG da acao [PROGRESS]
    self.console.log(2, action)

    exe = action["path"]

    try:
      cmd = execute(exe)

      # Em caso de sucesso ou erro
      if(cmd == 0):
        action["status"] = "SUCCESS"
      else:
        action["status"] = "ERROR"

    except:
      action["status"] = "ERROR"

    # LOG da acao [END]
    self.console.log(3, action)

  """

  """
  def _copy_folder(self, src, dest):

    if path.exists(dest):
      remove_folder(dest)

    copy_folder(src, dest)



#4model = Model()
#model.data["vars"]["dynamics"]["DPTxxx"]["value"] = "111"
#model.data["vars"]["dynamics"]["DBServerxxx"]["value"] = "RIOCARD"
#model.update_paths("DPTxxx")

# Configura controlador de console
#console = Console()

#main = Installer(model, console)

#main.start()

#print(model.modules)
