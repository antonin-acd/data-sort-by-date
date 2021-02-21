import os
from os import walk,path
import time
import shutil
from tkinter import *
from PIL import Image,ImageTk
import PIL
import json
import codecs
import threading

def get_json(): #on l'appel a chaque commande,si le fichier est amené a évolué au fil du programme
    with codecs.open("datas.json",encoding = "utf8") as f:
        json_file = f.read()
        f.close()
    json_file = json.loads(json_file)["content"]
    return json_file

def f_image(chemin,sizex=166,sizey=50):
    name_ph=Image.open(chemin)
    name_ph=name_ph.resize((sizex,sizey))
    name_ph=ImageTk.PhotoImage(name_ph)
    return name_ph


#Commons Valable


def reload_json():
    JSON_FILE = get_json()
    FOLDER = JSON_FILE["FOLDER"]
    FILE_FORMATS = JSON_FILE["file_formats"]
    ACCESS_PATH = JSON_FILE["chemin_dacces"]
    USER_NAME = os.getlogin()
    for i in range(len(ACCESS_PATH)):
        ACCESS_PATH[i] = ACCESS_PATH[i].replace("|username|",USER_NAME)
    return JSON_FILE,FOLDER,FILE_FORMATS,ACCESS_PATH,USER_NAME


JSON_FILE,FOLDER,FILE_FORMATS,ACCESS_PATH,USER_NAME = reload_json()




def folder_creation():
    all_folders = ["Videos","3D Objects","Musics","Pictures","Documents","Others","Folders"]
    date_now = time.strftime("%d_%b_%Y",time.localtime())
    if not path.exists(FOLDER+date_now):
        os.mkdir(FOLDER+date_now)    
        for fold in all_folders:
            if not path.exists(FOLDER+date_now+"/"+fold):
                os.mkdir(FOLDER+date_now+"/"+fold)


def get_element_date(chemin):
    file_date = time.ctime(os.path.getmtime(chemin))
    file_date = file_date.split(" ")
    file_date = [x for x in file_date if x !="" and x!=" "]
    date = str(file_date[2]) + "_" + file_date[1] + "_" + str(file_date[-1])
    return date


def get_element_of_path(path,element="fichiers"):
    list_of_file = []
    for (repertoire, sousRepertoires, fichiers) in walk(path):
        list_of_file.extend(eval(element))
        break
    return list_of_file

def rem(path):
    os.remove(path)

def chrono_file_sort(sorting_mode):
    today_date = time.strftime("%d_%b_%Y", time.localtime())
    for chemin in ACCESS_PATH:
        list_of_file = get_element_of_path(chemin,element="fichiers")
        for files in list_of_file:
            date_of_file = get_element_date(chemin+files)
            if date_of_file == today_date:
                try:
                    rem(FOLDER+today_date+"/{}/{}".format(FILE_FORMATS[i][1],files))
                except:
                    pass

                file_type = files.split(".")[-1]
                find = False
                for i in FILE_FORMATS:
                    if file_type in FILE_FORMATS[i][0]:
                        if sorting_mode == "Copy":
                            shutil.copy(chemin+files , FOLDER+today_date+"/{}/".format(FILE_FORMATS[i][1]))
                        else:
                            shutil.move(chemin+files, FOLDER+today_date+"/{}/".format(FILE_FORMATS[i][1]))
                        find = True
        
                if find == False:
                        if sorting_mode == "Copy":
                            shutil.copy(chemin+files , FOLDER+today_date+"/Others/")
                        else:
                            shutil.move(chemin+files, FOLDER+today_date+"/Others/")
        list_of_file = []

def rewrite_json(new_json):
    with open("datas.json","w") as f:
        f.write(new_json)
        f.close()

class App():
    def __init__(self):
        self.fen = Tk()
        self.fen.title("Chrono_Data_Sort")
        self.fen.geometry("400x400+760+340")
        self.fen.resizable(width=False,height=False)
        self.frequency = None
        self.sorting_mode = "Copy"
        self.statewheel = 0
        self.thr = None
        self.canvas_creation()
        self.princip_prog()
        self.fen.mainloop()
        
    
    def canvas_creation(self):
        def go_to_frequency(event):
            self.add_frequency()
        def go_to_home(event):
            self.Canv.delete("fen1item"),self.Canv.delete("fen2item"),self.Canv.delete("fen3item"),self.Canv.delete("fen4item"),self.Canv.delete("selectpathitem"),self.can_disp_paths.forget()
            self.statewheel = 0
            self.princip_prog()

        self.Canv = Canvas(self.fen,width=400,height=400,bd=-2)
        self.Canv.pack()
        self.logo_time = f_image("time_logo.png",50,50)
        self.logo_home = f_image("home.png",30,30)
        self.bg = f_image("background_2_1.jpg",400,400)
        self.Canv.create_image(200,200,image=self.bg)
        
        surve = self.Canv.create_image(390,10,anchor=NE,image=self.logo_time)
        self.Canv.tag_bind(surve,"<Button-1>",go_to_frequency)

        surve2 = self.Canv.create_image(10,390,anchor=SW,image=self.logo_home)
        self.Canv.tag_bind(surve2,"<Button-1>",go_to_home)
        

        
    def add_frequency(self):
        def valid_frequency():
            try:
                self.frequency = int(self.entrée2.get())
            except:
                self.frequency = float(self.entrée2.get())
            finally:
                self.Canv.itemconfig(self.message_erreur_2,state=NORMAL)
            self.Canv.delete("fen3item")
            self.princip_prog()

        self.Canv.delete("fen1item")
        self.Canv.delete("fen2item")
        self.Canv.create_text(200,125,text="Add Frequency",font=("Arial",23),fill="white",tags=("fen3item",))
        self.Canv.create_text(200,150,text="The frequency is the time between each save",fill="grey",tags=("fen3item",))
        self.Canv.create_text(200,165,text="You can just run it once,or all the hours if you want !",fill="grey",tags=("fen3item",))
        self.Canv.create_text(200,180,text="(The program must be on)",fill="grey",tags=("fen3item",))
        self.Canv.create_text(200,220,text="TIME IN SECONDS",fill="white",tags=("fen3item",),font=("Arial",18))
        self.entrée2 = Entry(self.Canv,font=(15))
        self.Canv.create_window(200,260,window=self.entrée2,tags=("fen3item",))
        self.ButtonThree = Button(self.Canv,text="Valid",command=valid_frequency)
        self.Canv.create_window(200,290,window=self.ButtonThree,tags=("fen3item"))
        self.message_erreur_2 = self.Canv.create_text(200,310,text="Wrong time format !",tags=("fen3item",),font=(15),fill="red",state=HIDDEN)



    def add_path(self):
        def add_to_paths():
            def exit_():
                self.Canv.delete("fen2item")
                self.relaunch_thread()
                self.princip_prog()

            new_path = self.entrée1.get()
            if new_path == "":
                self.Canv.itemconfig(self.message_erreur,state=NORMAL)
            else:
                self.Canv.itemconfig(self.message_erreur,state=HIDDEN)
                new_json_file = JSON_FILE
                new_json_file["chemin_dacces"].append(new_path)
                new_json_file = str({"content":new_json_file}).replace("'",'"')
                rewrite_json(new_json_file)
                self.Canv.itemconfig(self.message_de_reussite,state=NORMAL)
                self.Canv.after(1000,exit_)
                
        self.Canv.delete("fen1item")
        self.Canv.create_text(200,125,text="Add a path",font=("Arial",23),fill="white",tags=("fen2item",))
        self.Canv.create_text(200,150,text="A path is a folder visited by the program",fill="grey",tags=("fen2item",))
        self.Canv.create_text(200,165,text="Default paths are all the principals folders (Videos/Documents ect...)",fill="grey",tags=("fen2item",))
        self.entrée1 = Entry(self.Canv,font=(20))
        self.Canv.create_window(200,200,window=self.entrée1,tags=("fen2item",))
        self.ButtonTwo = Button(self.Canv,text="Valid",command=add_to_paths)
        self.Canv.create_window(200,230,window=self.ButtonTwo,tags=("fen2item",))
        self.message_erreur = self.Canv.create_text(200,260,text="Empty path input",state=HIDDEN,font=(15),fill="red",tags=("fen2item",))
        self.message_de_reussite = self.Canv.create_text(200,260,text="Path added !",state=HIDDEN,font=(15),fill="white",tags=("fen2item",))
    
    
    def launch_sort(self):
        if self.frequency == None:
            folder_creation()
            chrono_file_sort(self.sorting_mode)
        else:
            try:
                self.thr.Active = False
                self.thr = AtFrequency(self.frequency,self.Canv,self.timer,self.sorting_mode)
                self.thr.start()
            except:
                self.thr = AtFrequency(self.frequency,self.Canv,self.timer,self.sorting_mode)
                self.thr.start()

    def change_folder(self):
        def fonc_of_chfol():
            global JSON_FILE,FOLDER,FILE_FORMATS,ACCESS_PATH,USER_NAME
            new_folder = self.entrée3.get()
            new_json = JSON_FILE
            new_json["FOLDER"] = new_folder
            new_json = str({"content":new_json}).replace("'",'"')
            rewrite_json(new_json)
            JSON_FILE,FOLDER,FILE_FORMATS,ACCESS_PATH,USER_NAME = reload_json()
            self.Canv.delete("fen4item")
            self.relaunch_thread()
            self.princip_prog()
            


        self.Canv.delete("fen1item")
        self.Canv.create_text(200,125,text="Change Destination Folder",font=("Arial",23),fill="white",tags=("fen4item",))
        self.Canv.create_text(200,150,text="Current Destination Folder:",fill="grey",tags=("fen4item",))
        self.Canv.create_text(200,165,text=FOLDER,fill="grey",tags=("fen4item",))
        self.entrée3 = Entry(self.Canv,font=(20))
        self.Canv.create_window(200,200,window=self.entrée3,tags=("fen4item",))
        self.ButtonFour = Button(self.Canv,text="Valid",command=fonc_of_chfol)
        self.Canv.create_window(200,230,window=self.ButtonFour,tags=("fen4item",))

    def _on_mousewheel(self,event):
        if str(event.delta)[0]=="-":
            event.delta=-138
        else:
            event.delta=138

        if self.statewheel==len(ACCESS_PATH)*(-138):
            if event.delta==138:
                self.can_disp_paths.yview_scroll(round(-1*(event.delta/138)), "units")
                self.statewheel+=event.delta
            elif event.delta==-138:
                pass
        elif self.statewheel==0:
            if event.delta==-138:
                self.can_disp_paths.yview_scroll(round(-1*(event.delta/138)), "units")
                self.statewheel+=event.delta
            else:
                pass
        else:
            self.can_disp_paths.yview_scroll(round(-1*(event.delta/138)), "units")
            self.statewheel+=event.delta

    def relaunch_thread(self):
        if self.thr != None:
            try:
                self.thr.Active = False
                self.thr = AtFrequency(self.frequency,self.Canv,self.timer,self.sorting_mode)
                self.thr.start()
            except:
                self.thr = AtFrequency(self.frequency,self.Canv,self.timer,self.sorting_mode)
                self.thr.start()
            


    def select_paths(self):
        def appui(x):
            if x not in new_list:
                new_list.append(x)
            else:
                new_list.remove(x)
            
        def validation():
            global ACCESS_PATH
            ACCESS_PATH = new_list
            self.Canv.delete("selectpathitem")
            self.statewheel = 0
            self.princip_prog()
            
        local_json = get_json()
        ACCESS_PATH_1 = local_json["chemin_dacces"] 
        
        new_list = []
        self.Canv.delete("fen1item")
        self.Canv.create_text(200,125,text="Select paths",font=("Arial",23),fill="white",tags=("selectpathitem"))
        self.Canv.create_text(200,150,text="By default all paths are selected",fill="grey",tags=("selectpathitem"))
        self.Canv.create_text(200,165,text="but you can select the paths if you do not want all path",fill="grey",tags=("selectpathitem"))
        self.can_disp_paths = Canvas(self.Canv,width=400,height=120,bd=-2,bg="#191919")
        self.Canv.create_window(200,250,window=self.can_disp_paths,tags=("selectpathitem"))
        numeros = [x for x in range(len(ACCESS_PATH_1))]
        for x in numeros:
            numeros[x] = Checkbutton(self.can_disp_paths,text=ACCESS_PATH_1[x],command=lambda y=ACCESS_PATH_1[x]: appui(y),bg="#191919",fg="white",activebackground="#191919",selectcolor="#191919")
            self.can_disp_paths.create_window(200,10+20*x,window=numeros[x],tags=("selectpathitem"))
        self.can_disp_paths.bind_all("<MouseWheel>",self._on_mousewheel)
        self.Buttquatro = Button(self.Canv,text="Valid",command=validation)
        self.Canv.create_window(200,330,window=self.Buttquatro,tags=("selectpathitem",))

    def remove_path(self):
        def appui(x):
            global JSON_FILE,FOLDER,FILE_FORMATS,ACCESS_PATH,USER_NAME
            new_json = JSON_FILE
            new_json["chemin_dacces"].remove(x)
            new_json = str({"content":new_json}).replace("'",'"')
            rewrite_json(new_json)
            JSON_FILE,FOLDER,FILE_FORMATS,ACCESS_PATH,USER_NAME = reload_json()
            self.Canv.delete("selectpathitem")
            self.statewheel = 0
            self.princip_prog()

        local_json = get_json()
        ACCESS_PATH_1 = local_json["chemin_dacces"]
        self.Canv.delete("fen1item")
        self.Canv.create_text(200,125,text="Remove Path",font=("Arial",23),fill="white",tags=("selectpathitem"))
        self.Canv.create_text(200,150,text="You can choose a path to remove",fill="grey",tags=("selectpathitem"))
        self.can_disp_paths = Canvas(self.Canv,width=400,height=120,bd=-2,bg="#191919")
        self.Canv.create_window(200,250,window=self.can_disp_paths,tags=("selectpathitem"))
        numeros = [x for x in range(len(ACCESS_PATH_1))]
        for x in numeros:
            numeros[x] = Button(self.can_disp_paths,text=ACCESS_PATH_1[x],command=lambda y=ACCESS_PATH_1[x]: appui(y),bg="#191919",fg="white")
            self.can_disp_paths.create_window(200,10+20*x,window=numeros[x],tags=("selectpathitem"))
        self.can_disp_paths.bind_all("<MouseWheel>",self._on_mousewheel)


    def princip_prog(self):
        def open_folder():
            os.startfile(FOLDER)

        def mode_config(event,x):
            def hide():
                self.Canv.itemconfig(self.message_mode,text="")
            self.sorting_mode = x
            self.Canv.itemconfig(self.message_mode,text="Sorting mode changed for : {}".format(x))
            self.Canv.after(1000,hide)

        self.FolderButt = Button(self.Canv,text="Open the Folder",command=open_folder,bg="#838383",relief=FLAT)
        self.Canv.create_window(10,10,window=self.FolderButt,anchor=NW)

        self.ChangeFolder = Button(self.Canv,text="Change destination Folder",command=self.change_folder,bg="#838383",relief=FLAT)
        self.Canv.create_window(10,40,window=self.ChangeFolder,anchor=NW)

        self.ButtOne = Button(self.Canv,text="Add a path",command=self.add_path,bg="#838383",relief=FLAT,font=(15),width=13)
        self.Canv.create_window(200,150,window=self.ButtOne,tags=("fen1item",))

        self.Butttwo = Button(self.Canv,text="Select paths",command=self.select_paths,bg="#838383",relief=FLAT,font=(15),width=13)
        self.Canv.create_window(200,200,window=self.Butttwo,tags=("fen1item",))

        self.Butthree = Button(self.Canv,text="Remove path",command=self.remove_path,bg="#838383",relief=FLAT,font=(15),width=13)
        self.Canv.create_window(200,250,window=self.Butthree,tags=("fen1item",))


        self.Buttfour = Button(self.Canv,text="Sort my PC !",command=self.launch_sort,bg="#838383",relief=FLAT,font=(15),width=13)
        self.Canv.create_window(200,300,window=self.Buttfour,tags=("fen1item",))
        
        self.timer = self.Canv.create_text(200,380,text="Next save: ",state=HIDDEN,font=(13),fill="white",tags=("countdown"))

        self.Copy_logo = f_image("copy_logo.png",40,40)
        self.CopyButt = self.Canv.create_image(390,70,image=self.Copy_logo,anchor=NE,tags=("fen1item",))
        self.Canv.tag_bind(self.CopyButt,"<Button-1>",lambda x: mode_config("","Copy"))
        
        self.Deplace_logo = f_image("deplace_logo.png",40,40)
        self.DeplaceButt = self.Canv.create_image(385,120,image=self.Deplace_logo,anchor=NE,tags=("fen1item",))
        self.Canv.tag_bind(self.DeplaceButt,"<Button-1>",lambda x: mode_config("","Deplace"))

        self.message_mode = self.Canv.create_text(200,120,text="",font=(15),fill="white")


class AtFrequency(threading.Thread):
    def __init__(self,frequency,canvas,element,sorting_mode):
        threading.Thread.__init__(self)
        self.frequency = frequency
        self.canvas = canvas
        self.element = element
        self.Active = True
        self.sorting_mode = sorting_mode
    
    def run(self):
        self.canvas.itemconfig(self.element,text="")
        self.canvas.itemconfig(self.element,state=NORMAL)
        folder_creation()
        while self.Active == True:
            try:
                for i in range(self.frequency,0,-1):
                    if self.Active == True:
                        time.sleep(1)
                        self.canvas.itemconfig(self.element,text="Next save: {} s".format(i))
                    else:
                        self.canvas.itemconfig(self.element,text="")
                        break
                chrono_file_sort(self.sorting_mode)
            except:
                break
App()