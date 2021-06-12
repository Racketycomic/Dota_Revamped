import time
import os

directory = os.path.join("/home/vinay/fsproject2/app", "app.log")
k = "*"


class logclear():

    def clearlog(self):
            with open(directory,"w+") as file:
                file.write(k)
                print(k)
