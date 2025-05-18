import tkinter as tk
from tkinter import messagebox

# Base de datos de alimentos.
menu = {
    "pollo": {"proteinas": 27, "grasas": 3, "carbohidratos": 0},
    "huevo": {"proteinas": 13, "grasas": 11, "carbohidratos": 1},
    "atun": {"proteinas": 26, "grasas": 1, "carbohidratos": 0},
    "ternera": {"proteinas": 25, "grasas": 15, "carbohidratos": 0},
    "lentejas cocidas": {"proteinas": 9, "grasas": 0.4, "carbohidratos": 20},
    "arroz blanco cocido": {"proteinas": 2.7, "grasas": 0.3, "carbohidratos": 28},
    "quinoa cocida": {"proteinas": 4.4, "grasas": 1.9, "carbohidratos": 21},
    "garbanzos cocidos": {"proteinas": 8.9, "grasas": 2.6, "carbohidratos": 27},
    "pavo": {"proteinas": 29, "grasas": 1, "carbohidratos": 0},
    "salmón": {"proteinas": 20, "grasas": 13, "carbohidratos": 0},
    "bacalao": {"proteinas": 18, "grasas": 0.7, "carbohidratos": 0},
    "almendras": {"proteinas": 21, "grasas": 49, "carbohidratos": 22},
    "avena": {"proteinas": 13.5, "grasas": 7, "carbohidratos": 60},
    "pan integral": {"proteinas": 9, "grasas": 2.5, "carbohidratos": 42},
    "leche entera": {"proteinas": 3.4, "grasas": 3.7, "carbohidratos": 5},
    "yogur natural": {"proteinas": 4, "grasas": 3, "carbohidratos": 4},
}
# Funciones
#--Calculamos los macronutrientes de cada alimento selecccionado.
def calcular_macros(alimento, cantidad):
    datos = menu.get(alimento)                      #-Seleccionamos el alimento en concreto.
    if not datos:
        return None
    return {
        "proteinas": datos["proteinas"] * cantidad / 100,           #-Devolvemos los datos según la cantidad elegida.
        "grasas": datos["grasas"] * cantidad / 100,
        "carbohidratos": datos["carbohidratos"] * cantidad / 100
    }
#--Buscamos el equivalente de nuestro alimento si lo hay.
def buscar_equivalentes(calculo, tolerancia=2.0):
    equivalentes = []                   
    for nombre, datos in menu.items():          #-Pasamos por cada uno de los alimentos de nuestra lista "menu" y guardamos sus macronutrientrres.
        proteinas = datos["proteinas"]
        grasas = datos["grasas"]
        carbos = datos["carbohidratos"]
        for cantidad in range(50, 201, 10):         #-Pasamos desde los 50g a los 200g con paso 10g para calcular una cantidad equivalente.
            prot_eq = proteinas * cantidad / 100
            gras_eq = grasas * cantidad / 100
            carb_eq = carbos * cantidad / 100
            if (abs(prot_eq - calculo["proteinas"]) < tolerancia and        #-Si las variables de equivalencia restadas a nuestro cálculo son inferiores a nuestra tolerancia
                abs(gras_eq - calculo["grasas"]) < tolerancia and           #-añadiremos ese alimento/cantidad a la lista equivalentes.
                abs(carb_eq - calculo["carbohidratos"]) < tolerancia):
                equivalentes.append((nombre, cantidad))
                break
    return equivalentes
#--Función para convertir el alimento y sacar sus equivalentes.
def convertir(event=None):                  #-Creamos event para que funcione con key <return>
    alimento = var_alimento.get()               #-Alimento será los que el StringVar del OptionMenu señale en el momento
    try:
        cantidad = float(entry_cantidad.get())      #-Creamos un try - except para la cantidad en gramos.
    except ValueError:
        messagebox.showerror("Error", "Introduce una cantidad válida en gramos.")   #-Messagebox,sale una ventanita señalando el error.
        return
    
    macros = calcular_macros(alimento, cantidad)            #-Variable que invoca a la función para calcular nuestros nutrientes.
    if not macros:
        messagebox.showerror("Error", f"El alimento '{alimento}' no está en el menú.")  #-Opción que queda anulada al tener un OptionMenu
        return
    
    resultados = buscar_equivalentes(macros)        #-Variable que invoca a la función que almacena la lista con los alimentos equivalentes.
    text_resultado.delete(1.0, tk.END)                  #-Borramos el texto de la caja de texto.
    if resultados:
        text_resultado.insert(tk.END, f"Equivalentes a {cantidad}g de {alimento}:\n\n")     #-Si disponemos de equivalencias para nuestro alimento se imprime en nuestro text_resultado.
        for nombre, cantidad_eq in resultados:
            text_resultado.insert(tk.END, f"- {cantidad_eq}g de {nombre}\n")
    else:
        text_resultado.insert(tk.END, "No se encontraron equivalentes con esta tolerancia.")    #Si no hay resultado disponible, se imprime mensaje.

#--Interfaz gráfica
#-Root
ventana = tk.Tk()
ventana.title("Conversor de Alimentos")
ventana.geometry("400x400")
#-Label(alimento) + OptionMenu(StringVar)
tk.Label(ventana, text="Selecciona un alimento:").pack()
var_alimento = tk.StringVar(ventana)
var_alimento.set(list(menu.keys())[0])          #-Valor por defecto, en este caso: "pollo"
menu_desplegable = tk.OptionMenu(ventana, var_alimento, *menu.keys())       #-Situamos en ventana, con el texxto del StringVar de ver_alimento y los keys de la lista -menu-
menu_desplegable.pack()
#-Label(Cantidad) + Entry "caja de texto"
tk.Label(ventana, text="Cantidad (g):").pack()
entry_cantidad = tk.Entry(ventana)
entry_cantidad.pack()
#-Botón para buscar los equivalentes.
tk.Button(ventana, text="Buscar Equivalentes", command=convertir).pack(pady=10)
#-Caja de texto donde poner todas las equivalencias existentes.
text_resultado = tk.Text(ventana, height=15, width=45)
text_resultado.pack()
#-Vinculamos la tecla <return> al botón Buscar Equivalentes
ventana.bind("<Return>", convertir)
#-Mostramos ventana.
ventana.mainloop()