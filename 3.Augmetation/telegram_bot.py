import telebot

import tensorflow as tf
import numpy as np
import cv2


bot = telebot.TeleBot("6340701803:AAHo-n4XQggdWgFwCq9W-UvkzqJ4nmUHY5U", parse_mode=None)

flowers_name = ['bluebell', 'buttercup', 'coltsfoot', 'cowslip', 'crocus', 'daffodil','daisy', 'dandelion', 'fritillary', 'iris', 'lilyvalley', 'pansy', 'snowdrop', 'sunflower', 'tigerlily', 'tulip', 'windflower']
model = tf.keras.models.load_model('/content/drive/MyDrive/PyLearn 7 Course/53.Augmentation/17flower_model.h5')


result_keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2)
buttom1 = telebot.types.KeyboardButton("True")
buttom2 = telebot.types.KeyboardButton("False")
result_keyboard.add(buttom1, buttom2)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello " + message.from_user.first_name + " 👋"+"\n"+"Wellcome to 17flowers Detector bot ✨")
    bot.send_message(message.chat.id, "Send a photo from one of the 17 flower to detect it 🌸🌻🌹🌺🌼🌷"+"\n\n"+"If you don`t know 17flowers send /17flowers_list to I send you their names 📃")


@bot.message_handler(commands=['17flowers_list'])
def send_welcome(message):
    bot.reply_to(message, """bluebell 🌸\n buttercup 🌻\n coltsfoot 🌹\n cowslip 🌷\n crocus 🌺\n daffodil 🌼\n daisy 🌷\n dandelion 🌸\n fritillary 🌻\n iris🌹\n lilyvalley 🌺\n pansy 🌼\n snowdrop 🌷\n sunflower 🌻\n tigerlily 🌸\n tulip 🌹\n windflower 🌺""")


def feedback(message):
      if message.text == "True":
        bot.send_message(message.chat.id, "Hooray! 💪🥳")
      elif message.text == "False":
        bot.send_message(message.chat.id, "OOh! I`m sory, I hope I predict the next ones correctly 🙏😓")


@bot.message_handler(content_types = ['photo'])
def receive_photo(message):
    bot.send_message(message.chat.id, 'Please Wait a minute ... I`m predicting your flower 👾')

    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)

    with open("flower.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)

    img = cv2.imread("flower.jpg")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img ,(224,224))
    img = img / 255
    img = img.reshape(1,224,224,3)
    result = np.argmax(model.predict(img))
    print(result)
    print(flowers_name[result])

    bot.send_message(message.chat.id,f'My prediction is that your flower is a {flowers_name[result]} 🤖')
    userMessage = bot.send_message(message.chat.id, "Isn`t it?", reply_markup = result_keyboard)
    bot.register_next_step_handler(userMessage, feedback)

    
bot.infinity_polling()