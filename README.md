# Sangue na Cabeça

![GitHub repo size](https://img.shields.io/github/repo-size/herlanassis/sanguenacabeca)
![GitHub contributors](https://img.shields.io/github/contributors/herlanassis/sanguenacabeca)
![GitHub stars](https://img.shields.io/github/stars/herlanassis/sanguenacabeca?style=social)
![GitHub forks](https://img.shields.io/github/forks/herlanassis/sanguenacabeca?style=social)
![GitHub issues](https://img.shields.io/github/issues-raw/herlanassis/sanguenacabeca?style=social)
![Twitter Follow](https://img.shields.io/twitter/follow/herlanassis?style=social)

Sangue na Cabeça é uma `ferramenta` que permite `análise` de arquivos DICOM com suspeira de `hemorragia intracraniana`. Ela pode ser utilizada via bot, pelo link [@SangueNaCabeca](https://telegram.me/SangueNaCabeca_Bot).

Você também pode utilizar um `executável` para executar no seu terminal.

Este projeto foi desenvolvido como requisito para conclusão da turma de Inteligência Computacional do Programa de Pós Graduação da UERN/UFERSA no ano de 2020.

A seguir, irei fornecer instruções executar o projeto na sua máquina.

## Pré-requisitos

Antes de começar, verifique se você atendeu aos seguintes requisitos:

- Você instalou o [conda](https://phoenixnap.com/kb/how-to-install-anaconda-ubuntu-18-04-or-20-04)?
- Você criou um [bot no telegram](https://core.telegram.org/bots)?
- (OPCIONAL) Você instalou a versão mais recente do `docker`?
- (OPCIONAL) Você instalou a versão mais recente do `docker-compose`?

## Instalando SangueNaCabeca

1. Clone o projeto:

```shell
git clone https://github.com/HerlanAssis/sanguenacabeca;
cd sanguenacabeca;
```

2. Siga as instruções do arquivo src/main.py para executar no seu terminal.

3. Ou, acesse o link [SeuBot](https://core.telegram.org/bots) e configure seu bot.

4. Para adicionar seu bot, crie um arquivo `.env` no diretório principal do projeto adicione a variável TELEGRAM_TOKEN=<seu_token>.

5. Depois execute no diretório principal:

```
docker-compose up -d --build
```

## Utilizando SangueNaCabeca

Para usar o SangueNaCabeca, siga estes passos:

* crie um ambiente virtual com o conda, ative ele e execute o scrypt `main.py` para ser as instruções:

```shell
conda install --file requirements.txt --yes
```

```
python src/main.py --path caminho_da_pasta/
```

OU

```
python src/main.py --files caminho_do_arquivo1 caminho_do_arquivo2
```

## TODO

As próximas ações para o SangueNaCabeca são:

- [x] ~~Escrever README~~
- [ ] Documentar
- [X] ~~Adicionar mais exemplos no bot~~
- [ ] Melhorar a apresentação do bot explicando seu algoritmo
- [ ] Referênciar artigo escrito
- [ ] Referências leitura base
- [ ] Escrever Testes

## Contribuindo para SangueNaCabeca

Para contribuir com SangueNaCabeca, siga estes passos:

1. Fork esse repositório.
2. Crie uma branch: `git checkout -b <branch_name>`.
3. Faça suas mudanças e comite para: `git commit -m '<commit_message>'`
4. Push para a branch de origem: `git push origin SangueNaCabeca/<location>`
5. crie um pull request.

Como alternativa, consulte a documentação do GitHub em [criando uma pull request](https://help.github.com/pt/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).

## Contribuidores

Agradeço às seguintes pessoas que contribuíram para este projeto:

- [@herlanassis](https://github.com/herlanassis)
- [José Ricardo Soriano](mailto:jrsoriano.sistemas@gmail.com)

## Contato

Se você quiser entrar em contato comigo, entre em contato com herlanassis@gmail.com.

<!-- ## License

Se você não tiver certeza de qual licença aberta usar, consulte https://choosealicense.com

Este projeto usa a seguinte licença: [<license_name>](link). -->
