import webbrowser
from customtkinter import *
import conexionmysql
from tkinter import messagebox
import pytz
from datetime import datetime
import pyperclip
import json


def registrar():
    usuario = entrada1.get()
    contrasenia = entrada2.get()
    if '@gmail.com' not in usuario:
        messagebox.showinfo('Atención', 'El usuario debe ser un correo de Gmail válido.')
        return

    conection1 = conexionmysql.Connection()
    resultado = conection1.consulta_usuario(usuario, contrasenia)

    if resultado:
        messagebox.showinfo('atencion', 'el usuario ya existe')
    else:
        conection1.inserta_usuario(usuario, contrasenia)
        messagebox.showinfo('Felicidades', 'Registro exitoso')

    conection1.cerrar_conexion()


def eliminar():
    usuario = entrada1.get()
    contrasenia = entrada2.get()
    conection1 = conexionmysql.Connection()
    resultado = conection1.consulta_usuario(usuario, contrasenia)
    if resultado:
        contenido = messagebox.askyesno('atencion', '¿ desea continuar ?')
        if contenido:
            conection1.borrar_usuario(usuario, contrasenia)
            messagebox.showinfo('atencion', 'el usuario a sido eliminado')
        else:
            messagebox.showinfo('atencion', 'aun conservas tu usuario')
    else:
        messagebox.showinfo('atencion', 'el usuario no existe')

    conection1.cerrar_conexion()


def ingresar():
    usuario = entrada1.get()
    contrasenia = entrada2.get()
    conection1 = conexionmysql.Connection()
    resultado = conection1.consulta_usuario(usuario, contrasenia)
    if resultado:
        ventana1.state('zoomed')
        ventana1.title('Area de trabajo')
        frame1.place_forget()
        frame2.place(x=20, y=20)
        frame3.place(x=700, y=20)
        frame4.place(x=20, y=490)
        frame5.place(x=700, y=330)
        frame6.place(x=1070, y=490)

    conection1.cerrar_conexion()


try:
    with open("datos_notas.json", "r") as archivo_json:
        datos_notas = json.load(archivo_json)
except FileNotFoundError:
    datos_notas = {}


# Función para guardar los datos en el archivo JSON
def guardar_datos():
    with open("datos_notas.json", "w") as archivo_json:
        json.dump(datos_notas, archivo_json)


# Función para crear una nueva nota
def crear_nota():
    titulo = entrada7.get()
    contenido = cuadrotexto.get(1.0, END)

    datos_notas[titulo] = contenido.strip()
    guardar_datos()

    opciones.append(titulo)
    combo2['values'] = opciones


# Función para cargar notas guardadas en el combo2
def cargar_notas():
    print(datos_notas.keys())
    valores_lista = list(datos_notas.keys())
    print(valores_lista)
    combo2.configure(values=valores_lista)
    combo2.update()


# Función para ver la nota seleccionada en el cuadrotexto
def ver_nota():
    seleccion = combo2.get()
    contenido = datos_notas.get(seleccion, "")
    cuadrotexto.delete(1.0, END)
    cuadrotexto.insert(END, contenido)
    nota = cuadrotexto.get(1.0, END)
    pyperclip.copy(nota)


# Función para eliminar la nota seleccionada
def eliminar_nota():
    seleccion = combo2.get()
    if seleccion in datos_notas:
        del datos_notas[seleccion]
        guardar_datos()

        # Convertir la selección y los valores de la lista a minúsculas para comparar
        seleccion_min = seleccion.lower()
        opciones_lower = [opcion.lower() for opcion in opciones]

        if seleccion_min in opciones_lower:
            opciones.remove(opciones[opciones_lower.index(seleccion_min)])
            combo2['values'] = opciones
            cuadrotexto.delete(1.0, END)
    else:
        print("La nota seleccionada no existe.")


def mostrar_hora():
    pais = combo1.get()

    try:
        zona_horaria = pytz.timezone(paises_zonas[pais])
        hora_actual = datetime.now(tz=zona_horaria)
        hora_formateada = hora_actual.strftime('%H:%M:%S')

        label1.configure(text=f"Hora en {pais}: {hora_formateada}")
    except KeyError:
        label1.configure(text="Seleccione un país válido.")

    frame2.after(1000, mostrar_hora)


paises_zonas = {
    "Argentina": "America/Argentina/Buenos_Aires",
    "Bolivia": "America/La_Paz",
    "Chile": "America/Santiago",
    "Ecuador": "America/Guayaquil",
    "Paraguay": "America/Asuncion",
    "Perú": "America/Lima",
    "Uruguay": "America/Montevideo",
    "Venezuela": "America/Caracas",
    "Costa Rica": "America/Costa_Rica",
    "El Salvador": "America/El_Salvador",
    "Guatemala": "America/Guatemala",
    "Honduras": "America/Tegucigalpa",
    "Nicaragua": "America/Managua",
    "Panamá": "America/Panama",
    "República Dominicana": "America/Santo_Domingo"
}


def copiar_contenido_entrada3():
    contenido = entrada3.get()
    pyperclip.copy(contenido)


def copiar_contenido_entrada4():
    contenido = entrada4.get()
    pyperclip.copy(contenido)


def copiar_contenido_entrada5():
    contenido = entrada5.get()
    pyperclip.copy(contenido)


def copiar_contenido_entrada6():
    contenido = entrada6.get()
    pyperclip.copy(contenido)


def modificar_numero():
    contenido = entrada6.get()
    numerosinespacios = (contenido.replace(" ", "").replace("(", "").replace(")", "").replace("-", "").replace("_", "")
                         .replace("+54", "").replace("+591", "").replace("+56", "").replace("+593", "")
                         .replace("+595", "").replace("+51", "").replace("+598", "").replace("+58", "")
                         .replace("+506", "").replace("+503", "").replace("+502", "").replace("+504", "")
                         .replace("+505", "").replace("+507", "").replace("+1", "").replace("0054", "")
                         .replace("00591", "").replace("0056", "").replace("00593", "")
                         .replace("00595", "").replace("0051", "").replace("00598", "").replace("0058", "")
                         .replace("00506", "").replace("00503", "").replace("00502", "").replace("00504", "")
                         .replace("00505", "").replace("00507", "").replace("001", ""))
    entrada6.delete(0, END)
    entrada6.insert(END, numerosinespacios)


def verificar_codigopais():
    pais = combo1.get()
    if pais in codigointernacional:
        return codigointernacional[pais]


codigointernacional = {
    "Argentina": "+54",
    "Bolivia": "+591",
    "Chile": "+56",
    "Ecuador": "+593",
    "Paraguay": "+595",
    "Perú": "+51",
    "Uruguay": "+598",
    "Venezuela": "+58",
    "Costa Rica": "+506",
    "El Salvador": "+503",
    "Guatemala": "+502",
    "Honduras": "+504",
    "Nicaragua": "+505",
    "Panamá": "+507",
    "República Dominicana": "+1"
}


def insertar_codigopais():
    contenido = verificar_codigopais()
    if contenido:
        entrada_actual = entrada6.get()
        nuevo_contenido = contenido + entrada_actual
        entrada6.delete(0, END)
        entrada6.insert(0, nuevo_contenido)


def abrirhu():
    pais = obtener_pais()
    numeroorden = entrada4.get()
    urlhu = 'https://{}.us.logisticsbackoffice.com/dispatcher/order_details/{}'.format(pais, numeroorden)
    webbrowser.open_new_tab(urlhu)


def abrirbo():
    numero_de_orden = entrada4.get()
    urlbo = 'https://backoffice-app.pedidosya.com/#/orders/' + numero_de_orden
    webbrowser.open_new_tab(urlbo)


def abrirhu2():
    pais = obtener_pais()
    numero_de_orden = entrada4.get()
    urlhu2 = 'http://{}.us.logisticsbackoffice.com/dashboard/v2/hurrier/order_details/{}'.format(
        pais, numero_de_orden)
    webbrowser.open_new_tab(urlhu2)


def obtener_pais():
    pais = combo1.get()

    if pais == 'Argentina':
        pais = 'ar'
    elif pais == 'Bolivia':
        pais = 'bo'
    elif pais == 'Chile':
        pais = 'cl'
    elif pais == 'Ecuador':
        pais = 'ec'
    elif pais == 'Paraguay':
        pais = 'py'
    elif pais == 'Perú':
        pais = 'pe'
    elif pais == 'Uruguay':
        pais = 'uy'
    elif pais == 'Venezuela':
        pais = 've'
    elif pais == 'Costa Rica':
        pais = 'cr'
    elif pais == 'El Salvador':
        pais = 'sv'
    elif pais == 'Guatemala':
        pais = 'gt'
    elif pais == 'Honduras':
        pais = 'hn'
    elif pais == 'Nicaragua':
        pais = 'ni'
    elif pais == 'Panamá':
        pais = 'pa'
    elif pais == 'República Dominicana':
        pais = 'do'
    return pais


def obtener_segmento():
    segmento = entrada5.get()

    url3 = 'https://lookerstudio.google.com/u/0/reporting/7d96f4bb-a653-4240-bd71-' \
           'b4e7c2b0bb12/page/p_9sq6spxkxc?params=%7B%22df11%22:%22include%25EE%2580%25801%25EE' \
           '%2580%2580EQ%25EE%2580%2580{}%22%7D'.format(segmento)

    webbrowser.open_new_tab(url3)


def enlace_hurrier():
    pais = obtener_pais()
    numeroorden = entrada4.get()
    urlhu = 'https://{}.us.logisticsbackoffice.com/dispatcher/order_details/{}'.format(pais, numeroorden)
    pyperclip.copy(urlhu)
    return urlhu


def verpelican():
    pais = obtener_pais()
    numeroorden = entrada4.get()
    urlpelican = (f'https://ops-portal.pedidosya.com/{pais}/p/shopper?random=6oowjlogtyd#/orders/all?star'
                  f'tDate=2023-06-08&orderId={numeroorden}')

    webbrowser.open_new_tab(urlpelican)


def verdarkstore():
    urldarkstore = 'https://docs.google.com/spreadsheets/d/16FL3G2TPC7xY0hxgtTQ8LXuZ6B-njFfr/edit?pli=1#gid=1595429039'
    webbrowser.open_new_tab(urldarkstore)


def limpiar():
    entrada3.delete(0, END)
    entrada4.delete(0, END)
    entrada5.delete(0, END)
    entrada6.delete(0, END)
    cuadrotexto2.delete(1.0, END)


def reporteic():
    mail = entrada8.get()
    numero = entrada6.get()
    pais = obtener_pais()
    datos = f'{mail}\n{enlace_hurrier()}\n{numero}\n{pais}\nmotivo: llamadas canceladas'
    pyperclip.copy(datos)


def nota_nombre():
    nombre = entrada3.get()
    cuadrotexto2.insert(END, '{}//'.format(nombre))


def nota_ox():
    nota1 = 'O.X//'
    cuadrotexto2.insert(END, nota1)


def nota_sa():
    nota2 = 'S.A//'
    cuadrotexto2.insert(END, nota2)


def nota_rs():
    nota3 = '//RS'
    cuadrotexto2.insert(END, nota3)


def nota_cancelo():
    nota4 = '//cancelo orden'
    cuadrotexto2.insert(END, nota4)


def nota_reasigno():
    nota5 = '//reasigno orden'
    cuadrotexto2.insert(END, nota5)


def nota_divido():
    nota6 = '//divido orden'
    cuadrotexto2.insert(END, nota6)


def nota_solucion():
    nota7 = '//envio solucion '
    cuadrotexto2.insert(END, nota7)


def nota_llamoconexito():
    nota8 = '//llamo con exito'
    cuadrotexto2.insert(END, nota8)


def nota_llamosinexito():
    nota9 = '//llamo sin exito'
    cuadrotexto2.insert(END, nota9)


def nota_icx():
    nota10 = '//no puedo llamar ICX'
    cuadrotexto2.insert(END, nota10)


def nota_sega():
    nota11 = '//segmento A'
    cuadrotexto2.insert(END, nota11)


def nota_segb():
    nota12 = '//segmento B'
    cuadrotexto2.insert(END, nota12)


def nota_activopausa():
    nota13 = '//activo pausa'
    cuadrotexto2.insert(END, nota13)


def nota_desactivopausa():
    nota14 = '//desactivo pausa'
    cuadrotexto2.insert(END, nota14)


def nota_pedidocancelado():
    pais = combo1.get()
    nota15 = '{} PedidoCancelado'.format(pais)
    cuadrotexto2.insert(END, nota15)


def nota_deliveryinverso():
    nota16 = 'DeliveryInverso'
    cuadrotexto2.insert(END, nota16)


def copiarcuadrotexto2():
    contenido = cuadrotexto2.get('1.0', 'end-1c')
    pyperclip.copy(contenido)


def nota_panamaparaguay():
    nota17 = 'D2'
    cuadrotexto2.insert(END, nota17)


def nota_devolucionbolivia():
    nota18 = 'DevolucionBolivia'
    cuadrotexto2.insert(END, nota18)


def nota_devolucionnicaragua():
    nota19 = 'D2Nicaragua'
    cuadrotexto2.insert(END, nota19)


def nota_feedback():
    nota20 = 'realizo Feedback'
    cuadrotexto2.insert(END, nota20)


def copiar_contenido_entrada8():
    contenido = entrada8.get()
    pyperclip.copy(contenido)


ventana1 = CTk()
ventana1.geometry('500x260+400+180')
ventana1.title('Login')
ventana1.configure(fg_color='black')

frame1 = CTkFrame(ventana1,
                  bg_color='black',
                  fg_color='black',
                  width=460,
                  height=220,
                  corner_radius=15,
                  border_width=3,
                  border_color='green'
                  )
frame1.place(x=20, y=20)

entrada1 = CTkEntry(frame1,
                    bg_color='black',
                    fg_color='black',
                    width=400,
                    height=40,
                    corner_radius=10,
                    border_width=3,
                    border_color='purple',
                    text_color='#FD8D14',
                    placeholder_text_color='#FFE17B',
                    placeholder_text='usuario@gmail.com',
                    font=('Arial', 16, 'bold'),
                    justify='center'
                    )
entrada1.place(x=30, y=30)

entrada2 = CTkEntry(frame1,
                    bg_color='black',
                    fg_color='black',
                    width=400,
                    height=40,
                    corner_radius=10,
                    border_width=3,
                    border_color='purple',
                    text_color='#FD8D14',
                    placeholder_text_color='#FFE17B',
                    placeholder_text='contraseña',
                    font=('Arial', 16, 'bold'),
                    show='*',
                    justify='center'
                    )
entrada2.place(x=30, y=80)

boton1 = CTkButton(frame1,
                   bg_color='black',
                   fg_color='#FFE17B',
                   width=130,
                   height=40,
                   text_color='black',
                   font=('Arial', 16, 'bold'),
                   corner_radius=8,
                   text='Registrar',
                   command=registrar
                   )
boton1.place(x=30, y=140)

boton2 = CTkButton(frame1,
                   bg_color='black',
                   fg_color='#FFE17B',
                   width=130,
                   height=40,
                   text_color='black',
                   font=('Arial', 16, 'bold'),
                   corner_radius=8,
                   text='Eliminar',
                   command=eliminar
                   )
boton2.place(x=165, y=140)

boton3 = CTkButton(frame1,
                   bg_color='black',
                   fg_color='#FFE17B',
                   width=130,
                   height=40,
                   text_color='black',
                   font=('Arial', 16, 'bold'),
                   corner_radius=8,
                   text='Ingresar',
                   command=ingresar
                   )
boton3.place(x=300, y=140)

frame2 = CTkFrame(ventana1,
                  bg_color='black',
                  fg_color='black',
                  width=650,
                  height=450,
                  corner_radius=15,
                  border_width=3,
                  border_color='green'
                  )

frame3 = CTkFrame(ventana1,
                  bg_color='black',
                  fg_color='black',
                  width=650,
                  height=300,
                  corner_radius=15,
                  border_width=3,
                  border_color='green'
                  )

entrada3 = CTkEntry(frame2,
                    bg_color='black',
                    fg_color='black',
                    width=400,
                    height=40,
                    corner_radius=10,
                    border_width=3,
                    border_color='purple',
                    text_color='#FD8D14',
                    placeholder_text_color='#FFE17B',
                    placeholder_text='Nombre de rider',
                    font=('Arial', 16, 'bold'),
                    justify='center'
                    )
entrada3.place(x=30, y=30)
boton4 = CTkButton(frame2,
                   bg_color='black',
                   fg_color='#FFE17B',
                   width=130,
                   height=40,
                   text_color='black',
                   font=('Arial', 16, 'bold'),
                   corner_radius=8,
                   text='copiar',
                   command=copiar_contenido_entrada3
                   )
boton4.place(x=430, y=30)

entrada4 = CTkEntry(frame2,
                    bg_color='black',
                    fg_color='black',
                    width=400,
                    height=40,
                    corner_radius=10,
                    border_width=3,
                    border_color='purple',
                    text_color='#FD8D14',
                    placeholder_text_color='#FFE17B',
                    placeholder_text='Numero de orden',
                    font=('Arial', 16, 'bold'),
                    justify='center'
                    )
entrada4.place(x=30, y=80)
boton5 = CTkButton(frame2,
                   bg_color='black',
                   fg_color='#FFE17B',
                   width=130,
                   height=40,
                   text_color='black',
                   font=('Arial', 16, 'bold'),
                   corner_radius=8,
                   text='copiar',
                   command=copiar_contenido_entrada4
                   )
boton5.place(x=430, y=80)

entrada5 = CTkEntry(frame2,
                    bg_color='black',
                    fg_color='black',
                    width=400,
                    height=40,
                    corner_radius=10,
                    border_width=3,
                    border_color='purple',
                    text_color='#FD8D14',
                    placeholder_text_color='#FFE17B',
                    placeholder_text='ID del rider',
                    font=('Arial', 16, 'bold'),
                    justify='center'
                    )
entrada5.place(x=30, y=130)

boton6 = CTkButton(frame2,
                   bg_color='black',
                   fg_color='#FFE17B',
                   width=130,
                   height=40,
                   text_color='black',
                   font=('Arial', 16, 'bold'),
                   corner_radius=8,
                   text='copiar',
                   command=copiar_contenido_entrada5
                   )
boton6.place(x=430, y=130)

entrada6 = CTkEntry(frame2,
                    bg_color='black',
                    fg_color='black',
                    width=280,
                    height=40,
                    corner_radius=10,
                    border_width=3,
                    border_color='purple',
                    text_color='#FD8D14',
                    placeholder_text_color='#FFE17B',
                    placeholder_text='Telefono',
                    font=('Arial', 16, 'bold'),
                    justify='center'
                    )
entrada6.place(x=90, y=180)

boton14 = CTkButton(frame2,
                    bg_color='black',
                    fg_color='#FFE17B',
                    width=50,
                    height=40,
                    text_color='black',
                    font=('Arial', 16, 'bold'),
                    corner_radius=8,
                    text='pais',
                    command=insertar_codigopais
                    )
boton14.place(x=30, y=180)

boton7 = CTkButton(frame2,
                   bg_color='black',
                   fg_color='#FFE17B',
                   width=100,
                   height=40,
                   text_color='black',
                   font=('Arial', 16, 'bold'),
                   corner_radius=8,
                   text='copiar',
                   command=copiar_contenido_entrada6
                   )
boton7.place(x=490, y=180)

boton9 = CTkButton(frame2,
                   bg_color='black',
                   fg_color='#FFE17B',
                   width=100,
                   height=40,
                   text_color='black',
                   font=('Arial', 16, 'bold'),
                   corner_radius=8,
                   text='modificar',
                   command=modificar_numero
                   )
boton9.place(x=380, y=180)

label1 = CTkLabel(frame2,
                  width=350,
                  height=40,
                  font=('Arial', 16, 'bold'),
                  text_color='black',
                  bg_color='black',
                  fg_color='#FD8D14',
                  corner_radius=15,
                  text="Seleccione un país"
                  )
label1.place(x=30, y=230)

boton8 = CTkButton(frame2,
                   bg_color='black',
                   fg_color='#FFE17B',
                   width=130,
                   height=40,
                   text_color='black',
                   font=('Arial', 16, 'bold'),
                   corner_radius=8,
                   text='mostrar hora',
                   command=mostrar_hora
                   )

boton8.place(x=390, y=230)

combo1 = CTkComboBox(frame2,
                     bg_color='black',
                     fg_color='black',
                     border_color='purple',
                     button_color='blue',
                     button_hover_color='blue',
                     text_color='white',
                     corner_radius=8,
                     font=('Arial', 16, 'bold'),
                     justify='center',
                     dropdown_font=('Arial', 16, 'bold'),
                     dropdown_fg_color='blue',
                     dropdown_text_color='white',
                     dropdown_hover_color='green',
                     width=280,
                     height=40,
                     values=list(paises_zonas.keys()),
                     state='readonly'
                     )
combo1.place(x=30, y=280)

boton9 = CTkButton(frame2,
                   bg_color='black',
                   fg_color='#FFE17B',
                   width=100,
                   height=40,
                   text_color='black',
                   font=('Arial', 16, 'bold'),
                   corner_radius=8,
                   text='HU',
                   command=abrirhu
                   )

boton9.place(x=30, y=330)

boton10 = CTkButton(frame2,
                    bg_color='black',
                    fg_color='#FFE17B',
                    width=100,
                    height=40,
                    text_color='black',
                    font=('Arial', 16, 'bold'),
                    corner_radius=8,
                    text='HU2',
                    command=abrirhu2
                    )

boton10.place(x=140, y=330)

boton11 = CTkButton(frame2,
                    bg_color='black',
                    fg_color='#FFE17B',
                    width=100,
                    height=40,
                    text_color='black',
                    font=('Arial', 16, 'bold'),
                    corner_radius=8,
                    text='BO',
                    command=abrirbo
                    )

boton11.place(x=250, y=330)

boton12 = CTkButton(frame2,
                    bg_color='black',
                    fg_color='#FFE17B',
                    width=100,
                    height=40,
                    text_color='black',
                    font=('Arial', 16, 'bold'),
                    corner_radius=8,
                    text='ver segmento',
                    command=obtener_segmento
                    )

boton12.place(x=360, y=330)

botonpelican = CTkButton(frame2,
                         bg_color='black',
                         fg_color='#FFE17B',
                         width=150,
                         height=40,
                         text_color='black',
                         font=('Arial', 16, 'bold'),
                         corner_radius=8,
                         text='ver pelican',
                         command=verpelican
                         )

botonpelican.place(x=490, y=330)

botondarkstore = CTkButton(frame2,
                           bg_color='black',
                           fg_color='#FFE17B',
                           width=150,
                           height=40,
                           text_color='black',
                           font=('Arial', 16, 'bold'),
                           corner_radius=8,
                           text='ver darkstore',
                           command=verdarkstore
                           )

botondarkstore.place(x=490, y=380)

boton13 = CTkButton(frame2,
                    bg_color='black',
                    fg_color='#FFE17B',
                    width=100,
                    height=40,
                    text_color='black',
                    font=('Arial', 16, 'bold'),
                    corner_radius=8,
                    text='copiar enlace HU',
                    command=enlace_hurrier
                    )

boton13.place(x=30, y=380)

boton15 = CTkButton(frame2,
                    bg_color='black',
                    fg_color='#A076F9',
                    width=100,
                    height=40,
                    text_color='black',
                    font=('Arial', 16, 'bold'),
                    corner_radius=8,
                    text='Limpiar todo',
                    command=limpiar
                    )

boton15.place(x=350, y=280)

boton16 = CTkButton(frame3,
                    bg_color='black',
                    fg_color='#FFE17B',
                    width=150,
                    height=40,
                    text_color='black',
                    font=('Arial', 16, 'bold'),
                    corner_radius=8,
                    text='crear solucion',
                    command=crear_nota
                    )

boton16.place(x=30, y=230)

cuadrotexto = CTkTextbox(frame3,
                         border_width=3,
                         border_color='green',
                         width=300,
                         height=200,
                         bg_color='black',
                         fg_color='black',
                         text_color='white',
                         font=('Arial', 16, 'bold')
                         )

cuadrotexto.place(x=30, y=30)

entrada7 = CTkEntry(frame3,
                    bg_color='black',
                    fg_color='black',
                    width=300,
                    height=40,
                    corner_radius=10,
                    border_width=3,
                    border_color='purple',
                    text_color='#FD8D14',
                    placeholder_text_color='#FFE17B',
                    placeholder_text='nombre para solucion',
                    font=('Arial', 16, 'bold'),
                    justify='center'
                    )
entrada7.place(x=340, y=30)

boton17 = CTkButton(frame3,
                    bg_color='black',
                    fg_color='#FFE17B',
                    width=200,
                    height=40,
                    text_color='black',
                    font=('Arial', 16, 'bold'),
                    corner_radius=8,
                    text='Recargar lista',
                    command=cargar_notas
                    )

boton17.place(x=340, y=80)

opciones = []
combo2 = CTkComboBox(frame3,
                     border_width=3,
                     border_color='purple',
                     text_color='white',
                     fg_color='black',
                     bg_color='black',
                     width=200,
                     height=40,
                     justify='center',
                     button_color='blue',
                     button_hover_color='blue',
                     dropdown_fg_color='blue',
                     dropdown_text_color='white',
                     dropdown_hover_color='green',
                     values=opciones
                     )
combo2.place(x=340, y=130)

boton18 = CTkButton(frame3,
                    bg_color='black',
                    fg_color='#FFE17B',
                    width=80,
                    height=40,
                    text_color='black',
                    font=('Arial', 16, 'bold'),
                    corner_radius=8,
                    text='ver',
                    command=ver_nota
                    )

boton18.place(x=550, y=130)

boton19 = CTkButton(frame3,
                    bg_color='black',
                    fg_color='#FFE17B',
                    width=80,
                    height=40,
                    text_color='black',
                    font=('Arial', 16, 'bold'),
                    corner_radius=8,
                    text='borrar',
                    command=eliminar_nota
                    )

boton19.place(x=550, y=180)

frame4 = CTkFrame(ventana1,
                  bg_color='black',
                  fg_color='black',
                  width=1030,
                  height=210,
                  corner_radius=15,
                  border_width=3,
                  border_color='green'
                  )

cuadrotexto2 = CTkTextbox(frame4,
                          border_width=3,
                          border_color='green',
                          width=300,
                          height=160,
                          bg_color='black',
                          fg_color='black',
                          text_color='white',
                          font=('Arial', 16, 'bold')
                          )

cuadrotexto2.place(x=20, y=20)

boton37 = CTkButton(frame4,
                    bg_color='black',
                    fg_color='#FFE17B',
                    width=100,
                    height=40,
                    text_color='black',
                    font=('Arial', 16, 'bold'),
                    corner_radius=8,
                    text='copiar',
                    command=copiarcuadrotexto2,
                    border_color='purple',
                    border_width=2
                    )

boton37.place(x=220, y=140)

boton20 = CTkButton(frame4,
                    bg_color='black',
                    fg_color='#FFE17B',
                    width=80,
                    height=40,
                    text_color='black',
                    font=('Arial', 16, 'bold'),
                    corner_radius=8,
                    text='Nombre',
                    command=nota_nombre,
                    border_color='purple',
                    border_width=2
                    )

boton20.place(x=330, y=20)

boton21 = CTkButton(frame4,
                    bg_color='black',
                    fg_color='#FFE17B',
                    width=80,
                    height=40,
                    text_color='black',
                    font=('Arial', 16, 'bold'),
                    corner_radius=8,
                    text='O.X',
                    command=nota_ox,
                    border_color='purple',
                    border_width=2
                    )

boton21.place(x=330, y=60)

boton22 = CTkButton(frame4,
                    bg_color='black',
                    fg_color='#FFE17B',
                    width=80,
                    height=40,
                    text_color='black',
                    font=('Arial', 16, 'bold'),
                    corner_radius=8,
                    text='S.A',
                    command=nota_sa,
                    border_color='purple',
                    border_width=2
                    )

boton22.place(x=330, y=100)

boton23 = CTkButton(frame4,
                    bg_color='black',
                    fg_color='#FFE17B',
                    width=80,
                    height=40,
                    text_color='black',
                    font=('Arial', 16, 'bold'),
                    corner_radius=8,
                    text='RS',
                    command=nota_rs,
                    border_color='purple',
                    border_width=2
                    )

boton23.place(x=330, y=140)

boton24 = CTkButton(frame4,
                    bg_color='black',
                    fg_color='#FFE17B',
                    width=90,
                    height=40,
                    text_color='black',
                    font=('Arial', 16, 'bold'),
                    corner_radius=8,
                    text='cancelo',
                    command=nota_cancelo,
                    border_color='purple',
                    border_width=2
                    )

boton24.place(x=420, y=20)

boton25 = CTkButton(frame4,
                    bg_color='black',
                    fg_color='#FFE17B',
                    width=90,
                    height=40,
                    text_color='black',
                    font=('Arial', 16, 'bold'),
                    corner_radius=8,
                    text='Reasigno',
                    command=nota_reasigno,
                    border_color='purple',
                    border_width=2
                    )

boton25.place(x=420, y=60)

boton26 = CTkButton(frame4,
                    bg_color='black',
                    fg_color='#FFE17B',
                    width=90,
                    height=40,
                    text_color='black',
                    font=('Arial', 16, 'bold'),
                    corner_radius=8,
                    text='divido',
                    command=nota_divido,
                    border_color='purple',
                    border_width=2
                    )

boton26.place(x=420, y=100)

boton27 = CTkButton(frame4,
                    bg_color='black',
                    fg_color='#FFE17B',
                    width=90,
                    height=40,
                    text_color='black',
                    font=('Arial', 16, 'bold'),
                    corner_radius=8,
                    text='Solucion',
                    command=nota_solucion,
                    border_color='purple',
                    border_width=2
                    )

boton27.place(x=420, y=140)

boton28 = CTkButton(frame4,
                    bg_color='black',
                    fg_color='#FFE17B',
                    width=130,
                    height=40,
                    text_color='black',
                    font=('Arial', 16, 'bold'),
                    corner_radius=8,
                    text='llamo con exito',
                    command=nota_llamoconexito,
                    border_color='purple',
                    border_width=2
                    )

boton28.place(x=530, y=20)

boton29 = CTkButton(frame4,
                    bg_color='black',
                    fg_color='#FFE17B',
                    width=130,
                    height=40,
                    text_color='black',
                    font=('Arial', 16, 'bold'),
                    corner_radius=8,
                    text='llamo sin exito',
                    command=nota_llamosinexito,
                    border_color='purple',
                    border_width=2
                    )

boton29.place(x=530, y=60)

boton30 = CTkButton(frame4,
                    bg_color='black',
                    fg_color='#FFE17B',
                    width=130,
                    height=40,
                    text_color='black',
                    font=('Arial', 16, 'bold'),
                    corner_radius=8,
                    text='ICX',
                    command=nota_icx,
                    border_color='purple',
                    border_width=2
                    )

boton30.place(x=530, y=100)

boton41 = CTkButton(frame4,
                    bg_color='black',
                    fg_color='#FFE17B',
                    width=130,
                    height=40,
                    text_color='black',
                    font=('Arial', 16, 'bold'),
                    corner_radius=8,
                    text='Feedback',
                    command=nota_feedback,
                    border_color='purple',
                    border_width=2
                    )

boton41.place(x=530, y=140)

boton31 = CTkButton(frame4,
                    bg_color='black',
                    fg_color='#FFE17B',
                    width=130,
                    height=40,
                    text_color='black',
                    font=('Arial', 16, 'bold'),
                    corner_radius=8,
                    text='Segmento A',
                    command=nota_sega,
                    border_color='purple',
                    border_width=2
                    )

boton31.place(x=680, y=20)

boton32 = CTkButton(frame4,
                    bg_color='black',
                    fg_color='#FFE17B',
                    width=130,
                    height=40,
                    text_color='black',
                    font=('Arial', 16, 'bold'),
                    corner_radius=8,
                    text='Segmento B',
                    command=nota_segb,
                    border_color='purple',
                    border_width=2
                    )

boton32.place(x=680, y=60)

boton33 = CTkButton(frame4,
                    bg_color='black',
                    fg_color='#FFE17B',
                    width=130,
                    height=40,
                    text_color='black',
                    font=('Arial', 16, 'bold'),
                    corner_radius=8,
                    text='Act Pausa',
                    command=nota_activopausa,
                    border_color='purple',
                    border_width=2
                    )

boton33.place(x=680, y=100)

boton34 = CTkButton(frame4,
                    bg_color='black',
                    fg_color='#FFE17B',
                    width=130,
                    height=40,
                    text_color='black',
                    font=('Arial', 16, 'bold'),
                    corner_radius=8,
                    text='Desact Pausa',
                    command=nota_desactivopausa,
                    border_color='purple',
                    border_width=2
                    )

boton34.place(x=680, y=140)

boton35 = CTkButton(frame4,
                    bg_color='black',
                    fg_color='#FFE17B',
                    width=150,
                    height=40,
                    text_color='black',
                    font=('Arial', 16, 'bold'),
                    corner_radius=8,
                    text='Pedidocancelado',
                    command=nota_pedidocancelado,
                    border_color='purple',
                    border_width=2
                    )

boton35.place(x=20, y=140)

boton36 = CTkButton(frame4,
                    bg_color='black',
                    fg_color='#FFE17B',
                    width=170,
                    height=40,
                    text_color='black',
                    font=('Arial', 16, 'bold'),
                    corner_radius=8,
                    text='DeliveryInverso',
                    command=nota_deliveryinverso,
                    border_color='purple',
                    border_width=2
                    )

boton36.place(x=830, y=60)

boton38 = CTkButton(frame4,
                    bg_color='black',
                    fg_color='#FFE17B',
                    width=170,
                    height=40,
                    text_color='black',
                    font=('Arial', 16, 'bold'),
                    corner_radius=8,
                    text='panama-paraguay',
                    command=nota_panamaparaguay,
                    border_color='purple',
                    border_width=2
                    )

boton38.place(x=830, y=100)

boton39 = CTkButton(frame4,
                    bg_color='black',
                    fg_color='#FFE17B',
                    width=170,
                    height=40,
                    text_color='black',
                    font=('Arial', 16, 'bold'),
                    corner_radius=8,
                    text='devolucionBolivia',
                    command=nota_devolucionbolivia,
                    border_color='purple',
                    border_width=2
                    )

boton39.place(x=830, y=140)

boton40 = CTkButton(frame4,
                    bg_color='black',
                    fg_color='#FFE17B',
                    width=170,
                    height=40,
                    text_color='black',
                    font=('Arial', 16, 'bold'),
                    corner_radius=8,
                    text='D2Nicaragua',
                    command=nota_devolucionnicaragua,
                    border_color='purple',
                    border_width=2
                    )

boton40.place(x=830, y=20)

frame5 = CTkFrame(ventana1,
                  bg_color='black',
                  fg_color='black',
                  width=650,
                  height=140,
                  corner_radius=15,
                  border_width=3,
                  border_color='green'
                  )

entrada8 = CTkEntry(frame5,
                    bg_color='black',
                    fg_color='black',
                    width=500,
                    height=40,
                    corner_radius=10,
                    border_width=3,
                    border_color='purple',
                    text_color='#FD8D14',
                    placeholder_text_color='#FFE17B',
                    placeholder_text='correo@pedidosya.com',
                    font=('Arial', 16, 'bold'),
                    justify='center'
                    )
entrada8.place(x=20, y=20)

boton42 = CTkButton(frame5,
                    bg_color='black',
                    fg_color='#FFE17B',
                    width=100,
                    height=40,
                    text_color='black',
                    font=('Arial', 16, 'bold'),
                    corner_radius=8,
                    text='copiar',
                    command=copiar_contenido_entrada8,
                    border_color='purple',
                    border_width=2
                    )

boton42.place(x=530, y=20)

boton43 = CTkButton(frame5,
                    bg_color='black',
                    fg_color='#FFE17B',
                    width=100,
                    height=40,
                    text_color='black',
                    font=('Arial', 16, 'bold'),
                    corner_radius=8,
                    text='reporte',
                    command=reporteic,
                    border_color='purple',
                    border_width=2
                    )

boton43.place(x=20, y=70)

frame6 = CTkFrame(ventana1,
                  bg_color='black',
                  fg_color='black',
                  width=280,
                  height=210,
                  corner_radius=15,
                  border_width=3,
                  border_color='green'
                  )

ancho_ventana = ventana1.winfo_reqwidth()
alto_ventana = ventana1.winfo_reqheight()

label2 = CTkLabel(frame6,
                  width=240,
                  height=30,
                  font=('Arial', 16, 'bold'),
                  text_color='black',
                  bg_color='black',
                  fg_color='#FD8D14',
                  corner_radius=15,
                  justify='center',
                  text='Peru'
                  )

label2.place(x=20, y=10)

label3 = CTkLabel(frame6,
                  width=240,
                  height=30,
                  font=('Arial', 16, 'bold'),
                  text_color='black',
                  bg_color='black',
                  fg_color='#FD8D14',
                  corner_radius=15,
                  justify='center',
                  text='Ecuador'
                  )

label3.place(x=20, y=50)

label4 = CTkLabel(frame6,
                  width=240,
                  height=30,
                  font=('Arial', 16, 'bold'),
                  text_color='black',
                  bg_color='black',
                  fg_color='#FD8D14',
                  corner_radius=15,
                  justify='center',
                  text='Guatemala'
                  )

label4.place(x=20, y=90)

label5 = CTkLabel(frame6,
                  width=240,
                  height=30,
                  font=('Arial', 16, 'bold'),
                  text_color='black',
                  bg_color='black',
                  fg_color='#FD8D14',
                  corner_radius=15,
                  justify='center',
                  text='Costa Rica'
                  )

label5.place(x=20, y=130)

label6 = CTkLabel(frame6,
                  width=240,
                  height=30,
                  font=('Arial', 16, 'bold'),
                  text_color='black',
                  bg_color='black',
                  fg_color='#FD8D14',
                  corner_radius=15,
                  justify='center',
                  text='Honduras'
                  )

label6.place(x=20, y=170)

ventana1.mainloop()
