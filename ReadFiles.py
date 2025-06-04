#Função para expressão regular
import re

#variávais 
vLinha = 0

#Escrever arquivo
newFile      = open("fileEmail.txt", "w")
newFileError = open("fileEmailFail.txt", "w")


#Criar função que grava no arquivo novo, validando o email via regex
def validate(email):
    pattern = r'^[\w\.-]+@[\w-]+\.[\w-]+(\.[\w-]+){0,2}$'
    if re.match(pattern, email):
        return True
    else:
        return False
       
#Ler Arquivo
with open('email.txt') as arquivo:
    for line in arquivo:
        vLinha+=1

        newLine = re.sub("[,<>]", "", line)
        arrayLine = newLine.split(" ")
        #descartar a palavra que não contiver @
        if len(arrayLine) > 1:
            for i in arrayLine:                
                if (i.find("@") >= 1):
                    if validate(i):
                        newFile.write(i)
                    else:
                        newFileError.write(i)
        else:
            if validate(newLine):
                newFile.write(newLine)
            else:
                newFileError.write(newLine)

newFile.close()       
newFileError.close()       


