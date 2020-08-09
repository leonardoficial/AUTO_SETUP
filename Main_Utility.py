from os import system

class Utility(object):

  def __init__(self):

    self.ENDC = '\033[0m'

    self.pallet = {
      "HEADER":    '\033[95m',
      "BLUE":      '\033[94m',
      "GREEN":     '\033[92m',
      "YELLOW":    '\033[93m',
      "FAIL":      '\033[91m',
      "BOLD":      '\033[1m',
      "UNDERLINE": '\033[4m'
    }

  # Print para o console
  def print(self, message, colours=[], println=False):

    message = self.paint(message, colours)

    if println:
      message = message + "\n"

    print(message)


  # Colore o texto
  def paint(self, text, colours):

    base = ""

    for colour in colours:
      base = base + self.pallet[colour]

    return base + text + self.ENDC


  # Limpa o console
  def clear(self, pause=False):

    if pause == True:
      input("")

    system("cls")


  # a
  def confirm(self, message, colours=[]):

    message = self.paint(message, colours)

    value = input(message)

    if(value == "N"):
      exit()
    else:
      print()
