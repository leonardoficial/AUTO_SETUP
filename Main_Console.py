
# Modulos do sistema

from os      import system
from os.path import join
from json    import load

# Modulos de dependencia

from Main_Utility import Utility

class Console(Utility):

  def __init__(self, config=False):

    # Convoca setup da classe Utility

    super().__init__()

    # Configuracao padrao

    if(config == False):

      config = { "root": "CONFIG", "file": "language.json" }

    # Prepara e carrega o arquivo de idioma

    fpath = join(config["root"], config["file"])

    try:
      with open(fpath, "r", encoding="utf-8") as data:
        self.language = load(data)

    except:
      print("ERROR %s" % fpath)
      exit()

  # Introducao do sistema
  def boot(self, variables):
      pass

  # Encerramento do sistema
  def finish(self):
    pass


  # Trata logs do sistema
  def log(self, ID, values=False):

    # Valor padrao
    if(values == False):
      values = { "file": "" }

    # Apenas printa logs de fim da acao
    if ID[2] == "3":

      name = values["file"]

      print(self.language[ID] % name)

  # Trata erros.do sistema
  def error(self, ID, values=False):

    # Valor padrao
    if(values == False):
      values = { "file": "" }

    print(self.language[ID])



#console = Console()

#console.log("2.1", { "file": "aaaaa"})

#console.data({ "DPTxxx": None, "HEHxxx": None })
