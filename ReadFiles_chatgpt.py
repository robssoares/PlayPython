import re

# Regex para detectar e-mails válidos
email_regex = re.compile(
    r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
)

# Conjuntos para evitar e-mails duplicados
emails_validos = set()
emails_invalidos = set()

# Lê o arquivo EMAIL.TXT
with open("EMAIL.TXT") as arquivo:
    for linha in arquivo:
        # Divide a linha por vírgulas
        partes = linha.split(",")
        for item in partes:
            item = item.strip()
            # Verifica se tem algo que parece um e-mail
            encontrados = re.findall(email_regex, item)
            if encontrados:
                for email in encontrados:
                    # Verifica se o e-mail completo está correto
                    if re.fullmatch(email_regex, email):
                        emails_validos.add(email)
                    else:
                        emails_invalidos.add(email)
            elif "@" in item:
                # Se contém "@" mas não passa na regex, considera inválido
                emails_invalidos.add(item)

# Salva os e-mails válidos
with open("EMAILVALIDO.TXT", "w", encoding="utf-8") as valid_file:
    for email in sorted(emails_validos):
        valid_file.write(email + "\n")

# Salva os e-mails inválidos
with open("EMAILINVALIDO.TXT", "w", encoding="utf-8") as invalid_file:
    for email in sorted(emails_invalidos):
        invalid_file.write(email + "\n")

print("Processamento concluído. Arquivos EMAILVALIDO.TXT e EMAILINVALIDO.TXT foram gerados.")
