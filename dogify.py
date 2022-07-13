#   Este programa combina archivos de imagen en un pdf y permite establecer en que orden lo hace
#   Copyright (C) 2022 Cristian Tocci
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.

#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

#   Contacto : toccicristian@hotmail.com / toccicristian@protonmail.ch

licencias = dict()
licencias['gplv3'] = """    dogify.py  Copyright (C) 2022  Cristian Tocci
    This program comes with ABSOLUTELY NO WARRANTY; for details press 'w'.
    This is free software, and you are welcome to redistribute it
    under certain conditions; See COPYING.odt file for further details.
"""
licencias['gplv3logo'] = """
+----------------------------------------------------------------------------------------------------+
|oooooooo+~~~+~~~~~~+~~~~~+~~~~+~~~~~~+~~~~+~~~~~~+~~+~~~~+~~~~~+~~~~+~~~~~~++~~+~~+~~~~~~:  ::::::~+|
|oooooooo :::::::::::::::::::::::::::::::::::::::::::~::::::::::::::::::::::::::::::::. ~~~++ooooo+:.|
|ooooooo~::::::~:::::::::::::::::::::::::::::::::::::+::::::::::::::::::::::::~~.~:~:~+oooooooooooo:.|
|ooooooo :~:~~~~~~~~~~+~::: +~~~~~~~~~~~~~::++ :::::~+~:::::::::::::::::::~...~:::~ooooooooooooooo~.+|
|oooooo~~:~oo~~~~~~~~~oo~:~+oo ~~~~~~.ooo.~oo+~::::.+o ::::::::::::::::~  .~::::+oo+~:   +ooooooo::+o|
|oooooo::.+o+~::::::~+oo : oo~::::::::oo~:~oo~::::: oo~:::::::::::::: ~ ~::::.++~ ~:::::.+oooo+~ ~ooo|
|ooooo+~:~oo~:::::::::::::~oo::::::::+oo :+oo~:::::~oo+.::::::::::.:~ ~:::::: .:::::::~~oooo+:~ +oooo|
|ooooo::~+o+.:::::::::::: oo+~:::::: oo~~:oo~::::::~ooo~::::::::.~~.::::::::::::::::~~+oooooo+~::oooo|
|oooo+~::oo~:::~:~:~~::::~oo~       ~oo::+oo.::::::~ooo+~::::: ~~.:::::::::::::::: ~+oooooooooo~~oooo|
|oooo~::+oo :::~   +oo::.ooo~~~~~~~~~:.: oo+:::::::~oooo~:::~~+:::::::::::::::: ~+++~~~~oooooo+.~oooo|
|ooo+.: oo~:::::::.oo+.:~oo~::::::::::::~oo:::::::::oooo+~::++~::::::::::::::~   .::::::ooooo~.~ooooo|
|ooo~::~oo::::::::~oo~:~+o+~::::::::::: oo+~:::::::.+ooo~.~o+:::::::::::::::::::::::: +oooo+: +oooooo|
|ooo.: oo+.~~~~~~ +oo.::oo~::::::::::::~oo~~~~~~~:::+oo~ +oo ::::::::::::::::::::.:~ooooo+: ~oooooooo|
|oo~::.~~~~~~~~~~~~~ ::~+~.::::::::::::~+~~~~~~~~~:::o~ +ooo:::::::::::::::::: ~+oooooo~::~oooooooooo|
|o+ :~   ~::::::::::::.  ~::::: ..:::::::::::::::::::~ ~oooo~~::::::::::~. ~~+oooooo+~::+oooooooooooo|
|o~~:~~: ~ :~~. ~~.::~~~~. ::.~~~~::~:: :~~.~::~~ ::::.oooooo+~~::::~~~~ooooooooo+~::~+oooooooooooooo|
|o::~~~~:::~~~ ~~~.:: ::~.~:~.~~~: ~~~ :~~~: ~~~~~:::: oooooooooooooooooooooo++~::~+ooooooooooooooooo|
|+:::~::::::~~::::::::~~:::~::~:::::::::::~::::~:::::::~ooooooooooooooooo++~::~~+oooooooooooooooooooo|
|::::::::::::::::::::::::::::::::::::::::::::::::::::::: ~oooooooooo+~~~::~~+oooooooooooooooooooooooo|
|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~:~~~~~:    ::::::::~~~ooooooooooooooooooooooooooooo|
+----------------------------------------------------------------------------------------------------+
"""
licencias['textow'] = """ 
    15. Disclaimer of Warranty.
    THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY 
    APPLICABLE LAW. EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT 
    HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM “AS IS” WITHOUT 
    WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT 
    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A 
    PARTICULAR PURPOSE. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE 
    OF THE PROGRAM IS WITH YOU. SHOULD THE PROGRAM PROVE DEFECTIVE, YOU 
    ASSUME THE COST OF ALL NECESSARY SERVICING, REPAIR OR CORRECTION.
    
    16. Limitation of Liability.
    IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING 
    WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MODIFIES AND/OR 
    CONVEYS THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR 
    DAMAGES, INCLUDING ANY GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL 
    DAMAGES ARISING OUT OF THE USE OR INABILITY TO USE THE PROGRAM 
    (INCLUDING BUT NOT LIMITED TO LOSS OF DATA OR DATA BEING RENDERED 
    INACCURATE OR LOSSES SUSTAINED BY YOU OR THIRD PARTIES OR A FAILURE OF 
    THE PROGRAM TO OPERATE WITH ANY OTHER PROGRAMS), EVEN IF SUCH HOLDER 
    OR OTHER PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.

    17. Interpretation of Sections 15 and 16.
    If the disclaimer of warranty and limitation of liability provided above 
    cannot be given local legal effect according to their terms, 
    reviewing courts shall apply local law that most closely approximates 
    an absolute waiver of all civil liability in connection with the Program, 
    unless a warranty or assumption of liability accompanies a copy of 
    the Program in return for a fee.
    """

import tkinter
from tkinter import filedialog
import os
import PIL
from PIL import Image
import pikepdf

pdf_salida_defaultdir = '~'
pdf_salida_default = 'output.pdf'


def es_imagen(path):
    try:
        tmp = Image.open(path)
        tmp.close()
        return True
    except PIL.UnidentifiedImageError:
        return False


def convierte_archivos_a_pdf(origen=None, destino=str()):
    if origen is None:
        origen = list()
    lista_img = list()
    errores = 0
    for img in origen:
        try:
            tmp_img = Image.open(img)
            if tmp_img.mode == 'RGBA':
                tmp_img = tmp_img.convert('RGB')
            lista_img.append(tmp_img)
        except PIL.UnidentifiedImageError:
            errores += 1
    lista_img[0].save(destino, 'PDF', resolution=100.0, save_all=True, append_images=lista_img[1:])
    return len(lista_img), errores


def loguea(logbox, linea=str()):
    logbox.configure(state='normal')
    logbox.insert(tkinter.END, linea)
    logbox.see(tkinter.END)
    logbox.configure(state='disabled')


def file_browser():
    tipos = (('archivos de imagen', '*.png *.jpg *.jpeg'),
             ('Todos los archivos', '*.*'))
    archivo_url = filedialog.askopenfilenames(title='Agregar Imagen...', filetypes=tipos)
    return archivo_url


def directory_browser(titulo=str(), defaultdir=str()):
    if not titulo:
        titulo = 'Seleccione directorio destino...'
    directorio = filedialog.askdirectory(title=titulo)
    if not directorio:
        directorio = defaultdir
    return os.path.expanduser(os.path.normpath(directorio))


def agregar_imagen(listbox_imagenes, logbox):
    archivo_urls = file_browser()
    for archivo_url in archivo_urls:
        listbox_imagenes.insert(tkinter.END, archivo_url)
        listbox_imagenes.see(tkinter.END)
        loguea(logbox, 'Archivo agregado: ' + str(archivo_url) + '\n')


def quitar_imagen(listbox_imagenes, logbox):
    for i in listbox_imagenes.curselection()[::-1]:
        loguea(logbox, 'Quitar :' + str(listbox_imagenes.get(i)) + '\n')
        listbox_imagenes.delete(i)


def moverarriba(listbox_imagenes):
    indices_seleccion = listbox_imagenes.curselection()
    if not indices_seleccion:
        return
    for posicion in indices_seleccion:
        if posicion == 0:
            return
        contenido = listbox_imagenes.get(posicion)
        listbox_imagenes.delete(posicion)
        listbox_imagenes.insert(posicion - 1, contenido)
    listbox_imagenes.selection_clear(0, tkinter.END)
    for indice in indices_seleccion:
        listbox_imagenes.selection_set(indice - 1)
    listbox_imagenes.see(indices_seleccion[0] - 1)


def moverabajo(listbox_imagenes):
    indices_seleccion = listbox_imagenes.curselection()
    if not indices_seleccion:
        return
    if indices_seleccion[-1] == listbox_imagenes.size() - 1:
        return
    for posicion in indices_seleccion[::-1]:
        contenido = listbox_imagenes.get(posicion)
        listbox_imagenes.delete(posicion)
        listbox_imagenes.insert(posicion + 1, contenido)
    listbox_imagenes.selection_clear(0, tkinter.END)
    for indice in indices_seleccion:
        listbox_imagenes.selection_set(indice + 1)
    listbox_imagenes.see(indices_seleccion[-1] + 1)


def examinar(entry_url):
    head_url = os.path.expanduser(os.path.normpath(pdf_salida_defaultdir))
    tail_url = os.path.expanduser(os.path.normpath(pdf_salida_default))
    if len(entry_url.get()) != 0:
        head_url = os.path.split(os.path.expanduser(os.path.normpath(entry_url.get())))[0]
        tail_url = os.path.split(os.path.expanduser(os.path.normpath(entry_url.get())))[1]
    directorio_seleccionado = directory_browser('Seleccione directorio para ' + tail_url, head_url)
    entry_url.delete(0, tkinter.END)
    if not directorio_seleccionado:
        directorio_seleccionado = head_url
    entry_url.insert(tkinter.END, os.path.join(directorio_seleccionado, tail_url))
    return


def dogify(listbox_imagenes, entry_url, logbox):
    head_url = os.path.split(os.path.expanduser(os.path.normpath(entry_url.get())))[0]
    tail_url = os.path.split(os.path.expanduser(os.path.normpath(entry_url.get())))[1]
    if (not head_url) or (not tail_url) or (not os.path.isdir(os.path.expanduser(os.path.normpath(head_url)))):
        loguea(logbox, '***No se ha generado ningún pdf: Ruta de destino no válida.\n')
        return None
    lista_imagenes = []
    for i in range(0, listbox_imagenes.size()):
        lista_imagenes.append(listbox_imagenes.get(i))
    if len(lista_imagenes) > 0:
        loguea(logbox, 'Concatenando (' + str(len(lista_imagenes)) + ') Imagenes:\n')
        resultados = convierte_archivos_a_pdf(lista_imagenes, os.path.join(head_url, tail_url))
        loguea(logbox, f'({resultados[0]}) Archivos añadidos; ({resultados[1]}) Errores\n')
        orig_sz = 0
        for f in lista_imagenes:
            if es_imagen(f):
                orig_sz += os.path.getsize(f)
        loguea(logbox, f'{str(round(orig_sz / 1024, 2))} KB en Imagenes -> '
                       f'{str(round(os.path.getsize(os.path.join(head_url, tail_url))/1024,2))} KB en {tail_url}\n')
        return None
    loguea(logbox, '***No se ha generado ningún pdf: Lista vacía.\n')


def show_w(ventana_principal, textow):
    ventana_w = tkinter.Toplevel(ventana_principal)
    ventana_w.title('This program comes with ABSOLUTELY NO WARRANTY')
    ventana_w.geometry('800x600')
    tkinter.Label(ventana_w, text=textow).pack()
    ventana_w.focus_set()
    ventana_w.bind('<Escape>', lambda event: ventana_w.destroy())


def ayuda(ventana_principal):
    texto_ayuda = """
        F1 : Esta ayuda.
        w : Más acerca de la licencia
        z : Agrega Imagen
        x : Quita Imagen
        u : Mueve hacia arriba las imágenes seleccionadas.
        j : Mueve hacia abajo las imágenes seleccionadas.
        Enter : Combina las imagenes de la lista en el pdf indicado.
        Esc : Cierra la aplicación / Cierra esta ventana
        """
    ventana_ayuda = tkinter.Toplevel(ventana_principal)
    ventana_ayuda.title(' Atajos y ayuda')
    tkinter.Label(ventana_ayuda, text=texto_ayuda, justify='left').pack(side=tkinter.LEFT, padx=(0, 30), pady=(10, 10))
    ventana_ayuda.focus_set()
    ventana_ayuda.bind('<Escape>', lambda event: ventana_ayuda.destroy())


#####################################################################################
#			GUI :
#####################################################################################
ventana = tkinter.Tk()
ventana.title("DOGIFY!")
ventana.geometry("800x600")

#               DEFINICIONES
marco_superior = tkinter.Frame(ventana)
marco_inferior = tkinter.Frame(ventana)
marco_fondo = tkinter.Frame(ventana)
marco_izquierdo = tkinter.Frame(marco_superior)
marco_derecho = tkinter.Frame(marco_superior)
marco_inferior_izquierdo = tkinter.Frame(marco_inferior)
marco_inferior_derecho = tkinter.Frame(marco_inferior)
listbox_pdfs = tkinter.Listbox(marco_izquierdo, selectmode="multiple")
scrollbar_pdfs = tkinter.Scrollbar(marco_izquierdo)
etiqueta_logbox = tkinter.Label(marco_fondo, text="Log:")
logbox = tkinter.Text(marco_fondo, height=5, width=95, state='disabled')
scrollbar_logbox = tkinter.Scrollbar(marco_fondo)
imagen_boton_agregar = tkinter.PhotoImage(file=os.path.normpath('./res/PDF_mas-64x64.png'))
imagen_boton_quitar = tkinter.PhotoImage(file=os.path.normpath('./res/PDF_menos-64x64.png'))
imagen_boton_subir = tkinter.PhotoImage(file=os.path.normpath('./res/arrow_up-32x32.png'), height=32, width=32)
imagen_boton_bajar = tkinter.PhotoImage(file=os.path.normpath('./res/arrow_down-32x32.png'), height=32, width=32)
imagen_boton_dog = tkinter.PhotoImage(file=os.path.normpath('./res/olicara-64x64.png'))
boton_agregar = tkinter.Button(marco_derecho, image=imagen_boton_agregar,
                               command=lambda: agregar_imagen(listbox_pdfs, logbox))
boton_quitar = tkinter.Button(marco_derecho, image=imagen_boton_quitar,
                              command=lambda: quitar_imagen(listbox_pdfs, logbox))
boton_subir = tkinter.Button(marco_derecho, image=imagen_boton_subir, command=lambda: moverarriba(listbox_pdfs))
boton_bajar = tkinter.Button(marco_derecho, image=imagen_boton_bajar, command=lambda: moverabajo(listbox_pdfs))
boton_dog = tkinter.Button(marco_derecho, image=imagen_boton_dog,
                           command=lambda: dogify(listbox_pdfs, entry_url, logbox))
etiqueta_entry_url = tkinter.Label(marco_inferior_izquierdo, text="Ruta y nombre del pdf a generar:")
entry_url = tkinter.Entry(marco_inferior_izquierdo, width=95)
boton_examinar = tkinter.Button(marco_inferior_derecho, text="Examinar...", command=lambda: examinar(entry_url))

#               PACKS
marco_superior.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=tkinter.YES, pady=(10, 10), padx=(10, 10))
marco_inferior.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=tkinter.YES, pady=(10, 0), padx=(10, 10))
marco_fondo.pack(side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=tkinter.YES, pady=(0, 10), padx=(10, 10))
#		                     lado izquierdo
marco_izquierdo.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=tkinter.YES, pady=(10, 10))
#				                   LISTBOX CON SCROLLBAR
listbox_pdfs.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=tkinter.YES)
scrollbar_pdfs.pack(side=tkinter.RIGHT, fill=tkinter.BOTH)
listbox_pdfs.config(yscrollcommand=scrollbar_pdfs.set)
scrollbar_pdfs.config(command=listbox_pdfs.yview)
#		lado derecho
marco_derecho.pack(side=tkinter.RIGHT, fill=tkinter.BOTH, anchor=tkinter.N)
#				botones:
boton_agregar.pack(side=tkinter.TOP, anchor=tkinter.E, pady=(10, 0), padx=(20, 10))
boton_quitar.pack(side=tkinter.TOP, anchor=tkinter.E, padx=(0, 10))
boton_subir.pack(side=tkinter.TOP, anchor=tkinter.E, pady=(40, 0), padx=(0, 10))
boton_bajar.pack(side=tkinter.TOP, anchor=tkinter.E, padx=(0, 10))
boton_dog.pack(side=tkinter.BOTTOM, anchor=tkinter.E, pady=(40, 10), padx=(0, 10))
#		abajo
marco_inferior_izquierdo.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=tkinter.YES)
marco_inferior_derecho.pack(side=tkinter.RIGHT, fill=tkinter.BOTH, expand=tkinter.YES)
etiqueta_entry_url.pack(side=tkinter.TOP, anchor=tkinter.W, pady=(0, 0))
entry_url.pack(side=tkinter.TOP, anchor=tkinter.W)
boton_examinar.pack(side=tkinter.TOP, anchor=tkinter.E, pady=(15, 0), padx=(0, 10))
#		fondo	(log y scrollbar)
etiqueta_logbox.pack(side=tkinter.TOP, anchor=tkinter.W)
logbox.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=tkinter.YES)
scrollbar_logbox.pack(side=tkinter.RIGHT, fill=tkinter.BOTH)
logbox.config(yscrollcommand=scrollbar_logbox.set)
scrollbar_logbox.config(command=logbox.yview)

#####################################################################################
#				BINDEOS:
#####################################################################################


ventana.bind('<F1>', lambda event: ayuda(ventana))
ventana.bind('<w>', lambda event: show_w(ventana, licencias['textow']))
ventana.bind('<z>', lambda event: agregar_imagen(listbox_pdfs, logbox))
ventana.bind('<x>', lambda event: quitar_imagen(listbox_pdfs, logbox))
ventana.bind('<u>', lambda event: moverarriba(listbox_pdfs))
ventana.bind('<j>', lambda event: moverabajo(listbox_pdfs))
ventana.bind('<Return>', lambda event: dogify(listbox_pdfs, entry_url, logbox))
ventana.bind('<Escape>', lambda event: ventana.destroy())
#####################################################################################
#				EL PROGRAMA:
#####################################################################################


loguea(logbox, licencias['gplv3'])
loguea(logbox, 'Presione <F1> para ayuda.\n')
logbox.see(0.0)
entry_url.insert(tkinter.END,
                 os.path.expanduser(os.path.normpath(os.path.join(pdf_salida_defaultdir, pdf_salida_default))))

ventana.mainloop()
