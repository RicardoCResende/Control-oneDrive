chave = 1234

def cripto(chave):
    encriptado = ''
    if chave == 1234:
        letras = ['f', 'r', 'y', 'q', 'i', 'a', 'z', 'm', 't', 'l']
    elif chave == 4321:
        letras = ['r', 'g', 'w', 'j', 'a', 'k', 'v', 'i', 'q', 'p']
    elif chave == 2413:
        letras = ['t', 'e', 'x', 'v', 'b', 'm', 's', 'o', 'l', 'u']
        
    original = open('test.txt').readlines()

    formatado = []
    for c in original:
        formatado.append(c.strip('\n'))
    
    for item in formatado[0]:
        if item == '.':
            encriptado += '.'
        else:
            encriptado+= letras[int(item)]

    print(encriptado)
    a = open('encriptado.txt', 'w')
    a.writelines(encriptado)
    a.close

    
def decripto():
    letras = {'f': '0', 'r': '1', 'y': '2', 'q': '3', 'i': '4', 'a': '5', 'z': '6', 'm': '7', 't': '8', 'l': '9'}

    valor = open('encriptado.txt').readlines()

    decriptado = ''
    for c in valor[0]:
        if c == '.':
            decriptado += '.'
        else:
            decriptado += letras[c]

    print(decriptado)

    

        

cripto()