import discord
from discord.ext import commands
from discord.ui import Button, View

# Configura il bot con intents
intents = discord.Intents.default()
intents.message_content = True  # Per gestire contenuti dei messaggi
bot = commands.Bot(command_prefix='/', intents=intents)

# Funzione per inviare il modulo domanda per domanda
async def send_application_form(user, application_type):
    if application_type == 'chat-mod':
        questions = [
            "Come ti chiami?",
            "Quanti anni hai?",
            "Perché vuoi candidarti?",
            "Come ti chiami in gioco?",
            "Quanto saresti bravo nel moderare le varie chat da 1 a 10?",
            "Hai già delle esperienze? Se sì, in quali server?"
        ]
    elif application_type == 'staff':
        questions = [
            "Come ti chiami in gioco?",
            "Quanti anni hai?",
            "Perché vuoi candidarti?",
            "Quanto saresti bravo a moderare i player in farm da 1 a 10?",
            "Hai già avuto esperienze in altre farm? Se sì, in quali?",
            "Quanto investiresti nella farm?"
        ]

    try:
        await user.send("Iniziamo il modulo. Rispondi alle seguenti domande una per una.")
        answers = []  # Lista per salvare le risposte dell'utente

        for question in questions:
            await user.send(question)

            def check(m):
                return m.author == user and isinstance(m.channel, discord.DMChannel)

            try:
                msg = await bot.wait_for('message', check=check, timeout=300)  # Timeout di 5 minuti
                answers.append(msg.content)
            except discord.TimeoutError:
                await user.send("Hai impiegato troppo tempo a rispondere. Modulo annullato.")
                return

        # Al termine, conferma il completamento
        await user.send("Hai completato il modulo! Grazie per la tua candidatura.")

        # Recupera il canale "𝙍𝙚𝙨𝙤𝙘𝙤𝙣𝙩𝙤-𝙨𝙩𝙖𝙛𝙛"
        guild = user.guild
        channel = discord.utils.get(guild.text_channels, name="𝙍𝙚𝙨𝙤𝙘𝙤𝙣𝙩𝙤-𝙨𝙩𝙖𝙛𝙛")
        if channel:
            embed = discord.Embed(
                title=f"Candidatura per {application_type.replace('-', ' ').capitalize()}",
                description=f"Risposte fornite da {user.mention}",
                color=discord.Color.blue()
            )
            for i, answer in enumerate(answers, start=1):
                embed.add_field(name=f"Domanda {i}", value=answer, inline=False)

            await channel.send(embed=embed)
        else:
            print("Canale 𝙍𝙚𝙨𝙤𝙘𝙤𝙣𝙩𝙤-𝙨𝙩𝙖𝙛𝙛 non trovato.")

    except discord.Forbidden:
        print(f"Non posso inviare DM a {user.name}. Verifica le impostazioni della privacy.")

# Comando /candidatura
@bot.tree.command(name='candidatura')
async def candidatura(interaction: discord.Interaction):
    print(f"Comando /candidatura eseguito da {interaction.user.name}")
    
    # Verifica permessi
    if not any(role.name == "OWNER" for role in interaction.user.roles):
        await interaction.response.send_message("Non hai il permesso per usare questo comando.", ephemeral=True)
        return

    # Crea i bottoni
    button_chat_mod = Button(label="Candidati per Chat-Mod", style=discord.ButtonStyle.success, custom_id="chat_mod")
    button_staff = Button(label="Candidati per Staff", style=discord.ButtonStyle.primary, custom_id="staff")

    # Funzione callback
    async def button_callback(interaction: discord.Interaction):
        custom_id = interaction.data["custom_id"]  # Ottieni il custom_id
        print(f"Bottone cliccato: {custom_id}")
        
        if custom_id == "chat_mod":
            await send_application_form(interaction.user, 'chat-mod')
        elif custom_id == "staff":
            await send_application_form(interaction.user, 'staff')

        await interaction.response.send_message(
            f"Ti abbiamo inviato il modulo per {custom_id.replace('_', ' ').capitalize()}!", ephemeral=True
        )

    # Assegna callback ai bottoni
    button_chat_mod.callback = button_callback
    button_staff.callback = button_callback

    # Crea e invia la vista
    view = View()
    view.add_item(button_chat_mod)
    view.add_item(button_staff)
    await interaction.response.send_message("Scegli per quale ruolo ti vuoi candidare:", view=view)

# Gestione errori
@bot.event
async def on_error(event, *args, **kwargs):
    print(f"Errore nell'evento {event}: {args}, {kwargs}")

# Evento on_ready
@bot.event
async def on_ready():
    print(f'Bot connesso come {bot.user}')
    await bot.tree.sync()

# Inserisci il token direttamente qui
TOKEN = "MTMzMDg4OTEzMDM2Mzg0NjY5OA.Gt5SEg.lbekN7f9VEDDCAnsL0PXCptp2f2kMraR7gTkG4"

# Avvio del bot
if TOKEN:
    bot.run(TOKEN)
else:
    print("Errore: Il token del bot non è stato inserito!")
