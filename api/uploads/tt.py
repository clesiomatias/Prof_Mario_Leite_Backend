
'''
CriaTriangulo.py
-------------------------------------------------------------------------
Traça um triâgulo numa interface gráfica a partir dos lados do triânguklo.
-------------------------------------------------------------------------
'''
import tkinter as tk
import math

def draw_triangle():
    #Define as carcterístucas do triângulo
    a = float(entradaA.get())*3
    b = float(entradaB.get())*3
    c = float(entradaC.get())*3

    #Verifica se pode ser formado um triângulo
    if(a + b > c and a + c > b and b + c > a):
        # Encontrar o maior lado para ser a hipotenusa
        if( a >= b and a >= c):
            hypotenuse = a
            cathetus1 = b
            cathetus2 = c
        elif( b >= a and b >= c):
            hypotenuse = b
            cathetus1 = a
            cathetus2 = c
        else:
            hypotenuse = c
            cathetus1 = a
            cathetus2 = b

        #Cálcula o baricentro do triângulo
        baricenter_x = 50
        baricenter_y = 150

        #Cálcula as coordenadas dos vértices do triângulo
        scale = 10  # Aproximadamente 10 pixels por unidade
        if(a == 3 and b == 4 and c == 5):
            height = 3 * scale
            base = 4 * scale
        else:
            height = cathetus2 * scale
            base = cathetus1 * scale

        A = (baricenter_x - base / 2, baricenter_y + height / 2)
        B = (baricenter_x + base / 2, baricenter_y + height / 2)
        C = (baricenter_x - base / 2, baricenter_y - height / 2)

        # Desenho do triângulo
        canvas.delete("all")
        canvas.create_line(A[0], A[1], B[0], B[1])
        canvas.create_line(B[0], B[1], C[0], C[1])
        canvas.create_line(C[0], C[1], A[0], A[1])
    else:
        canvas.delete("all")
        canvas.create_text(50, 12, text="Não é possível formar um triângulo com esses lados", fill="red")

#Cria a janela
root = tk.Tk()
root.title("Desenho de Triângulo")
#Fim do programa "CriaTriangulo" ----------------------------------------------------------------------------

#Calcula as dimensões da janela em pixels
dpi = root.winfo_fpixels('1i')
width = int(5 * dpi)  # 5 cm
height = int(5 * dpi)   # 5 cm
root.geometry(f"{width}x{height}")

# Criação dos widgets
labelA = tk.Label(root, text="Lado A:")
labelA.pack()
entradaA = tk.Entry(root)
entradaA.pack()

labelB = tk.Label(root, text="Lado B:")
labelB.pack()
entradaB = tk.Entry(root)
entradaB.pack()

labelC = tk.Label(root, text="Lado C:")
labelC.pack()
entradaC = tk.Entry(root)
entradaC.pack()

botaoDesenhar = tk.Button(root, text="Desenhar Triângulo", command=draw_triangle)
botaoDesenhar.pack()

canvas = tk.Canvas(root, width=width, height=height-50)  # Reduz a altura para acomodar os controles acima
canvas.pack()

# Roda o programa
root.mainloop()

