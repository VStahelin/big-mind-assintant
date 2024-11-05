import json
import os
import logging
from datetime import datetime
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from google.generativeai.types import HarmCategory, HarmBlockThreshold

from environs import Env
import google.generativeai as genai
from gtts import gTTS

from shemas.gemini import GeminiImageAnalyzer, GeminiAudioAnalyzer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

env = Env()
env.read_env()
BOT_FATHER_TOKEN = env.str("BOT_FATHER_TOKEN")
genai.configure(api_key=env.str("GEMINI_API_KEY"))


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f"User {update.effective_user.id} started the bot.")

    help_text = (
        "🤖 Olá! Eu sou o *Big Mind Assistent*! Aqui estão algumas coisas legais que eu posso fazer para você:\n\n"  # noqa
        "🎤 */to_audio* <texto> - Transformo seu texto em um áudio incrível!\n"
        "🖼️ *Envie uma imagem* - Vou analisar e descrever tudo que está na foto!\n"
        "🔊 *Envie um áudio* - Transcrevo o que está sendo dito para você.\n\n"
        "💡 Estou aqui para ajudar! Se precisar de mais informações, é só digitar */start* novamente!\n"  # noqa
        "Vamos nos divertir juntos! 🚀"
    )

    await update.message.reply_text(help_text, parse_mode="markdown")


async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Recebendo a imagem. Iniciando o processo de descrição da imagem..."
    )

    photo = update.message.photo[-1]
    file = await photo.get_file()

    image_file = await file.download_as_bytearray()
    os.makedirs("temp", exist_ok=True)
    path = f"temp/image_{datetime.now().date().isoformat()}_{datetime.now().strftime('%H_%M_%S')}.jpg"
    with open(path, "wb") as f:
        f.write(image_file)

    logger.info("Fazendo o upload da imagem para o Gemini...")
    image = genai.upload_file(path)

    logger.info("Extraindo texto da imagem...")
    response = genai.GenerativeModel("gemini-1.5-flash").generate_content(
        [
            "Você é um especialista em descrição de imagens. **Responda em português do Brasil.** "
            "Analise a imagem que estou enviando "
            "e forneça uma descrição detalhada do que você vê. Se a imagem for um print de uma "
            "conversa, descreva o diálogo entre as pessoas, mencionando o que cada um diz e o "
            "contexto da interação. Por favor, forneça informações sobre os elementos visuais, "
            "como as cores, os objetos e as expressões faciais, se houver.",
            image,
        ],
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json", response_schema=GeminiImageAnalyzer
        ),
        safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        },
    )

    description = json.loads(response.text)

    logger.info(f"Dados extraídos: {response.text}")
    await update.message.reply_text("Sua descrição da imagem")
    await update.message.reply_text(description["description"])


async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Recebendo áudio. Iniciando o processo de transcrição do áudio..."
    )

    # Baixando o áudio enviado
    audio = await update.message.voice.get_file()
    audio_file = await audio.download_as_bytearray()

    os.makedirs("temp", exist_ok=True)
    audio_path = f"temp/audio_{datetime.now().date().isoformat()}_{datetime.now().strftime('%H_%M_%S')}.ogg"
    with open(audio_path, "wb") as f:
        f.write(audio_file)

    try:
        _file = genai.upload_file(audio_path)

        response = genai.GenerativeModel("gemini-1.5-flash").generate_content(
            [
                {
                    "text": "Transcreva este áudio para português do Brasil, garantindo que o "
                    "texto resultante seja claro e fluido, como se fosse um texto corrido "
                    "para leitura humana."
                },
                {"text": "data:audio/ogg;base64"},
                _file,
            ],
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                response_schema=GeminiAudioAnalyzer,
            ),
            safety_settings={
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            },
        )

        transcription = json.loads(response.text)["transcription"]

        logger.info(f"Resultado da transcrição: {transcription}")
        await update.message.reply_text("Transcrição do áudio:")
        await update.message.reply_text(transcription)

    except Exception as e:
        logger.error(f"Erro na transcrição: {str(e)}", exc_info=True)
        await update.message.reply_text(
            "Desculpe, ocorreu um erro durante a transcrição."
        )


async def generate_audio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = " ".join(context.args)
    if not text:
        await update.message.reply_text(
            "Por favor, forneça o texto após o comando /generate_audio."
        )
        return

    await update.message.reply_text("Gerando áudio...")

    tts = gTTS(text, lang="pt")

    os.makedirs("temp", exist_ok=True)
    audio_path = f"temp/audio_{datetime.now().date().isoformat()}_{datetime.now().strftime('%H_%M_%S')}.mp3"
    tts.save(audio_path)

    with open(audio_path, "rb") as f:
        await update.message.reply_voice(voice=f, caption="Aqui está o áudio gerado!")


if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_FATHER_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("to_audio", generate_audio))
    app.add_handler(MessageHandler(filters.PHOTO, handle_image))
    app.add_handler(MessageHandler(filters.VOICE, handle_audio))

    logger.info("Bot is running...")
    app.run_polling()
