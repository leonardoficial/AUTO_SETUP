from os.path import join
from json    import load, dumps

class Model(object):

    def __init__(self, config=False):

        # Objeto final contendo os modulos modificados
        # Contem referencias a variaveis nao inicializadas
        # Contem referencias a caminhos dinamicos
        self.data = {
            # statics  = Fila de valores estaticos inputados no arquivo
            # dynamics = Fila de valores a serem alterados na interface
            "vars":    { "dynamics": {}, "statics": {}, "total": {} },
            "paths":   { "dynamics": {}, "statics": {}, "total": {} },
            "actions": { "dynamics": [], "statics": [], "total": [] }
        }

        # Modulos modificados
        self.modules = []

        # Nomes dos modulos carregados
        self.modules_names = []

        # Contador de modulos, variaveis, caminhos e ações
        # Usando principalmente para criar IDs
        self.counter_var    = -1
        self.counter_path   = -1
        self.counter_action = -1
        self.counter_module = -1

        # Configuracao padrao
        if(config == False):
            config = { "root": "CONFIG", "file": "modules.json" }
            #config = { "root": "CONFIG", "file": "temp_model.json" }

        # Caminho absoluto do arquivo de configurações
        fpath = join(config["root"], config["file"])

        # Tenta ler arquivo de configurações
        # Caso não consiga, encerra aplicação
        #try:
        with open(fpath, "r", encoding="utf-8") as modules:
                #  Carrega modulos
            modules = load(modules)
        #except Exception as error:
            #print("ERRO AO ABRIR ARQUIVO %s" % fpath)
            #exit()

        # A
        for module in modules:
            # Modulo deve ser ignorada
            if module["ignore"] == True:
                continue

            # Atualiza o contador total de de variaveis
            self.counter_module = self.counter_module + 1
            # Usado para identificar o modulo
            module["index"] = self.counter_module
            # Adiciona modulo ao objeto
            self.modules.append(module)
            # Salva nome do modulo
            self.modules_names.append(module["name"])

            # Verifica se modulo tem interface correta
            self.test(module)

            # CARREGA VARIAVEIS
            self.handle_vars(module)

            # CARREGA CAMINHOS
            self.handle_paths(module)

            # CARREGA AÇÕES
            self.handle_actions(module)

    def test(self, data):
        pass

    #   CARREGA VARIAVEIS
    def handle_vars(self, module):

        # Usando para localizar o objeto dentro do modulo especifico
        micro_id = -1
        # Carrega variaveis no sistema
        for var in module["vars"]:

            name = var["name"]

            # Atualiza o contator de variaveis do modulo
            micro_id = micro_id + 1
            # Atualiza o contador total de de variaveis
            self.counter_var = self.counter_var + 1
            # IDs da variavel
            var["macro_index"] = self.counter_var
            var["micro_index"] = micro_id
            # Nome do modulo a que pertence
            var["module"] = module["name"]

            if var["status"] == False:
                _queue_ = "dynamics"
            else:
                _queue_ = "statics"

            # Adiciona objeto a fila apropriada e referencia a fila total
            self.data["vars"][_queue_][name] = var
            self.data["vars"]["total"][name] = var

    #   CARREGA CAMINHOS ABSOLUTOS
    def handle_paths(self, module):
        # Usando para localizar o objeto dentro do modulo especifico
        micro_id = -1
        # Carrega os caminhos
        for path in module["paths"]:

            name = path["name"]
            base = path["base"]
            root = path["root"]

            # Atualiza o contator de variaveis do modulo
            micro_id = micro_id + 1
            # Atualiza o contador de variaveis
            self.counter_path = self.counter_path + 1
            # IDs da variavel
            path["macro_index"] = self.counter_path
            path["micro_index"] = micro_id
            # Nome do modulo a que pertence
            path["module"] = module["name"]
            # Cria estrutura de nodes
            # Guarda referencia aos nodes superiores
            # Guarda referencia aos nodes inferiores
            if len(root) > 0:
                # Elementos pai do objeto path
                parentNd = self.data["paths"]["total"][root]

                # Adiciona root como objeto pai
                path["parentNodes"].append(root)
                path["parentNodes"].extend(parentNd["parentNodes"])

                # Adiciona este objeto como filho do objeto pai
                parentNd["childNodes"].append(name)

                # Caminho absoluto do root
                root = self.data["paths"]["total"][root]["value"]

            # seta caminho absoluto do objecto
            path["value"] = join(root, base)

            # Se objeto for 'puro', seu valor é estatico.
            # Logo seu valor nao necessita ser alterado posteriormente.
            if path["pure"] == False:
                _queue_ = "dynamics"
            else:
                _queue_ = "statics"

            # Adiciona objeto a fila apropriada e referencia a fila total
            self.data["paths"][_queue_][name] = path
            self.data["paths"]["total"][name] = path

    def handle_actions(self, module):
        # Usando para localizar o objeto dentro do modulo especifico
        micro_id = -1
        # Adiciona ações
        for action in module["actions"]:

            name = module["name"]
            file = action["file"]
            type = action["type"]

            # Atualiza o contator de variaveis do modulo
            micro_id = micro_id + 1
            # Atualiza o contador de variaveis
            self.counter_action = self.counter_action + 1
            # IDs da variavel
            action["macro_index"] = self.counter_action
            action["micro_index"] = micro_id
            # Nome do modulo a que pertence
            action["module"] = module["name"]
            # Ação deve ser ignorada
            if action["ignore"] == True:
                continue

            # Seta o caminho do arquivo
            action["path"] = join( self.data["paths"]["total"][name]["value"], file )

            # Adiciona objeto a fila apropriada e referencia a fila total
            #self.actions[_queue_].append(action)
            self.data["actions"]["total"].append(action)

    def update_paths(self, var_name):

        # Caminhos que foram modificados
        modified_paths = []

        if len(self.data["paths"]["dynamics"]) == 0:
            return 0

        # ALTERA PATHS QUE NECESSITAM DE ACAO
        def recurse(path, oldvalue, newvalue):
            # Adiciona caminho a lista de modificados
            modified_paths.append(path["name"])
            # Referencia aos nodes inferiores
            childNodes = path["childNodes"]
            # Modifica path do objecto atual
            path["value"] = path["value"].replace(oldvalue, newvalue)
            # Se houver node inferior na arvore desse
            if len(childNodes) > 0:

                for child in childNodes:
                    child = self.data["paths"]["total"][child]
                    recurse(child, oldvalue, newvalue)

            return path

        key = var_name
        val = self.data["paths"]["dynamics"][var_name]
        # Valor da variavel a ser modificada no paths
        newvalue = self.data["vars"]["total"][key]["value"]
        # Modifica path dos nodes
        recurse(val, key, newvalue)
        # Adiciona variavel a fila de estaticas
        self.data["paths"]["total"][key] = val

        # Esvazia fila de caminhos a serem modificadas
        del self.data["paths"]["dynamics"][var_name]

        return modified_paths

    # RETORNA MODULO REQUISITADO
    def get_module(self, key):

        if type(key) == int:
            module = self.modules[key]
        else:
            index  = self.modules_names.index(key)
            module = self.modules[index]

        return module

    # REMOVE TODOS OS MODULOS E AÇÕES MARCADAS COM IGNORE
    def clear(self):
        # QUANTIDADE DE ITENS RMEOVIDOS
        removed_modules = []
        removed_actions = []

        for i in range( len(self.modules) ):
            # INDEX DO MODULO
            index = i - len( removed_modules )
            # MODULO ATUAL
            module = self.modules[ index ]
            # CASO MODULO ESTEJA MARCADO COM IGNORE
            if module["ignore"] == True:
                # REMOVE MODULO
                del self.modules[index]
                # INCREMENTA QUANTIDADE DE REMOVIDOS
                removed_modules.append(module["name"])


        # REMOVE AÇÕES DESTE MODULO
        for queue_name, queue in self.data["actions"].items():
            # LOOP EM CADA TARGET NA FILA
            for i in range( len(queue) ):
                # INDEX DO TARGET
                target_index = i - len( removed_actions )
                #
                target = queue[target_index]
                # SE MODULO DESTA AÇÃO FOI REMOVIDO
                if target["module"] in removed_modules:
                    # REMOVE TARGET
                    del queue[target_index]
                    # ADICIONA AÇÃO A LISTA DE REMOVIDOS
                    removed_actions.append( target["desc"] )

        # RETORNA LISTA DE MODULOS REMOVIDOS
        return removed_modules

    def set_ignore(self, target, value):
        pass


#model = Model()
#foo = model.update_paths("DPTxxx")
#module2 = model.get_module("UDP_GARAGE")
#module2["ignore"] = True
#print(module)
#removed_modules = model.clear()
#print(removed_modules)
#print(removed_modules)
#print( len(model.data["actions"]["total"]) )
#print(model.modules)
