import selfcord
import re
import json
from poe_api_wrapper import PoeApi



def remove_urls(input_string):
    # Define a regular expression pattern to match URLs
    url_pattern = re.compile(r'https?://\S+|www\.\S+')

    # Use the sub method to replace URLs with an empty string
    result_string = url_pattern.sub('', input_string)

    return result_string







# File path to store all data in a single file
ALL_DATA_FILE = "all_data.json"

# Load existing data from the file
try:
    with open(ALL_DATA_FILE, 'r') as file:
        all_data = json.load(file)
except FileNotFoundError:
    # If the file is not found, initialize an empty dictionary
    all_data = {"user_chat_codes": {}, "ai_author_data": {}, "user_ai_author_association": {}}

def save_all_data():
    # Save all data to the file
    with open(ALL_DATA_FILE, 'w') as file:
        json.dump(all_data, file)

    

token = ""
bot = selfcord.Bot()
client = PoeApi("")


@bot.on("ready")
async def ready(time):
    print(f"Connected To {bot.user.name}\n Startup took {time:0.2f} seconds")

@bot.on("message")
async def responder(message):
    # Check if the message is a reply to the bot
    if message.author == bot.user:
        return ""
    if str(bot.user.id) in message.content:
        print("command found : " + message.content)
        
        if(message.content == "<@1190289562711359600> ?"):
            await message.channel.send("""
```@Daïmon [auteur], [question]```
Auteurs : \n
`Épicure, Platon, Aristote, Spinoza, Kant, Descartes, Rousseau, Hume, Hegel, Schopenhauer, Nietzsche, Sartre, Arendt, Wittgenstein`
""")
            return ""
            
        # Split the message content into parts
        parts = message.content.split(",")

        # Ensure the message contains enough parts
        if len(parts) >= 2:
            author = parts[0].strip()   # Hobbes
            author = author.replace("<@1190289562711359600> ", "").strip()
            question = ",".join(parts[1:]).strip()  # Join the remaining parts as the question

            print("author = '" + author + "'")
            ai_author = "unknown"

            if(author.startswith("Socrate")):
                ai_author = "Socrate-AI"
            if(author.startswith("Heidegger")):
                ai_author = "H-aidegger"
            if(author.startswith("Épicure")):
                ai_author = "Ep-aicure"
            if(author.startswith("Platon")):
                ai_author = "Pl-aiton"
            if(author.startswith("Aristote")):
                ai_author = "Ai-ristote"
            if(author.startswith("Spinoza")):
                ai_author = "Sp-ainoza"
            if(author.startswith("Kant")):
                ai_author = "K-aint"
            if(author.startswith("Descartes")):
                ai_author = "D-aicartes"
            if(author.startswith("Hobbes")):
                ai_author = "Hobb-ais"
            if(author.startswith("Rousseau")):
                ai_author = "Rousse-aiu"
            if(author.startswith("Hume")):
                ai_author = "Hume-ai"
            if(author.startswith("Hegel")):
                ai_author = "H-aigel"
            if(author.startswith("Schopenhauer")):
                ai_author = "Schopenh-aiuer"
            if(author.startswith("Nietzsche")):
                ai_author = "N-aitzsche"
            if(author.startswith("Sartre")):
                ai_author = "S-airtre"
            if(author.startswith("Arendt")):
                ai_author = "Ai-rendt"
            if(author.startswith("Wittgenstein")):
                ai_author = "Wittg-ainstein"
            if(author.startswith("Commentaire")):
                ai_author = "Platon-eprof-texte"
            if(author.startswith("Dissertation")):
                ai_author = "Platon-eprof"

            if(ai_author == "unknown"):
                #await message.channel.send("Hm, je connais bien Épicure, Platon, Aristote, Spinoza, Kant, Descartes, Rousseau, Hegel, Nietzsche, Sartre, Arendt... Je peux aussi répondre à des questions sur le commentaire de texte ou la dissertation ! Il suffit de me tag et d'indiquer le nom du philosophe ou l'exercice en premier dans le message.")
                return ""
            
            if author.startswith("Commentaire"):
                # Handle the case where author starts with "Commentaire"
                await message.channel.send("🧑‍🏫🎒 Analyse de commentaire / d'explication de texte en cours...")
            elif author.startswith("Dissertation"):
                # Handle the case where author starts with "Dissertation"
                await message.channel.send("🧑‍🏫🎒 Analyse de dissertation en cours...")
            else:
                # Handle other cases
                await message.channel.send("... ✨ " + author + " vient de se réveiller...")

            

            # Do something with the decomposed parts (e.g., print or respond)
            # Non-streamed example:
            for chunk in client.send_message(ai_author, question):
                pass
            messageId = chunk["messageId"]
            print("normal response = " + chunk["text"])
            reponse = remove_urls(chunk["text"])
            reponse = reponse.replace("]](", "]]")

            data = client.get_citations(messageId)

            citations = data['data']['message']['citations']

            # Loop through citations and replace in the response
            for i, citation in enumerate(citations, start=1):
                formatted_citation = ">>> *"+citation['text']+"*" + "\n\n" + "```("+citation['title']+")```¤"
                formatted_citation = ' '.join(formatted_citation.split())

                reponse = reponse.replace(f"[[{i}]]", "\n\n "+formatted_citation+" \n\n")


            # Split reponse using '¤' as the delimiter
            response_parts = reponse.split('¤')

            # Save the chatCode and ai_author in their respective dictionaries
            all_data["user_chat_codes"][str(message.author.id)] = {"chatCode": chunk["chatCode"], "ai_author": ai_author}
            all_data["ai_author_data"][ai_author] = ai_author  # Add the ai_author if it doesn't exist
            all_data["user_ai_author_association"][str(message.author.id)] = {"ai_author": ai_author}

            all_data["user_ai_author_association"][message.author.id] = {"ai_author": author}

            # Save all data to the file
            save_all_data()
            
            # Send each part separately
            for part in response_parts:
                await message.channel.send(part)
##        else:
##            # Handle the case where the message doesn't have enough parts
##            await message.channel.send("Oh lala, et c'est le drame...")

@bot.on("message")
async def user_reply(message):
    if(message.content.startswith("<")):
        return ""
    if(len(message.mentions) == 0):
        print("pas de mention, ciao")
        return ""
    # Check if the message is a reply to the bot
    if message.author != bot.user:
        print(message.author)
        print(bot.user)
    
    if str(message.author.id) in all_data["user_chat_codes"]:
        author_id = str(message.author.id)
        ai_author = ""
        user_association_data = all_data["user_ai_author_association"][author_id]
        ai_author = user_association_data["ai_author"]
        
        # sanitiaze the message
        question = message.content.strip()

        
        if(ai_author.startswith("Socrate")):
            ai_author = "Socrate-AI"
        if(ai_author.startswith("Heidegger")):
            ai_author = "H-aidegger"
        if(ai_author.startswith("Épicure")):
            ai_author = "Ep-aicure"
        if(ai_author.startswith("Platon")):
            ai_author = "Pl-aiton"
        if(ai_author.startswith("Aristote")):
            ai_author = "Ai-ristote"
        if(ai_author.startswith("Spinoza")):
            ai_author = "Sp-ainoza"
        if(ai_author.startswith("Kant")):
            ai_author = "K-aint"
        if(ai_author.startswith("Descartes")):
            ai_author = "D-aicartes"
        if(ai_author.startswith("Hobbes")):
            ai_author = "Hobb-ais"
        if(ai_author.startswith("Rousseau")):
            ai_author = "Rousse-aiu"
        if(ai_author.startswith("Hume")):
            ai_author = "Hume-ai"
        if(ai_author.startswith("Hegel")):
            ai_author = "H-aigel"
        if(ai_author.startswith("Schopenhauer")):
            ai_author = "Schopenh-aiuer"
        if(ai_author.startswith("Nietzsche")):
            ai_author = "N-aitzsche"
        if(ai_author.startswith("Sartre")):
            ai_author = "S-airtre"
        if(ai_author.startswith("Arendt")):
            ai_author = "Ai-rendt"
        if(ai_author.startswith("Wittgenstein")):
            ai_author = "Wittg-ainstein"
        if(ai_author.startswith("Commentaire")):
            ai_author = "Platon-eprof-texte"
        if(ai_author.startswith("Dissertation")):
            ai_author = "Platon-eprof"

        print("reply question = " + question)
        print("reply ai author = " + ai_author)
        chat_code_data = all_data["user_chat_codes"][str(message.author.id)]
        chat_code = chat_code_data["chatCode"]
        print("reply chat code = " + chat_code)
        #ai_author = chat_code_data["ai_author"]

        # Check if the user has previously interacted with the specific ai_author
        if ai_author in all_data["ai_author_data"]:
           
            print("reply author = '" + ai_author + "'")
            # Do something with the decomposed parts (e.g., print or respond)
            # Non-streamed example:
            for chunk in client.send_message(ai_author, question, chatCode=chat_code):
                pass
            messageId = chunk["messageId"]
            print("reply response = " + chunk["text"])
            reponse = remove_urls(chunk["text"])
            reponse = reponse.replace("]](", "]]")

            data = client.get_citations(messageId)

            citations = data['data']['message']['citations']

            # Loop through citations and replace in the response
            for i, citation in enumerate(citations, start=1):
                formatted_citation = ">>> *"+citation['text']+"*" + "\n\n" + "```("+citation['title']+")```¤"
                formatted_citation = ' '.join(formatted_citation.split())

                reponse = reponse.replace(f"[[{i}]]", "\n\n "+formatted_citation+" \n\n")


            # Split reponse using '¤' as the delimiter
            response_parts = reponse.split('¤')

            # Save the chatCode and ai_author in their respective dictionaries
            all_data["user_chat_codes"][str(message.author.id)] = {"chatCode": chunk["chatCode"], "ai_author": ai_author}
            all_data["ai_author_data"][ai_author] = ai_author  # Add the ai_author if it doesn't exist
            all_data["user_ai_author_association"][str(message.author.id)] = {"ai_author": ai_author}

            # Save all data to the file
            save_all_data()
            
            # Send each part separately
            for part in response_parts:
                await message.channel.send(part)

        else:
            save_all_data()

        
        
bot.run(token)
