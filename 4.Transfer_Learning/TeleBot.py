import telebot

import tensorflow as tf
import numpy as np
import cv2


bot = telebot.TeleBot("7024779071:AAGPaH5b0-NQi2XJfUm3HNkgKib9sDMBOdM", parse_mode=None)

person = ['Akhund', 'Human']

model = tf.keras.models.load_model('/content/drive/MyDrive/PyLearn 7 Course/54.TransferLearning/Akhund_detector_model.h5')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hey " + message.from_user.first_name + " 👋"+"\n"+"Wanna know who you can trust? Just send ma a photo 🧐")


@bot.message_handler(content_types = ['photo'])
def receive_photo(message):
    bot.send_message(message.chat.id, 'Please Wait a moment ... I`m watching 👀 👾')

    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)

    with open("person.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)

    img = cv2.imread("person.jpg")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img ,(224,224))
    img = img / 255
    img = img.reshape(1,224,224,3)
    result = np.argmax(model.predict(img))

    print(result)
    print(person[result])

    if result == 0:
      bot.send_message(message.chat.id, f'Not from us 👳🏻‍♂️👎')
    else:
      bot.send_message(message.chat.id, f'One of us 👍🤝')


    
bot.infinity_polling()