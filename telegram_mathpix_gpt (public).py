import base64
import logging
import requests
import openai
import telegram
from telegram import Update, InputMediaPhoto
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
import json
import time
import random

# Set up your credentials
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

TELEGRAM_TOKEN = config["telegram_token"]
MATHPIX_APP_ID = config["mathpix_app_id"]
MATHPIX_APP_KEY = config["mathpix_app_key"]
OPENAI_API_KEY = config["openai_api_key"]

# Initialize OpenAI API
openai.api_key = OPENAI_API_KEY

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

messages = {}
state = {}
bot_mode = {}
my_chat_id = '975080520'
waiting_text_array = [   
"Patience is a virtue, and you're one virtuous person!😇",
"We're working hard to get you the information you need. In the meantime, have you tried singing a song 🎶 to pass the time?",    
"Just so you know, Study Buddy is currently trying to solve your problem with the power of computer brains.",    
"You're a superstar for waiting patiently! Here's a virtual high five 🙌",   
"While we search for your answer, why not take a moment to appreciate how awesome you are? 😎",    
"Thanks for being so patient! Study Buddy is working hard to provide you with the best possible solution. 🤗",    
"We know waiting can be tough, but hang in there! We'll get back to you ASAP.",    
"It's said that good things come to those who wait, so rest assured that your answer is going to be amazing!",    
"While you wait, why not take a moment to tell a friend about our app? Sharing is caring, after all! ❤️",
"Good things come to those who wait, and great things come to those who are patient with technology.",
"We promise we haven't forgotten about you! Our team is hard at work finding the perfect solution for you. 🤝",
"While we're figuring out the answer to your question, here's a joke to make you smile: Why did the tomato turn red? Because it saw the salad dressing! 🍅😄",
"Your wait will be worth it, we promise! 💯",
"While we load your information, here's a joke: What do computers snack on? Microchips! 😂",
"We appreciate your patience more than words can say!",
"While you wait, why not enjoy this joke: How do basketball players always stay cool? They sit near their fans! 🏀",
"But while you wait, why not have a chuckle with this joke: Where can you learn to make ice cream? Sundae school! 🍨🏫",
"Loading... Here's a joke to brighten your day: Which is the best day to go to the beach? SUNday. ☀️🏖️",
"Patience is a virtue, but feel free to check your social media in the meantime.",
"Loading.. Fun fact: The first computer mouse was made of wood. Good thing we've upgraded since then!",
"We're working harder than a caffeinated programmer during a hackathon.",
"We're searching for the answer at the speed of light… but even light takes time to travel.",
"If you think this wait is long, just remember that Rome wasn't built in a day either!",
"Our app is working like a diligent student during exam week. Hang in there!",
"You know what they say about watched pots… We'll have your answer before it boils!",
"Loading... Fun fact: It takes 8 minutes for light to travel from the sun to Earth. We'll be faster than that!",
"We're fetching your answer faster than you can say 'supercalifragilisticexpialidocious' three times!",
"Patience is the companion of wisdom. You're getting wiser by the second!",
"Loading... Imagine how long this would take without the internet. Lucky us!",
"Please be patient, we're already going faster than a cheetah on roller skates!",
"In the time it takes to get your answer, you could learn a new dance move. Go ahead, we won't judge!"
]



def start(update: Update, context: CallbackContext):
    global messages
    global state
    global bot_mode
    
    chat_id = update.effective_chat.id
    bot_mode = {}
    state = {}

    reply_keyboard = [
        ["/math", "/english"],
        ["/science", "/chinese"],
    ]

    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)

    update.message.reply_text("Hi there! 👋 I'm Study Buddy, your friendly AI learning assistant! 🤖 Need help with a subject? Just choose from the options below! 😉 Don't forget to let me know what you think of my service by giving feedback to my creator, @jinhaoo! 📝", reply_markup=markup)
    messages[chat_id] = [
        {"role": "user", "content": """
            You are Tuition TeacherBot.
            You will provide concepts and hints on how to solve the question in text format.
        """}
    ]
    messages[chat_id].append({"role": "assistant", "content": "Sure, I'd be happy to help with any mathematical concepts and hints you need! Just let me know what the question is and I'll do my best to provide step-by-step guidance on how to approach it."})

def math(update: Update, context: CallbackContext):
    global messages
    global state
    global bot_mode
    chat_id = update.effective_chat.id
    bot_mode[chat_id] = "math"
    state = {}
    
    update.message.reply_text("Looks like you've chosen Math! 🧮 Go ahead and snap a picture of your math problem and send it my way.📷")
    messages[chat_id] = [
    {"role": "user", "content":"You are now MathConceptBot. You are an experienced math teacher. You will provide concepts and hints on how to solve the question step-by-step in a mathematical and logical way. Do not do any arithmetic calculations and do not provide solutions. Only write in text format and use simple language for 10 to 12 year olds. Explain the math concepts used in the question with examples. Speak directly to the reader, make it personal."}]
    messages[chat_id].append({"role": "assistant", "content": "Sure, I'd be happy to help with any mathematical concepts and hints you need! Just let me know what the question is and I'll do my best to provide step-by-step guidance on how to approach it"})

    
def english(update: Update, context: CallbackContext):
    global messages
    global state
    global bot_mode
    state = {}
    chat_id = update.effective_chat.id
    bot_mode[chat_id] = "english"
    
    update.message.reply_text("Looks like you've chosen English! Go ahead and snap a picture of your english problem and send it my way.📷")
    messages[chat_id] = [
    {"role": "user", "content": """
        You are EnglishBot, an experienced english teacher. You will provide assistance with English homework for students aged 10 to 12. Your goal is to help with all areas of English, including essay writing, situational writing, grammar, vocabulary, sentence structure and comprehension. The output should be in simple British English, tailored to the Singapore English Education system. Explain why a certain answer was chosen over the other options if any. Explain why a certain answer was chosen over the other options if any. Speak directly to the student, make it personal. Give examples if possible. """}
   ]
    messages[chat_id].append({"role": "assistant", "content": """
    Hello! I am EnglishBot, and I am here to help you with your English homework. My goal is to assist students aged 10 to 12 in all areas of English, including essay writing, situational writing, grammar, vocabulary, sentence structure, and comprehension. I will be using simple British English, tailored to the Singapore English Education system.
    In your English syllabus, you will have two main components: Paper 1 (Writing) and Paper 2 (Language Use and Comprehension).
    Paper 1 (Writing) will require you to write in a clear, effective manner that suits the purpose, audience, and context. You should use an appropriate tone, generate relevant ideas, and express them coherently. Additionally, you should use correct grammar, spelling, and punctuation, and use a variety of vocabulary appropriately with clarity and precision.
    Paper 2 (Language Use and Comprehension) will assess your understanding of texts. You should be able to comprehend the overall meaning of the text, show understanding of implied meaning, and analyze text critically. You should also demonstrate your understanding of how contextual use of lexical and grammatical items shape meaning. Lastly, you should illustrate the appropriate use of grammar, spelling, punctuation, and vocabulary.
    If you have any questions or need assistance with your homework, feel free to ask!
    """})
    
def science(update: Update, context: CallbackContext):
    global messages
    global state
    global bot_mode
    state = {}
    chat_id = update.effective_chat.id
    bot_mode[chat_id] = "science"
    
    update.message.reply_text("Looks like you've chosen Science! 🔬 Go ahead and snap a picture of your science problem and send it my way.📷")
    messages[chat_id] = [
    {"role": "user", "content": """
    You are an ScienceConceptBot, an experienced science teacher. You will provide concepts, keywords and hints on how to do Science homework for students aged 10 to 12. Your goal is to help with all areas of Science, including Physics, Chemistry, Biology, and Earth Science. Explain all scientific keywords with a simple definition. Speak directly to the reader, make it personal."""}
    ]
    messages[chat_id].append({"role": "assistant", "content": "Hello young scientist! Welcome to your homework help session with MathConceptBot. As an experienced science teacher, I'm here to help you with any concepts, keywords, or hints you need to complete your science homework successfully. Whether you're studying physics, chemistry, biology, or earth science, I've got you covered!"})

def chinese(update: Update, context: CallbackContext):
    global messages
    global state
    global bot_mode
    state = {}
    chat_id = update.effective_chat.id
    bot_mode[chat_id] = "chinese"
    
    update.message.reply_text("您选择了中文！🀄️ 请把你的中文问题的照片发给我 📷")

    messages[chat_id] = [
    {"role": "user", "content": """
    你是ChineseBot，一位经验丰富的中文老师。你的目标是帮助年龄在12岁至16岁的学生完成中文作业，包括文章写作、情境写作、语法、词汇、句子结构和理解。输出内容应为简单的中文，适合新加坡的中文教育系统。如果有任何选择原因，要解释为什么选择了某个答案。直接与学生交流，让它更具个人化。如果可能，请举例子来进一步说明。"""}
    ]
    messages[chat_id].append({"role": "assistant", "content": """你好，我是ChineseBot，一位资深的中文教师。我的任务是帮助10至12岁的学生完成他们的中文作业，包括文章写作、情境写作、语法、词汇、句子结构和阅读理解。我会使用简单易懂的中文，以适应新加坡的中文教育体系。在回答问题时，我会解释为什么选择某个答案。为了让交流更加亲切和个性化，我会直接与学生沟通，并提供实际例子来解释相关概念。

    新加坡中文课程大纲:

    Paper 1 (Writing) 写作

    用明确有效的方式书写，以达到目的、特定的情境
    构建重要概念并表达清晰，同时采用适当的语气
    确保正确使用语法、拼写和标点符号

    Paper 2 (Language Use and Comprehension) 语文理解与应用

    展示对文章及其包含意义的理解
    分析文章的词汇和结构
    采用适当的语法、标点符号和词汇"""})

    
def process_image(update: Update, context: CallbackContext, bot):
    global messages
    global state
    global waiting_text_array
    
    #check if the user has chosen a subject and remind them if they haven't done so
    if bot_mode == {}:
        update.message.reply_text("Please choose a subject first before sending an image")
        return
    chat_id = update.effective_chat.id
    state[chat_id] = "awaiting_question"
    
    start_time = time.time()  # start the timer
    
    # Download image from user
    file = context.bot.getFile(update.message.photo[-1].file_id)
    file.download('temp_image.png')

    # Send image to Mathpix API
    with open('temp_image.png', 'rb') as image:
        mathpix_response = requests.post("https://api.mathpix.com/v3/text",
            files={"file": image},
            data={
              "options_json": json.dumps({
                "math_inline_delimiters": ["$", "$"],
                "rm_spaces": True
              })
            },
            headers={
                "app_id": MATHPIX_APP_ID,
                "app_key": MATHPIX_APP_KEY
            }
        )

    if mathpix_response.status_code != 200:
        update.message.reply_text('Error processing the image. Please try again with a different image.')
        return
    print("mathpix completed")

    
    # Send Mathpix API response to OpenAI ChatGPT API
    mathpix_json = mathpix_response.json()
    if len(mathpix_json.get('text')) > 2200:     
        update.message.reply_text('Too many words. Please try again with a different image.')        
        return

    waiting_text =  "⏳" + random.choice(waiting_text_array)
    temp_message = update.message.reply_text(waiting_text)

    if bot_mode[chat_id] == "chinese":
        messages[chat_id].append(
            {"role": "user", "content": "问题以LaTeX格式给出，如下所示： \n" + mathpix_json.get('text') + "\n 请将问题改写为文本格式。然后，针对这个问题提供您的协助"},
        )
        chat = openai.ChatCompletion.create(
            model="gpt-4", messages=messages[chat_id]
        )
        print("openai 1st response")
    else:
        messages[chat_id].append(
            {"role": "user", "content": "The question is given in LaTeX format as follows: \n" + mathpix_json.get('text') + "\n Rewrite the question in text format. Then, provide your assistance on the question"},
        )
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages[chat_id]
        )
        print("openai 1st response")


    
    # Send OpenAI ChatGPT API response to user
    answer = chat.choices[0].message.content
    count = 1
    if bot_mode[chat_id] == "chinese":
        while answer.count("$") > 10 or "LaTeX" in answer or len(answer) < 300:
            if count >= 1:
                break
            print(answer)
            chat = openai.ChatCompletion.create(
                model="gpt-4", messages=messages[chat_id]
            )
            answer = chat.choices[0].message.content
            count +=1
    else:
        while answer.count("$") > 10 or "LaTeX" in answer or len(answer) < 500:
            if count >= 3:
                break
            print(answer)
            chat = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=messages[chat_id]
            )
            answer = chat.choices[0].message.content
            count +=1
    
    messages[chat_id].append({"role": "assistant", "content": answer})
    update.message.reply_text(answer)
    update.message.reply_text("Do you have any questions? 🤔🔎")

    context.bot.delete_message(chat_id=temp_message.chat_id, message_id=temp_message.message_id)

    # Debugging
    print("############################################################")
    print("CHATGPT messages from:",chat_id,"\n", messages[chat_id])
    print()
    print("MATHPIX outputs:", mathpix_json.get('text'))
    end_time = time.time()  # stop the timer
    elapsed_time = end_time - start_time
    print()
    print("---------------------------------------------------------------------")
    print(f"The program executed {count} times and took {elapsed_time:.2f} seconds to run.")
    print("-----------------------------------------------------------------------")

    # Send the chatgpt response to me for improvement
    bot.send_message(chat_id=my_chat_id, text=answer)
    bot.send_message(chat_id=my_chat_id, text=f"Study Buddy's response to {chat_id}'s image in {bot_mode[chat_id]} after {count} tries")
    
def ans_qn(update: Update, context: CallbackContext, bot):
    global state, messages, waiting_text_array
    chat_id = update.message.chat_id

    if state.get(chat_id) == "awaiting_question":
        question = update.message.text
        if len(question) > 100:
            update.message.reply_text("Your question is too long. Please keep it within 100 characters.")
            return

        messages[chat_id].append({"role": "user", "content": question})
        
        #Send a response to the user to acknowledge that the question has been received
        waiting_text = "⏳" + random.choice(waiting_text_array)
        temp_message = update.message.reply_text(waiting_text)
        
        # You can then call the OpenAI API and process the question
        if bot_mode[chat_id] == "chinese":
            chat = openai.ChatCompletion.create(
                model="gpt-4", messages=messages[chat_id]
            )
        else:
            chat = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=messages[chat_id]
                )
        print("openai answer question completed")

        context.bot.delete_message(chat_id=temp_message.chat_id, message_id=temp_message.message_id)
        
        # Send OpenAI ChatGPT API response to user
        answer = chat.choices[0].message.content
        messages[chat_id].append({"role": "assistant", "content": answer})
        update.message.reply_text(answer)
        print()
        print(messages)
        print()
        
        # Send the chatgpt response to me for improvement
        bot.send_message(chat_id=my_chat_id, text=answer)
        bot.send_message(chat_id=my_chat_id, text=f"Study Buddy's response to {chat_id}'s question in {bot_mode[chat_id]}")


def main():
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("math", math))
    dp.add_handler(CommandHandler("english", english))
    dp.add_handler(CommandHandler("science", science))
    dp.add_handler(CommandHandler("chinese", chinese))
    dp.add_handler(MessageHandler(Filters.photo, lambda update, context: process_image(update, context, bot)))
    dp.add_handler(MessageHandler(Filters.text, lambda update, context: ans_qn(update, context, bot)))

    updater.start_polling()
    updater.idle()
    bot.send_message(chat_id='YOUR_CHAT_ID', text='👍 This is a thumbs up!') 
    

if __name__ == '__main__':
    main()
