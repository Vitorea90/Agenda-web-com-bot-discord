import discord
import logging
import os
from discord.ext import commands, tasks
from datetime import datetime
from dotenv import load_dotenv
from app.models import task_model

# Configuração do logger para o bot
logger = logging.getLogger("DiscordBot")

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = os.getenv('DISCORD_CHANNEL_ID')
USER_ID = os.getenv('DISCORD_USER_ID')

intents = discord.Intents.default()
# Habilite intents.message_content se precisar de comandos mais complexos futuramente
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    """ Evento disparado quando o bot se conecta com sucesso. """
    logger.info(f'Bot conectado com sucesso como {bot.user}')
    if not check_tasks.is_running():
        logger.info("Iniciando loop de verificação de tarefas...")
        check_tasks.start()

@bot.command(name='tarefas')
async def list_tasks(ctx):
    """ Comando para listar as tarefas agendadas para o dia atual. """
    logger.info(f"Comando !tarefas recebido de {ctx.author}")
    try:
        all_tasks = task_model.get_all_tasks()
        hoje = datetime.now().strftime("%Y-%m-%d")
        
        tasks_hoje = [t for t in all_tasks if t['date'] == hoje]
        
        if not tasks_hoje:
            await ctx.send(f"📅 Nenhuma tarefa encontrada para hoje ({hoje}). Aproveite o seu dia!")
            return

        embed = discord.Embed(
            title=f"📋 Agenda de Hoje ({hoje})", 
            color=0x6c5ce7,
            description="Confira o que temos planejado:"
        )
        
        for t in tasks_hoje:
            status = "✅ Concluída" if t['completed'] else "⏳ Pendente"
            embed.add_field(
                name=f"⏰ {t['time']} - {t['title']}",
                value=f"**Status**: {status}\n{t['description'] or '_Sem descrição_.'}",
                inline=False
            )
        await ctx.send(embed=embed)
    except Exception as e:
        logger.error(f"Erro ao processar comando list_tasks: {e}")
        await ctx.send("❌ Ocorreu um erro interno ao buscar as tarefas.")

# Configuração dos marcos de notificação (em minutos antes da tarefa)
MILESTONES = [
    {"id": "7d", "minutes": 10080, "label": "7 dias"},
    {"id": "24h", "minutes": 1440, "label": "24 horas"},
    {"id": "5h", "minutes": 300, "label": "5 horas"},
    {"id": "1h", "minutes": 60, "label": "1 hora"},
    {"id": "10m", "minutes": 10, "label": "10 minutos"}
]

@tasks.loop(seconds=60)
async def check_tasks():
    """ 
    Loop periódico que verifica tarefas próximas e envia notificações.
    A verificação ocorre a cada 60 segundos.
    """
    try:
        target = None
        # Tenta pegar o alvo (Usuário via DM ou Canal específico)
        if USER_ID:
            try:
                target = await bot.fetch_user(int(USER_ID))
            except Exception as e:
                logger.warning(f"Não foi possível encontrar usuário ID {USER_ID}: {e}")
        
        if not target and CHANNEL_ID:
            target = bot.get_channel(int(CHANNEL_ID))

        if not target:
            # Se não houver destino configurado, silencia o loop para não poluir logs excessivamente
            return

        now = datetime.now()
        all_tasks = task_model.get_all_tasks()

        for task in all_tasks:
            # Ignora tarefas já feitas
            if task.get('completed'):
                continue
            
            try:
                # Formato de data flexível
                fmt = "%Y-%m-%d %H:%M:%S" if len(task['time']) > 5 else "%Y-%m-%d %H:%M"
                task_dt = datetime.strptime(f"{task['date']} {task['time']}", fmt)
                
                diff = task_dt - now
                diff_minutes = diff.total_seconds() / 60

                notified_list = task.get('notified_milestones', [])
                
                for m in MILESTONES:
                    m_id = m['id']
                    m_minutes = m['minutes']
                    
                    # Janela de tolerância de 2 minutos para garantir que o loop de 60s não perca o momento
                    if m_id not in notified_list and (m_minutes - 2) <= diff_minutes <= m_minutes:
                        logger.info(f"Enviando lembrete '{m_id}' para tarefa: {task['title']}")
                        
                        embed = discord.Embed(
                            title=f"🔔 Lembrete: {m['label']} para o compromisso!",
                            description=f"Sua tarefa **{task['title']}** está chegando em breve.",
                            color=0x00d2d3
                        )
                        embed.add_field(name="Horário", value=f"📅 {task['date']} às ⏰ {task['time']}", inline=True)
                        if task['description']:
                            embed.add_field(name="Sobre", value=task['description'], inline=False)
                        
                        await target.send(embed=embed)
                        task_model.mark_milestone_notified(task['id'], m_id)
                        break 

            except ValueError as ve:
                logger.error(f"Formato de data inválido na tarefa {task.get('id', 'N/A')}: {ve}")
            except Exception as e:
                logger.error(f"Erro ao processar lembrete da tarefa {task.get('id', 'N/A')}: {e}")

    except Exception as e:
        logger.error(f"Erro crítico no loop de verificação: {e}")

def run_bot():
    """ Inicializa a execução do bot do Discord. """
    if not TOKEN:
        logger.error("Falha ao iniciar: DISCORD_TOKEN não encontrado no .env")
        return

    try:
        bot.run(TOKEN)
    except discord.LoginFailure:
        logger.error("Erro de login: O Token do Discord fornecido é inválido.")
    except Exception as e:
        logger.error(f"Erro inesperado ao iniciar o bot: {e}")

