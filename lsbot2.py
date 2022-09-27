import random
import datetime
import sqlite3
import os

#greet = ['В7 ха1', 'Всем привет, остальным соболезную', 'Здоровье павшим', 'Ну чтож... приступим', 'Удачи неудачникам']
greet = ['В7 ха1', 'Hi eveyone, except for everyone else', 'Healtgh to dead', 'So what... les go', 'good luck to losers']
#medi = ['хороший выбор', 'ты не пожалеешь', 'как пожелаешь', 'Ваша воля для меня закон']
medi = ['good choice', 'you wont regret', 'as you wish', 'your wish is an order for me']
osas = ['\photo\sasha1.jpg', '\photo\sasha2.jpg', '\photo\sasha3.jpg', '\photo\sasha4.jpg', 
'\photo\sasha5.jpg', '\photo\sasha6.jpg', '\photo\sasha7.jpg', '\photo\sasha8.jpg']
k = True

from aiogram import Bot, Dispatcher, executor, types

TOKEN = '2069498211:AAGnb9aaViXTlfiApOlR9f7-K0oz-esjtNI'

bot = Bot(token = TOKEN)
dp = Dispatcher(bot)

###################################       connecting to sql database
con = sqlite3.connect('lsbot_db') #
c = con.cursor()                  #
###################################

is_gmail = False                    # It's used to distinguish between normal mesages and ones containing gmail of a user



###############################################################################
#                           strart of main code
###############################################################################


@dp.message_handler(commands = ['start'])
async def privet(message: types.Message):
    await message.answer(greet[random.randint(0,len(greet)-1)])
    await message.answer('Whats next?')
    await message.answer('"Hint:(/help)"')
    print(message.from_user.username, message.from_user.first_name, message.from_user.last_name, message.from_user.id)
    
    c.execute('select u.user_ID  from users u where u.tg_ID = "'+str(message.from_user.id)+'"')
            
    a = c.fetchone()
    
    
    if a == None:                                   #including user in database if he is not in it
        c.execute("INSERT INTO users (name, tg_ID) VALUES ('"+str(message.from_user.first_name)+str(message.from_user.last_name)+"','"+str(message.from_user.id)+"');")
        con.commit()
    
@dp.message_handler(commands = ['help'])
async def pomosh(message: types.Message):
    await message.reply('"/LS"-LowsSkills media')
    await message.answer('"/my_gmail"-input your gmail')
    await message.answer('"/join_LS"-send an application to join LS')
    await message.answer('If you encounter an error please contact @ch1r1nk0v')
    
@dp.message_handler(commands = ['ls'])
async def sait(message: types.Message):

    button_1 = types.InlineKeyboardButton(text='official site', url = "https://lowsskills.wixsite.com/lowsskills")
    button_2 = types.InlineKeyboardButton(text='youtube', url = "https://www.youtube.com/channel/UCJ7gKteshw7od9sk8fEdPcQ")
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(button_1)
    keyboard.add(button_2)
    await message.reply(medi[random.randint(0,len(medi))],reply_markup = keyboard)
    
@dp.message_handler(commands = ['my_gmail'])
async def gmail_activator(message: types.Message):
    global is_gmail
    is_gmail = True

    await message.answer('Input your gmail')



@dp.message_handler(commands = ['join_LS'])
async def send_invite(message: types.Message):
    try:
        print('1')
        c.execute('select u.user_gmail  from users u where u.tg_ID = "'+str(message.from_user.id)+'"')  
        a = c.fetchone()
        if a == None:
            await message.answer('We dont have your gmail yet, you can use "/my_gmail" to provide us with it')
            pass
        else:
            print('2')
            os.system("ls_emailbot_1.py "+a[0]+" "+str(message.from_user.id))
            await message.answer('Your request was sent, please check your inbox for a reply gmail. If you didnt get a reply gmail check the spelling of the gmail you inputed')
    except Exception:
        await message.answer('An error ocured')



@dp.message_handler(commands = ['саша'])
async def sasha(message: types.Message):
    photo = open(osas[random.randint(0,7)], 'rb')
    await bot.send_photo(chat_id=message.chat.id, photo=photo)



@dp.message_handler()
async def input_gmail(message: types.Message):
    
    global is_gmail

    if is_gmail == True:
        is_gmail = False
        try:
            if message.text[-10: -1] + message.text[-1] == '@gmail.com' and len(message.text) > 10:
                c.execute("UPDATE users SET user_gmail='"+str(message.text)+"' WHERE tg_ID='"+str(message.from_user.id)+"';")
                con.commit()
                await message.answer('Yor gmail, "'+message.text+'", was accepted')  
            else:
                await message.answer('Gmail declined. Please make sure that you entered a valid gmail')
        except Exception:
            await message.answer('An error ocured while collecting your email')




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates = True)
