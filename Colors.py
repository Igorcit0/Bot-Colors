import discord
import asyncio
import random
import os
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Ahora obtén las variables de entorno
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
GUILD_ID = int(os.getenv('DISCORD_GUILD_ID'))
ROLE_ID = int(os.getenv('DISCORD_ROLE_ID'))

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.message_content = True

client = discord.Client(intents=intents)

# Función para generar un color hexadecimal aleatorio
def get_random_color():
    return discord.Colour.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

async def change_role_color():
    await client.wait_until_ready()
    guild = client.get_guild(GUILD_ID)
    if not guild:
        print(f"Error: No se encontró el servidor con ID {GUILD_ID}.")
        return

    role_to_change = guild.get_role(ROLE_ID)
    if not role_to_change:
        print(f"Error: No se encontró el rol con ID {ROLE_ID} en el servidor '{guild.name}'.")
        return

    print(f"Iniciando el cambio continuo de color para el rol ID '{ROLE_ID}' en el servidor '{guild.name}'.")
    while not client.is_closed():
        try:
            new_color = get_random_color()
            await role_to_change.edit(colour=new_color)
            print(f"Cambiado el color del rol ID '{ROLE_ID}' a {new_color}")
            await asyncio.sleep(2)  # Cambiar color cada 2 segundos (ajusta según sea necesario)
        except Exception as e:
            print(f"Ocurrió un error al cambiar el color del rol: {e}")
            await asyncio.sleep(5) # Esperar más tiempo si ocurre un error para evitar reintentos rápidos

@client.event
async def on_ready():
    print(f'Iniciado como {client.user.name} ({client.user.id})')
    client.loop.create_task(change_role_color())

client.run(TOKEN)
