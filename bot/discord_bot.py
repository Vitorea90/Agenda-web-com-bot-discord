import discord
from discord.ext import commands, tasks
import os
from datetime import datetime, timedelta
from app.models import task_model
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = os.getenv('DISCORD_CHANNEL_ID')
USER_ID = os.getenv('DISCORD_USER_ID')

intents = discord.Intents.default()
# intents.message_content = True 
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')
    if not check_tasks.is_running():
        check_tasks.start()

@bot.command(name='tarefas')
async def list_tasks(ctx):
    """Mostra as tarefas cadastradas para o dia de hoje."""
    all_tasks = task_model.get_all_tasks()
    hoje = datetime.now().strftime("%Y-%m-%d")
    
    # Filtra apenas tarefas de hoje que não foram concluídas (ou todas de hoje)
    tasks_hoje = [t for t in all_tasks if t['date'] == hoje]
    
    if not tasks_hoje:
        await ctx.send(f"📅 Nenhuma tarefa agendada para hoje ({hoje}).")
        return

    embed = discord.Embed(
        title=f"📋 Tarefas de Hoje ({hoje})", 
        color=0x6c5ce7,
        description="Aqui está o que você tem para hoje:"
    )
    
    for t in tasks_hoje:
        status = "✅ Concluída" if t['completed'] else "⏳ Pendente"
        embed.add_field(
            name=f"{t['time']} - {t['title']}",
            value=f"Status: {status}\n{t['description'] or ''}",
            inline=False
        )
    await ctx.send(embed=embed)

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
    """Verifica tarefas para enviar múltiplas notificações."""
    target = None
    if USER_ID:
        try:
            target = await bot.fetch_user(int(USER_ID))
        except:
            pass
    
    if not target and CHANNEL_ID:
        target = bot.get_channel(int(CHANNEL_ID))

    if not target:
        return

    now = datetime.now()
    all_tasks = task_model.get_all_tasks()

    for task in all_tasks:
        if task['completed']:
            continue
        
        try:
            # Converte data/hora da tarefa
            task_dt = datetime.strptime(f"{task['date']} {task['time']}", "%Y-%m-%d %H:%M:%S" if len(task['time']) > 5 else "%Y-%m-%d %H:%M")
            diff = task_dt - now
            diff_minutes = diff.total_seconds() / 60

            # Verifica cada marco
            notified_list = task.get('notified_milestones', [])
            
            for m in MILESTONES:
                m_id = m['id']
                m_minutes = m['minutes']
                
                # Se estiver dentro da janela do marco e ainda não avisou este marco específico
                # Janela de tolerância de 2 minutos para evitar perder o loop
                if m_id not in notified_list and (m_minutes - 2) <= diff_minutes <= m_minutes:
                    embed = discord.Embed(
                        title=f"🔔 Lembrete: Falta {m['label']}!",
                        description=f"A tarefa **{task['title']}** está agendada para logo mais.",
                        color=0x6c5ce7
                    )
                    embed.add_field(name="Data/Hora", value=f"{task['date']} às {task['time']}", inline=True)
                    embed.add_field(name="Descrição", value=task['description'] or "Sem descrição", inline=False)
                    
                    await target.send(embed=embed)
                    task_model.mark_milestone_notified(task['id'], m_id)
                    break # Envia apenas um tipo de alerta por vez/loop

        except Exception as e:
            print(f"Erro ao processar tarefa {task['id']}: {e}")

def run_bot():
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("ERRO: DISCORD_TOKEN não encontrado no arquivo .env")
