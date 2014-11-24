
### Algoritmo para Qualificação das Saídas de Buscas em Gerenciadores de Repositórios de Distribuições Linux 

<center>
<br><br><br><br><br><br><br>

Luiz Fernando Gomes de Oliveira
<br>
26 de Novembro de 2014
</center>

#Presenter Notes

- Não esqueça de dar bom dia!

-------

# Problema atual

- Dificuldade em localização dos pacotes desejados.
- Sem opções de ordenação.
- Sem clareza da forma como os pacotes foram ordenados.
- Sem suporte para __string matching__.

#Presenter Notes

- Importante caracterizar a falta de informações quanto à ordenação.
- A deficiência da ferramenta de funcionar sozinha, necessitando do auxilio de outras ferramentas.

-----

# Contextualização

----

<h2>
<center>
Gerenciadores de pacotes <br>
X <br>
Gerenciadores de repositórios
</center>
</h2>


#Presenter Notes

- APT -> dpkg
- YUM -> RPM

### DPKG

> Instala pacotes

### APT

> Gerencia a lista de repositórios e previne dependências

----

# Code Sample

Landslide supports code snippets

    !python
    def log(self, message, level='notice'):
        if self.logger and not callable(self.logger):
            raise ValueError(u"Invalid logger set, must be a callable")

        if self.verbose and self.logger:
            self.logger(message, level)