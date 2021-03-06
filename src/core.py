from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from conf.settings import TELEGRAM_TOKEN
from dicom.files import load_scan_from_dir
from dicom.processing import process_and_save
from get_kaggle_rsna_data import get_sample_info_by
import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def _send_photos(bot, update, fig_paths):
    for fig in fig_paths:
        bot.send_photo(update.message.chat_id, photo=open(fig, 'rb'))


def start(bot, update):
    response_message = '''
    Olá
    O que você deseja fazer?
    /exemplos para ver a lista de arquivos disponíveis
    /processe <exemplo> para ver o processamento deste arquivo
    OU envie um arquivo dicom
    /help para ver essas instruções novamente.
    '''.replace("  ", "")
    bot.send_message(
        chat_id=update.message.chat_id,
        text=response_message
    )


def exemplos(bot, update):
    example_path = 'examples/'
    scans = []

    for scan in load_scan_from_dir(example_path):
        scans.append("/processe {}\n".format(scan))

    bot.send_message(
        chat_id=update.message.chat_id,
        text="".join(scans)
    )


def processe(bot, update, args):
    try:
        for _filename in args:
            fig_paths = process_and_save(_filename)
            bot.send_message(
                chat_id=update.message.chat_id,
                text="Resultados para {}:".format(_filename)
            )
            _send_photos(bot, update, fig_paths)

            try:
                # remove 'examples/' from examples/ID_647a6fadd.dcm:
                # and get id 'ID_647a6fadd' from /ID_647a6fadd.dcm:
                extra_info = get_sample_info_by(_filename[9:].split('.')[0])

                if len(extra_info) > 0:
                    extra_info_message = "\n".join(
                        ["{}: {}".format(sample[0], sample[1]) for sample in extra_info])

                    bot.send_message(
                        chat_id=update.message.chat_id,
                        text=extra_info_message
                    )
            except:
                pass

        if not args:
            bot.send_message(
                chat_id=update.message.chat_id,
                text="/processe <nome_arquivo.dcm>"
            )

    except:
        bot.send_message(
            chat_id=update.message.chat_id,
            text="Opss..."
        )


def dicom(bot, update):
    file = bot.getFile(update.message.document.file_id)
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Processando arquivo..."
    )
    try:
        dcm = file.download('{}.dcm'.format(file.file_id))

        fig_paths = process_and_save(dcm)
        bot.send_message(
            chat_id=update.message.chat_id,
            text="Resultados para {}:".format(dcm)
        )
        _send_photos(bot, update, fig_paths)
    except:
        bot.send_message(
            chat_id=update.message.chat_id,
            text="Ops, tivemos um problema com o arquivo enviado."
        )


def text(bot, update):
    response_message = 'Parece que você esta com dúvidas, se sim, clique em /help'
    bot.send_message(
        chat_id=update.message.chat_id,
        text=response_message
    )


def unknown(bot, update):
    response_message = "Comando não encontrado!"
    bot.send_message(
        chat_id=update.message.chat_id,
        text=response_message
    )


def main():
    updater = Updater(token=TELEGRAM_TOKEN)

    dispatcher = updater.dispatcher

    unknown_handler = MessageHandler(Filters.command, unknown)
    dicom_handler = MessageHandler(Filters.document, dicom)
    text_handler = MessageHandler(Filters.text, text)

    dispatcher.add_handler(
        CommandHandler('start', start)
    )
    dispatcher.add_handler(
        CommandHandler('exemplos', exemplos)
    )
    dispatcher.add_handler(
        CommandHandler('processe', processe, pass_args=True)
    )
    dispatcher.add_handler(
        CommandHandler('help', start)
    )

    dispatcher.add_handler(unknown_handler)
    dispatcher.add_handler(dicom_handler)
    dispatcher.add_handler(text_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    print("press CTRL + C to cancel.")
    main()
