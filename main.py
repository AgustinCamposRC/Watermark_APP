import ttkbootstrap as ttb
import tkinter as tk
from tkinter.colorchooser import askcolor
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont
from matplotlib import font_manager
from tkinter import messagebox

filetypes = (
        ('PNG img', '*.png'),
        ('JPG img', '*.jpg'),
        ('JPEG img', '*.jpeg'),
        ('All File', '*.*')
    )

def get_fonts():
    '''Get all system fonts.\n
    Formats the fonts name, sorted and create a new dictionary.\n
    Key: "font name" without extension. Example: arial\n
    Value: "font name" with extension. Example: arial.ttf\n
    \nReturn a dict of all fonts avaible'''
    ALL_FONTS = font_manager.findSystemFonts(fontpaths=None, fontext='ttf')
    ALL_FONTS = [font.split('\\')[-1] for font in ALL_FONTS]
    ALL_FONTS.sort(key=str.casefold)
    return {font.split('.')[0]: font for font in ALL_FONTS}


def get_text_dimensions(text_string, font) -> tuple:
    '''Get the text size in pixeles\n
    Return tuple(width, height)'''
    ascent, descent = font.getmetrics()
    text_width = font.getmask(text_string).getbbox()[2]
    text_height = font.getmask(text_string).getbbox()[3] + descent
    return (text_width, text_height)


def select_file():
    '''Img path selection
    Return Selected Img path. 
    \nExample: C:downloads/hellp.png'''

    return filedialog.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes
    )


def find_img_name(path: str):
    '''Return the Selected Img name\n
    Take the absolute path of the img and split it into a list.
    \n Return img name. (Last position in the list)'''
    full_path = path.split('/')
    return full_path[-1]


def resize(size, percent):
    '''Returns the new dimensions of the image.'''
    width = size[0]
    height = size[1]
    return int((width * percent) / 100), int((height * percent) / 100)


# Lambda functions: Apply the resize function based on the axes.
resize_lambda = lambda size,axs: resize(size, 340 * 100 / axs)


def resize_base(size):
    '''Resize the Base img to set it in the GUI\n
    Check if the img with or hight are bigger than the img Area frame dimension.
    Return the new size in an tuple.
    \n Return tuple(new_width, new_height)'''
    width = size[0]
    height = size[1]
    new_size = (width, height)
    if width > 340:
        new_size = resize_lambda(size,width)
        if new_size[1] > 340:
            new_size = resize_lambda(size,height)
    elif height > 340:
        new_size = new_size = resize_lambda(size,height)
        if new_size[0] > 340:
            new_size = resize_lambda(size,width)
    return new_size



class WatermarkGUI:
    '''Watermark App GUI'''

    def __init__(self):
        self.app = tk.Tk()

        ### Variables
        self.img_path = None 
        self.img_name = None
        self.x_axi = ttb.IntVar() # Watermark x position
        self.y_axi = ttb.IntVar() # Watermark y position
        self.color = (0, 0, 0) # Watermark Text color 
        self.font = tk.StringVar(value='arial') # Watermark Text font 
        self.fonts = get_fonts() 
        self.wm_size = (0, 0) # Watermark size tuple
        self.fontsize = tk.StringVar(value=str(20)) # Watermark text size
        self.opacity = tk.DoubleVar(value=1) # watermark opacity
        self.wmi_size = tk.DoubleVar(value=0.5) # Watermark img size
        self.opacity_value = 255 # watermark opacity RGBA value
        self.watermark_txt = ttb.StringVar(value='text example') # Watermark text value
        self.watermark_img = None  # Watermark img value
        self.mode = 0  # Watermark App Mode
        self.base_img = None # Base Img value
        self.rotation = ttb.StringVar(value=0)
 
        self.app.resizable(False, False)
      
        self.app.columnconfigure(0, weight=1)
        self.app.columnconfigure(1, weight=1)
        self.create_gui_widgets()
        self.app.mainloop()


    def create_gui_widgets(self):

        '''Create App Interface (GUI).'''

        ##################################### Nav Mode Bar ########################################
        nav_menu = ctk.CTkFrame(self.app, fg_color='#262626', corner_radius=5)
        nav_menu.grid(row=0, column=0, sticky='nsew', padx=20, pady=20, ipadx=4, columnspan=2)
        nav_menu.columnconfigure(2, weight=1)
        nav_menu.anchor('w')

        titlepart1 = ttb.Label(nav_menu, text='Gust', font=('arial', 22, 'bold'), foreground="#fff", 
                               anchor='center', background='#262626')
        titlepart1.grid(row=0, column=0, pady=15, sticky='nsew', padx=8)

        titlepart2 = ttb.Label(nav_menu, text='Wm', foreground='#ED7D31', font=('arial', 22, 'bold'), 
                               anchor='center',background='#262626')
        titlepart2.grid(row=0, column=1, pady=15, sticky='nsew')

        textOption = tk.Button(nav_menu, text='Text', borderwidth=0, activebackground='#262626',
                                font=('arial', 15), foreground='white', cursor='hand2', relief='flat',
                                command=lambda: self.change_watermark_type(0))
        textOption.grid(row=0, column=2, pady=15, sticky='nse', padx=8)
        textOption.configure(background='#262626')
        textOption.bind("<Enter>", lambda e: textOption.configure(foreground='#ED7D31'))
        textOption.bind("<Leave>", lambda e: textOption.configure(foreground='#fff'))

        imageOption = tk.Button(nav_menu, text='Image', foreground='#fff', font=('arial', 15), relief='flat',
                                cursor='hand2', command=lambda:self.change_watermark_type(1))
        imageOption.configure(background='#262626')
        imageOption.grid(row=0, column=3, pady=15, padx=20, sticky='nsew')

        ###################################### App Body ##############################################

        main_body_app = tk.Frame(self.app)
        main_body_app.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=25)

            #################### Base Image Section ####################
        baseimage_frame = tk.Frame(main_body_app, )
        baseimage_frame.grid(row=1, column=0, sticky='nsew', padx=5, rowspan=2)

        tk.Label(baseimage_frame, text='Base Image:', font=('arial', 16, 'bold')).grid(row=0, column=0, sticky='w')

        baseimage_area = ctk.CTkFrame(baseimage_frame, width=350, height=350, fg_color='#ED7D31', corner_radius=6, )
        baseimage_area.grid(row=1, column=0)
        baseimage_area.grid_propagate(False)
        baseimage_area.anchor('center')

        self.placeholder_img = Image.open('./img/image_.png')
        self.placeholder_img = ImageTk.PhotoImage(self.placeholder_img.resize(resize(self.placeholder_img.size, 40)))

        self.img = tk.Label(baseimage_area, image=self.placeholder_img)
        self.img.configure(background='#ED7D31')
        self.img.grid(row=0, column=0, sticky='nsew')


        setbutt = tk.Button(baseimage_frame, text='Set Image', relief='flat', borderwidth=1, foreground='#fff',
                            font=('arial', 12), command=self.set_base_img)
        setbutt.configure(background='#6FAC46')
        setbutt.grid(row=2, column=0, sticky='nsew', pady=10, ipady=5)
        setbutt.bind('<Enter>', lambda e: setbutt.configure(background='#A2CD85'))
        setbutt.bind('<Leave>', lambda e: setbutt.configure(background='#6FAC46'))

            #################### Watermark Options Section ####################

        self.textFrame = tk.Frame(main_body_app)
        self.textFrame.grid(row=1, column=1, sticky='nsew', padx=5)
        self.textFrame.columnconfigure(0, weight=1)
        self.textFrame.columnconfigure(2, weight=1)

        watermarktext_frame = tk.Frame(self.textFrame)
        watermarktext_frame.grid(row=0, column=0, sticky='nsew',columnspan=3)
        watermarktext_frame.columnconfigure(1, weight=1)

                #################### Watermark text Options Section ####################
        ttb.Label(watermarktext_frame, text='Text:', font=('arial', 13, 'bold'), )\
            .grid(row=0, column=0, sticky='nsew', padx=4, pady=4)
        self.wm_text_entry = ttb.Entry(watermarktext_frame, font=('arial', 12), bootstyle='danger', 
                                       textvariable=self.watermark_txt,width=40)
        self.watermark_txt.trace_add('write', self.set_watermark_text)
        self.wm_text_entry.grid(row=0, column=1, ipady=4, ipadx=1, 
                                columnspan=2, padx=5, pady=5,sticky='nsew')

                #################### Watermark text Color Options Section ####################
        tk.Label(self.textFrame, text='Color:', font=('arial', 13, 'bold'))\
            .grid(row=1, column=0, sticky='w', padx=4, pady=4)

        color_selection_section = tk.Frame(self.textFrame)
        color_selection_section.grid(row=2, column=0, ipady=4, ipadx=1, columnspan=2, sticky='w')

        self.colors_entry = ttb.Entry(color_selection_section, font=('arial', 11), width=15, bootstyle='success',
                                     justify='center', state='readnoly')
        self.colors_entry.grid(row=0, column=0, ipady=4, ipadx=1, pady=5, padx=8)
        self.colors_entry.insert(0,'#000000')

        color_butt = tk.Button(color_selection_section, text='Set', background='#6FAC46', relief='flat', borderwidth=1,
                               foreground='#fff',
                               font=('arial', 12), command=self.change_color)
        color_butt.grid(row=0, column=1, pady=5, ipadx=3, ipady=1, sticky='nsew')
        color_butt.configure(background='#6FAC46')
        color_butt.bind('<Enter>', lambda e: color_butt.configure(background='#A2CD85'))
        color_butt.bind('<Leave>', lambda e: color_butt.configure(background='#6FAC46'))

                #################### Watermark text font Options Section ####################
        tk.Label(self.textFrame, text='Font:', font=('arial', 13, 'bold'))\
            .grid(row=3, column=0, sticky='w', padx=4, pady=4)
        
        self.font_selection = ttb.Combobox(self.textFrame, font=('arial', 12), bootstyle='success',
                                           values=list(self.fonts.keys()), foreground='black', textvariable=self.font)
        self.font_selection.grid(row=4, column=0, ipadx=1, columnspan=2, sticky='nsew', padx=8,pady=2)
        self.font.trace_add("write", self.select_font)

                #################### Watermark Opacity Options Section ####################
        tk.Label(self.textFrame, text='Opacity:', font=('arial', 13, 'bold'))\
            .grid(row=5, column=0, sticky='w', padx=4, pady=4)
        opacity_selection_section = tk.Frame(self.textFrame, background='red')
        opacity_selection_section.grid(row=6, column=0, ipady=4, ipadx=1, columnspan=2, sticky='nsew', padx=8)
        opacity_selection_section.columnconfigure(0, weight=1)
        opacity_selection_section.rowconfigure(0, weight=1)
        
        self.opacity.trace_add('write', self.opacity_callback)
        self.opacity_selection = ttb.Scale(opacity_selection_section, orient='horizontal', bootstyle='success',
                                      variable=self.opacity, )
        self.opacity_selection.grid(row=0, column=0, ipady=4, ipadx=1, sticky='nsew', padx=2)

        self.opacity_label = tk.Label(opacity_selection_section, font=('arial', 13, 'bold'), text='100%')
        self.opacity_label.grid(row=0, column=1, sticky='nsew', padx=2, pady=4)

                #################### Watermark text size Options Section ####################
        tk.Label(self.textFrame, text='Size:', font=('arial', 13, 'bold'))\
            .grid(row=7, column=0, sticky='w', padx=4, pady=4)
        self.size_selection = ttb.Combobox(self.textFrame, values=[x for x in range(1, 201)], bootstyle='success',
                                          textvariable=self.fontsize, font=('arial', 12))
        self.size_selection.grid(row=8, column=0, ipadx=1, columnspan=2, sticky='new', padx=8)

        self.fontsize.trace_add(mode='write', callback=self.fontsize_callback)


                #################### Watermark IMG size Options Section ####################
        tk.Label(self.textFrame, text='Size Wm Img:', font=('arial', 13, 'bold'))\
            .grid(row=7, column=2, sticky='w', padx=4,pady=5)

        wmi_size_section = tk.Frame(self.textFrame, background='red')
        wmi_size_section.grid(row=8, column=2, ipady=4, ipadx=1, sticky='nsew', padx=8)
        self.wmi_size.trace_add('write', self.wmi_size_callback)

        self.wmi_size_selection = ttb.Scale(wmi_size_section, orient='horizontal', bootstyle='success',
                                      variable=self.wmi_size, from_=0.01, to=1)
        self.wmi_size_selection.grid(row=0, column=0, ipady=4, ipadx=1, sticky='nsew', padx=2)
        wmi_size_section.columnconfigure(0, weight=1)

        wmi_size_section.rowconfigure(0, weight=1)
        self.wmi_size_label = tk.Label(wmi_size_section, font=('arial', 13, 'bold'), 
                                       text=f'{int(self.wmi_size.get()*100)}')
        self.wmi_size_label.grid(row=0, column=1, sticky='nsew', padx=2, pady=4)

        #################### Watermark Position Options Section ####################
        position_frame = tk.Frame(self.textFrame, )
        position_frame.grid(row=1, column=2, rowspan=6, sticky='nsew', pady=8)
        position_frame.columnconfigure(0, weight=1)

        tk.Label(position_frame, text='Position:', font=('arial', 13, 'bold'))\
            .grid(row=0, column=0, sticky='w', padx=4, columnspan=2)
    
        self.up_img = Image.open('./img/up.png')
        self.up_img = ImageTk.PhotoImage(self.up_img)

        self.left_img = Image.open('./img/left.png')
        self.left_img = ImageTk.PhotoImage(self.left_img)

        self.right_img = Image.open('./img/rigth.png')
        self.right_img = ImageTk.PhotoImage(self.right_img)

        self.down_img = Image.open('./img/down.png')
        self.down_img = ImageTk.PhotoImage(self.down_img)

        buttons_position_frame = tk.Frame(position_frame)
        buttons_position_frame.grid(row=1, column=0, sticky='nsew')
        buttons_position_frame.anchor('center')
        background_color = buttons_position_frame.cget('bg')
        up = tk.Button(buttons_position_frame, image=self.up_img, relief='flat', borderwidth=0,
                  command=self.up)
        up.grid(row=1, column=0, columnspan=2, sticky='s')
        up.configure(background=background_color, activebackground=background_color)

        left = tk.Button(buttons_position_frame, image=self.left_img, relief='flat', borderwidth=0,
                  command=self.left)
        left.grid(row=2, column=0, padx=27)
        left.configure(background=background_color, activebackground=background_color)

        right = tk.Button(buttons_position_frame, image=self.right_img, relief='flat', borderwidth=0,
                  command=self.right)
        right.grid(row=2, column=1, padx=29)
        right.configure(background=background_color, activebackground=background_color)
        down = tk.Button(buttons_position_frame, image=self.down_img, relief='flat', borderwidth=0,
                  command=self.down)
        down.grid(row=3, column=0, columnspan=2, sticky='n')
        down.configure(background=background_color, activebackground=background_color)


        labels_position_frame = tk.Frame(position_frame, )
        labels_position_frame.grid(row=2, column=0, sticky='nsew', pady=10, padx=4)
        labels_position_frame.anchor('center')

        tk.Label(labels_position_frame, text='X axis:', font=('arial', 11, 'bold'))\
            .grid(row=0, column=0, sticky='nsew', padx=4, columnspan=2)
        self.x_position = ttb.Entry(labels_position_frame, width=10, textvariable=self.x_axi)
        self.x_position.grid(row=1, column=0)
        self.x_position.bind('<FocusOut>', lambda e: self.set_manual_position(self.x_axi, self.x_position,0))
        self.x_position_label = tk.Label(labels_position_frame, text='/ 0', font=('arial', 11), width=8, anchor='w')
        self.x_position_label.grid(row=1, column=1, sticky='w', padx=4, )


        tk.Label(labels_position_frame, text='Y axis:', font=('arial', 11, 'bold'))\
            .grid(row=0, column=2, sticky='nsew', padx=4, columnspan=2)
        self.y_position = ttb.Entry(labels_position_frame, width=10, textvariable=self.y_axi)
        self.y_position.grid(row=1, column=2)
        self.y_position.bind('<FocusOut>', lambda e: self.set_manual_position(self.y_axi, self.y_position,1))
        self.y_position_label = tk.Label(labels_position_frame, text='/ 0', anchor='w', font=('arial', 11), width=8)
        self.y_position_label.grid(row=1, column=3, sticky='w', padx=4, )

        tk.Label(position_frame, text='Rotation:', font=('arial', 13, 'bold'))\
            .grid(row=0, column=1, sticky='w', padx=4, columnspan=2)
        rotate_buttons_position_frame = tk.Frame(position_frame)
        rotate_buttons_position_frame.grid(row=1, column=1, sticky='nsew')
        rotate_buttons_position_frame.anchor('center')

        left = tk.Button(rotate_buttons_position_frame, image=self.left_img, relief='flat', borderwidth=0,
                  command=self.rotate_left)
        left.grid(row=2, column=0, padx=2)
        left.configure(background=background_color, activebackground=background_color)

        right = tk.Button(rotate_buttons_position_frame, image=self.right_img, relief='flat', borderwidth=0,
                  command=self.rotate_right)
        right.grid(row=2, column=1, padx=2)
        right.configure(background=background_color, activebackground=background_color)

        degrees_frame = ttb.Frame(rotate_buttons_position_frame)
        degrees_frame.grid(row=3, column=0, columnspan=2)

        tk.Label(degrees_frame, text='X axis:', font=('arial', 11, 'bold'))\
            .grid(row=0, column=0, sticky='nsew', padx=4, columnspan=2)
        self.degrees_entry = ttb.Entry(degrees_frame, width=10, textvariable=self.rotation)
        self.degrees_entry.grid(row=1, column=0)
        self.rotation.trace_add('write', self.set_manual_degrees)
        self.degrees_label = tk.Label(degrees_frame, text='Degrees', font=('arial', 11), anchor='w')
        self.degrees_label.grid(row=1, column=1, sticky='w', padx=4, )

        #################### Buttons Sections ####################
        complete_frame = tk.Frame(main_body_app, )
        complete_frame.grid(row=2, column=1, sticky='new', padx=5,pady=6)
        complete_frame.columnconfigure(0, weight=1)
        complete_frame.columnconfigure(1, weight=1)

        tk.Label(complete_frame, text='Save Image', font=('arial', 13, 'bold'))\
            .grid(row=0, column=0, sticky='w', padx=4, pady=8)

        apply_but = tk.Button(complete_frame, text='Save', background='#6FAC46', relief='flat', borderwidth=1,
                              foreground='#fff', command=self.save_img, font=('arial', 12), )
        apply_but.grid(row=1, column=0, ipadx=3, ipady=1, )
        apply_but.configure(background='#6FAC46')
        apply_but.bind('<Enter>', lambda e: apply_but.configure(background='#A2CD85'))
        apply_but.bind('<Leave>', lambda e: apply_but.configure(background='#6FAC46'))

        restart_butt = tk.Button(complete_frame, text='Restart', relief='flat', borderwidth=1, foreground='#fff',
                  font=('arial', 12), command=self.restart)
        restart_butt.config(background='#EF782F', activebackground='#EF782F', activeforeground='#F4EFD4')
        restart_butt.bind('<Enter>', lambda e: restart_butt.configure(background='#F2A068'))
        restart_butt.bind('<Leave>', lambda e: restart_butt.configure(background='#EF782F'))
        restart_butt.grid(row=1, column=1, ipadx=3, ipady=1)


    def set_base_img(self,):
        """Allow to Set the Base image """
        self.img_path = select_file()
        if self.img_path != '':
            self.img_name = find_img_name(self.img_path)
            self.selectedImg = Image.open(self.img_path)
            self.x_position_label['text'] = f"/ {self.selectedImg.size[0]}"
            self.y_position_label['text'] = f'/ {self.selectedImg.size[1]}'
            self.selectedImg = ImageTk.PhotoImage(self.selectedImg.resize(size=resize_base(self.selectedImg.size)))
            self.img['image'] = self.selectedImg
            self.check_watermark_type()

    
    def select_overlay_img_form(self):
        '''Open the overlay img selection window'''
        self.overlay_window  = ttb.Toplevel(title='Overlay Image - Watermark')
        baseimage_frame = tk.Frame(self.overlay_window, )
        baseimage_frame.grid(row=1, column=0, sticky='nsew', rowspan=2, padx=10, pady=10)

        ttb.Label(baseimage_frame, text='Watermark Image:', font=('arial', 16, 'bold')).grid(row=0, column=0, sticky='w', pady=5)

        overlay_area = ctk.CTkFrame(baseimage_frame, width=350, height=350, fg_color='#ED7D31', corner_radius=6, )
        overlay_area.grid(row=1, column=0)
        overlay_area.grid_propagate(False)
        overlay_area.anchor('center')

        self.overlayImg = tk.Label(overlay_area, image=self.placeholder_img)
        self.overlayImg.configure(background='#ED7D31')
        self.overlayImg.grid(row=0, column=0, sticky='nsew')

        buttons_frame = tk.Frame(baseimage_frame)
        buttons_frame.grid(row=2, column=0, sticky='nsew', pady=10)
        buttons_frame.columnconfigure(0, weight=1)
        buttons_frame.columnconfigure(1, weight=1)

        setbutt = tk.Button(buttons_frame, text='Set', relief='flat', borderwidth=1, foreground='#fff',
                            font=('arial', 12), command=self.set_overlay_img)
        setbutt.configure(background='#6FAC46')
        setbutt.grid(row=0, column=0, ipadx=3, ipady=1)
        setbutt.bind('<Enter>', lambda e: setbutt.configure(background='#A2CD85'))
        setbutt.bind('<Leave>', lambda e: setbutt.configure(background='#6FAC46'))

        remove = tk.Button(buttons_frame, text='Remove', relief='flat', borderwidth=1, foreground='#fff',
                  font=('arial', 12))
        remove.configure(background='#C00000')
        remove.grid(row=0, column=1, ipadx=3, ipady=1)


    def set_overlay_img(self,):
        """Allow to Set the watermark image """
        self.watermark_img = select_file()
        if self.watermark_img is not None:
            self.selectedOvImg = Image.open(self.watermark_img)
            self.selectedOvImg = ImageTk.PhotoImage(self.selectedOvImg.resize(size=resize_base(self.selectedOvImg.size)))
            self.overlayImg['image'] = self.selectedOvImg
            if self.base_img != '':
                self.add_watermark_img()
            self.overlay_window.destroy()
    

    def add_watermark_img(self):
        '''Set watermark img in the base img'''
        if self.img_path is not None and self.watermark_img is not None:
            self.base_img = Image.open(self.img_path) # Take Base img
            overlay_img = Image.open(self.watermark_img) # Take overlay img (watermark img)
            overlay_img = overlay_img.resize(size=(resize(overlay_img.size,int(self.wmi_size.get()*100))))
            if overlay_img.mode == 'RGBA':
                im2 = overlay_img.copy()
                im2.putalpha(int(self.opacity_value))
                overlay_img.paste(im2, overlay_img)
            else:
                overlay_img = overlay_img.convert('RGBA')
                overlay_img.putalpha(int(self.opacity_value))
            overlay_img = overlay_img.rotate(angle=int(self.rotation.get()),resample=Image.BILINEAR, expand=True)
            self.wm_size = overlay_img.size
            self.base_img.paste(overlay_img, (self.x_axi.get(), self.y_axi.get()), overlay_img)
            self.newImage= ImageTk.PhotoImage(self.base_img.resize(size=resize_base(self.base_img.size)))
            self.img['image'] = self.newImage


    def add_watermark_text(self):
        '''Set watermark text in the base img'''
        if self.img_path is not None: 
            color = list(self.color)
            color.append(int(self.opacity_value))
            if self.watermark_txt.get() !="":
                self.base_img = Image.open(self.img_path).convert('RGBA')
                txt = Image.new('RGBA', self.base_img.size, (250,250,250,0))
                mf = ImageFont.truetype(f'{self.fonts[self.font.get()]}', int(self.fontsize.get()))
                draw_base = ImageDraw.Draw(txt)
                self.wm_size = get_text_dimensions(self.watermark_txt.get(), mf)
                draw_base.text((self.x_axi.get(), self.y_axi.get()), self.watermark_txt.get(), font=mf, fill=tuple(color))
                txt = txt.rotate(int(self.rotation.get()))
                self.result_img = Image.alpha_composite(self.base_img, txt)
                self.newImage = ImageTk.PhotoImage(self.result_img.resize(size=resize_base(self.result_img.size)))
                self.img['image'] = self.newImage


    def check_watermark_type(self):
        '''Check watermark type'''
        if self.mode == 0:
            self.add_watermark_text()
        else:
            self.add_watermark_img()

    
    def block_text_edition(self, STATE):
        '''Change the status of the following widgets'''
        self.wm_text_entry['state'] = STATE
        self.colors_entry['state'] = STATE
        self.font_selection['state'] = STATE
        self.size_selection['state'] = STATE
    

    def change_watermark_type(self, mode):
        '''Determine the type of watermark'''
        self.restart()
        if mode == 0:
            self.block_text_edition(ttb.NORMAL)
            self.add_watermark_text()
            self.wmi_size_selection['state'] = ttb.DISABLED
            self.mode = 0
        else:
            self.block_text_edition(ttb.DISABLED)
            self.select_overlay_img_form()
            self.wmi_size_selection['state'] = ttb.NORMAL
            self.mode=1

    ############################# Watermark Text Edition Fucntions #############################

    def set_watermark_text(self, var, index, mode):
        """Set the watermark text"""
        self.add_watermark_text()


    def change_color(self):
        '''Set watermark text color '''
        colors = askcolor(title="Tkinter Color Chooser")
        if colors != (None,None):
            self.colors_entry.delete(0, ttb.END)
            self.colors_entry.insert(0, str(colors[1]))
            self.color = colors[0]
            self.add_watermark_text()


    def select_font(self, var, index, mode):
        '''Set the watermark font type'''
        self.add_watermark_text()


    def fontsize_callback(self, var, index, mode):
        '''Set the watermark font size'''
        if self.img_path is not None:
            self.check_watermark_dimension()
            self.add_watermark_text()

    
    def opacity_callback(self, var, index, mode):
        '''Set watermark opacity'''
        percentage = self.opacity.get()
        self.opacity_label['text'] = f"{int(percentage*100)}%"
        self.opacity_value = 255 * percentage
        self.check_watermark_type()

    
    def wmi_size_callback(self, var, index, mode):
        """Set Watermark image size"""
        percentage = self.wmi_size.get()
        self.wmi_size_label['text'] = f"{int(percentage*100)}%"
        if self.watermark_img is not None:
            self.check_watermark_dimension()
            self.add_watermark_img()


    def check_watermark_dimension(self):
        '''Checks if the watermark is outside the base image'''
        x_axi_excessive = self.base_img.size[0] - (self.wm_size[0]+self.x_axi.get())
        y_axi_excessive = self.base_img.size[1] - (self.wm_size[1]+self.y_axi.get())
        if x_axi_excessive<0:
            self.x_axi.set(self.x_axi.get()+x_axi_excessive)
        if self.x_axi.get()<0:
            self.x_axi.set(0)
        if y_axi_excessive<0:
            self.y_axi.set(self.y_axi.get()+y_axi_excessive)
        if self.y_axi.get()<0:
            self.y_axi.set(0)


    ############################# Watermark positioning functions #############################


    def set_manual_position(self, var, index, mode):
        '''Manually set the watermark position'''
        if self.img_path is not None:  
            self.check_watermark_type()


    def set_manual_degrees(self, axi_var, axi_entry: ttb.Entry, axi_num):
        '''Manually set the watermark degrees rotation'''
        if self.img_path is not None:  
            if self.rotation.get() != "":
                self.check_watermark_type()


    def up(self):
        '''Move up the watermark'''
        if self.img_path is not None and int(self.y_axi.get()) > 0:
            self.y_axi.set(self.y_axi.get() - 10)
            self.check_watermark_type()


    def down(self):
        '''Move down the watermark'''
        if self.img_path is not None and int(self.y_axi.get()) < (self.base_img.size[1]-self.wm_size[1]):
            self.y_axi.set(self.y_axi.get() + 10)
            self.check_watermark_type()


    def left(self):
        '''Move left the watermark'''
        if self.img_path is not None and int(self.x_axi.get()) > 0:
            self.x_axi.set(self.x_axi.get() - 10)
            self.check_watermark_type()


    def right(self):
        '''Move right the watermark'''
        if self.img_path is not None and int(self.x_axi.get()) < (self.base_img.size[0] - self.wm_size[0]):
            self.x_axi.set(self.x_axi.get() + 10)
            self.check_watermark_type()


    def rotate_left(self):
        '''Rotate left the watermark'''
        if self.img_path is not None:
            self.rotation.set(int(self.rotation.get())-5)
            self.check_watermark_type()

    
    def rotate_right(self):
        '''Rotate right the watermark'''
        if self.img_path is not None:
            self.rotation.set(int(self.rotation.get())+5)
            self.check_watermark_type()

    
    #######################################################

    def restart(self):
        self.x_axi.set(0)
        self.y_axi.set(0)
        self.color = (0, 0, 0)
        self.colors_entry.delete(0, tk.END)
        self.colors_entry.insert(0,'#000000')
        self.opacity_value = 255
        self.opacity.set(1)
        self.font.set('arial')
        self.fontsize.set(str(22))
        self.check_watermark_type()


    def save_img(self):
        if self.img_path is not None:
            path = filedialog.asksaveasfilename(confirmoverwrite=True, initialfile=self.img_name,
                                                filetypes=(('PNG img', '*.png'),))
            if path != '':
                self.result_img.save(path)
                messagebox.showinfo(title='New Img', message='Image Save it correctly')

    
WatermarkGUI()

