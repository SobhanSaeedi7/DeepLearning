import telebot

import tensorflow as tf
import numpy as np
from collections import Counter 

import pydub

def get_prober_name():
    return "C://ffmpeg/bin/ffprobe.exe"


pydub.AudioSegment.converter = "C://ffmpeg/bin/ffmpeg.exe"                  
pydub.utils.get_prober_name = get_prober_name

bot = telebot.TeleBot("7224215190:AAHiyNSG6dZYQsez-kwWCQ1X5DpOYWWHymE", parse_mode=None)


friends = ['Abdollah', 'Azera', 'Davood', 'Javad', 'Khadijeh', 'Kiana', 'Maryam', 'Matin', 'Melika', 'Mohammad Parvari', 'Mohammad Nemati', 'Mona', 'Nahid', 'Nima', 'Omid', 'Parisa', 'Parsa', 'Sajedeh', 'Shima', 'Sobhan', 'Tara']
singer_names = ['Faramarz Aslani', 'Mohsen Chavoshi', 'Hayedeh', 'Moein', 'Shadmehr']


keyboard = telebot.types.ReplyKeyboardMarkup()
buttom1 = telebot.types.KeyboardButton("/friend")
buttom2 = telebot.types.KeyboardButton("/singer")
keyboard.add(buttom1, buttom2)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hey " + message.from_user.first_name + " 👋"+"\n"+"Choose one of the options below to start predicting 🧐")
    bot.send_message(message.chat.id, "More details with /help", reply_markup = keyboard)


@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, 'If your one of my PyLearn friends, choose /friend send me your voice to I recognize you.' + '\n\n' + 'Elif choose /singer and send me a music from selected singers (/singers_list) to I recognize the singer.')


@bot.message_handler(commands=['singers_list'])
def singers(message):
    bot.reply_to(message, """Hayedeh \n Faramarz Aslani \n Moein \n Mohsen Chavoshi \n and Shadmehr""")


@bot.message_handler(commands=['friend'])
def friend_mode(message):
    global bot_mode
    bot_mode = 'friend'
    bot.reply_to(message, 'OK, send me your voice please : ')


@bot.message_handler(commands=['singer'])
def singer_mode(message):
    global bot_mode
    bot_mode = 'singer'
    bot.reply_to(message, 'OK, send me a music please : ')


@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    bot.reply_to(message, 'Listening...')
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open('received_file.wav', 'wb') as received_file:
        received_file.write(downloaded_file)
    audio = pydub.AudioSegment.from_file('received_file.wav')

    audio = audio.set_sample_width(2)  # convert to 16-bit (2 bytes per sample) to avoid tensorflow error
    audio = audio.set_frame_rate(48000)
    audio = audio.set_channels(1)  # convert stereo audio to mono audio to avoid tensorflow error

    chunks = pydub.silence.split_on_silence(audio, min_silence_len=900, silence_thresh=-45)
    result = sum(chunks)
    # result.export('test.wav', format="wav")

    chunks = pydub.utils.make_chunks(result, 1000)


    if bot_mode == 'friend':
        model = tf.keras.models.load_model('weights/audio_classification.h5')
        bot.send_message(message.chat.id, 'You got a great voice my friend!')

        predict_list = []
        for chunk in chunks:
            if len(chunk) >= 1000:
                print('o')
                chunk.export('chunk.wav', format="wav")
                x = tf.io.read_file('chunk.wav')
                x, sample_rate = tf.audio.decode_wav(x, desired_channels=1, desired_samples=48000,)
                x = x[tf.newaxis, ...]

                prediction = model.predict(x)
                predict_list.append(np.argmax(prediction))


        index, time = Counter(predict_list).most_common(1)[0]
        friend = friends[index]
        bot.send_message(message.chat.id, f'It`s you, {friend}')

        

    elif bot_mode == 'singer':
        model = tf.keras.models.load_model('weights/singers_audio_classification.h5')
        bot.send_message(message.chat.id, 'I really like this music!')

        predict_list = []
        for chunk in chunks:
            if len(chunk) >= 1000:
                print('o')
                chunk.export('chunk.wav', format="wav")
                x = tf.io.read_file('chunk.wav')
                x, sample_rate = tf.audio.decode_wav(x, desired_channels=1, desired_samples=48000,)
                x = x[tf.newaxis, ...]

                prediction = model.predict(x)
                predict_list.append(np.argmax(prediction))


        index, time = Counter(predict_list).most_common(1)[0]
        singer = singer_names[index]
        bot.send_message(message.chat.id, f'It`s from, {singer}')

    

    


bot.infinity_polling()