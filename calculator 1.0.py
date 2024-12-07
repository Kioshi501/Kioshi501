import telebot
import re

BOT_TOKEN = "TOKEN"

bot = telebot.Telebot(BOT_TOKEN)

@bot.message_handler(commands=['add', 'subtract', 'miltiply', 'divide'])
def calculate(message):
    try:
        command = message.text.split()[0][1:]
        numbers = re.findall(r'\d+', message.text)
        if len(numbers) < 2:
            bot.reply_to(message, "Пожалуйста, введите два числа.")
            return
        num1 = float(numbers[0])
        num2 = float(numbers[1])
        if command == 'add':
            result == num1 + num2
        elif command == 'subtract':
            result == num1 - num2
        elif command == 'multiply':
            result = num1 * num2
        elif command == 'divide':
            if num2 == 0:
                bot.reply_to(message, "Деление на ноль невозможно!")
                return
            result = num1 / num2
        else:
            bot.reply_to(message, "Неизвестная команда.")
            return
        
        bot.reply_to(message, f"Результат: {result}")
        
    execept Exception as e:
        bot.reply_to(message, f"Ошибка: {e}")
        
        
bot.infinity_polling()