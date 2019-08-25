import math
import datetime
import time

class C_GA_Log():
    '''
    My Logging class
    '''
    def __init__(self):
        self.reset()




    def reset(self):
        self.log = {}
        try:
            if self.now == datetime.datetime.now():
                time.sleep(1.1)
        except:
                pass
        self.now = datetime.datetime.now()
        self.run_id = (str(self.now)[0:10]+"_"+str(self.now)[11:19])
        # print("LOG_START: {run_id}".format(run_id=self.run_id))


    def log_score(self):
        print("Loging   score empty")
        pass

    def log_this(self,function_type,chance,eta,quantity):

        try:
            self.log.get(function_type).get(chance).update({eta:quantity})
        except AttributeError:
            #FIX not existing elements
            #FIX function_type element
            if self.log.get(function_type) == None:
                self.log.update({function_type:{}})
                print("Added new log function_type: '{0}'".format(function_type))
            #fix chance element
            if self.log.get(function_type).get(chance) == None:
                """Verify if "function_type" exist"""
                self.log.get(function_type).update({chance:{}})

    def export_to_file(self,file_link,mode="w"):
        file = open(file_link,mode)
        for function_type,dict_chance in self.log.items():
            for chance,dict_eta in dict_chance.items():
                for eta,quantity in dict_eta.items():
                    file.write("{};{};{};{};{}\n".\
                        format(self.run_id,function_type,chance,eta,quantity))
        file.close()
        self.reset()

    def log_print(self):
        for function_type,dict_chance in self.log.items():
            for chance,dict_eta in dict_chance.items():
                for eta,quantity in dict_eta.items():
                    print(self.run_id,function_type,chance,eta,quantity)
