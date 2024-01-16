import selfcord
import re
from poe_api_wrapper import PoeApi

def remove_urls(input_string):
    # Define a regular expression pattern to match URLs
    url_pattern = re.compile(r'https?://\S+|www\.\S+')

    # Use the sub method to replace URLs with an empty string
    result_string = url_pattern.sub('', input_string)

    return result_string

token = "le_token_discord"
bot = selfcord.Bot()
client = PoeApi("le_token_poe")

@bot.on("ready")
async def ready(time):
    print(f"Connected To {bot.user.name}\n Startup took {time:0.2f} seconds")

@bot.on("message")
async def responder(message):
    if str(bot.user.id) in message.content:
        print("command found : " + message.content)
        # Split the message content into parts
        parts = message.content.split(",")

        # Ensure the message contains enough parts
        if len(parts) >= 2:
            author = parts[0].strip()
            author = author.replace("<@1190289562711359600> ", "").strip()
            question = ",".join(parts[1:]).strip()  # Join the remaining parts as the question

            print("author = '" + author + "'")
            ai_author = "unknown"
            
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
            if(author.startswith("Hegel")):
                ai_author = "H-aigel"
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
                await message.channel.send("✨ Je suis " + author + "... hm, voici une réponse possible : ")

            

            # Do something with the decomposed parts (e.g., print or respond)
            # Non-streamed example:
            for chunk in client.send_message(ai_author, question):
                pass
            messageId = chunk["messageId"]
            reponse = remove_urls(chunk["text"])
            reponse = reponse.replace("]](", "]]")

            data = client.get_citations(messageId)

            citations = data['data']['message']['citations']

            # Loop through citations and replace in the response
            for i, citation in enumerate(citations, start=1):
                formatted_citation = f"\n\n >>> *{citation['text']}* \n\n```({citation['title']})```¤"
                formatted_citation = ' '.join(formatted_citation.split())

                reponse = reponse.replace(f"[[{i}]]", f'\n\n {formatted_citation} \n\n')


            # Split reponse using '¤' as the delimiter
            response_parts = reponse.split('¤')

            # Send each part separately
            for part in response_parts:
                await message.channel.send(part)
##        else:
##            # Handle the case where the message doesn't have enough parts
##            await message.channel.send("Oh lala, et c'est le drame...")


bot.run(token)
