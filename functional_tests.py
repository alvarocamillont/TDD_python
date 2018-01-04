from selenium import webdriver

browser = webdriver.Firefox()

# João ouviu falar de uma nova aplicação online para lista de tarefas
# Ele decide entra na homepage
browser.get('http://localhost:8000')

# Ele percebe que o título da página e o cabeçalho mencionam lista de tarefas
assert 'To-Do' in browser.title

# Ele é convidado a inserir um item de tarefa

# Ele digita "Comprar penas de pavão" em uma caixa de texto

# Quando ele aperta enter, a pagina é atualizada e agora a pagina lista
# 1: Comprar penas de pavão como um item em uma lista de tarefas

# Ainda há uma caixa de texto e ele acrescenta "Fazer isca de pesca"

#  A página é atualizada novamente e agora mostra dois itens na lista

# João se pergunta se o site irá lembrar dessa lista. Então ele percebe que o site gerou um
# url único para ele - há um texto explicando isso

# Ele acessa a url e verifica que sua lista continua lá

# Satisfeito ele vai durmir

browser.quit()
