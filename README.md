<p align="center">
  <img src="assets/logo.jpeg" alt="Big Mind Assistant Logo" width="200"> <br>
  <h1 align="center"><b>Big Mind Assistant 🤖</b></h1>
</p>

Um assistente de Telegram super inteligente, alimentado pelo Google Gemini! 🚀

Este bot utiliza o poder do Gemini para oferecer uma série de funcionalidades incríveis, diretamente no seu Telegram:

* **Transcrição de Áudio 🎤:** Envie uma mensagem de voz e o Big Mind Assistant transcreve para texto, facilitando a leitura e o compartilhamento.
* **Análise de Imagem 🖼️:** Envie uma imagem e receba uma descrição detalhada do conteúdo, incluindo objetos, cores e até mesmo o contexto de conversas em prints de tela!
* **Síntese de Texto para Fala 🗣️:** Transforme qualquer texto em áudio com o comando `/to_audio`. Perfeito para ouvir notícias, artigos ou qualquer texto em qualquer lugar.


## Começando 🚀

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/VStahelin/big-mind-assintant
   cd big-mind-assintant
   ```

2. **Instale as dependências (usando Poetry):**

   ```bash
   poetry install
   ```

3. **Configure as variáveis de ambiente:**

   * Crie um arquivo `.env` na raiz do projeto, copiando o conteúdo de `example.env`.
   * Preencha as seguintes variáveis com suas credenciais:
      * `BOT_FATHER_TOKEN`:  Seu token do BotFather (Telegram).
      * `GEMINI_API_KEY`: Sua chave de API do Google Gemini.

4. **Execute o bot (usando Poetry):**

   ```bash
   poetry run python main.py
   ```

## Comandos 🤖

* `/start`: Inicia o bot e exibe a lista de comandos.
* `/to_audio <texto>`: Converte o texto fornecido em áudio.
* *Enviar uma imagem*: O bot analisa a imagem e fornece uma descrição detalhada.
* *Enviar uma mensagem de voz*: O bot transcreve o áudio para texto.


## Estrutura do Projeto 📂

* `.gitignore`: Arquivo para ignorar arquivos e diretórios
* `README.md`: Este arquivo.
* `example.env`: Exemplo de arquivo de variáveis de ambiente.
* `main.py`: Arquivo principal do bot.
* `poetry.lock`: Arquivo de lock do Poetry.
* `pyproject.toml`: Arquivo de configuração do Poetry.
* `shemas/gemini.py`: Esquemas de resposta do Gemini.


## Formatação de Código ✨

Este projeto utiliza `black` e `ruff` para garantir um código limpo e consistente.  Após fazer alterações no código, execute:

```bash
poetry run black .
poetry run ruff check .
```


## Contribuindo 🤝

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.
