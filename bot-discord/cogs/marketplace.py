import discord
from discord.ext import commands
from typing import Optional
from ..api import marketplace, economy

class Marketplace(commands.Cog):
    """Comandos de mercado de jogadores/itens."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mercado")
    async def listar_mercado(self, ctx):
        """Lista todos os itens/jogadores à venda no mercado."""
        if not marketplace:
            await ctx.send("Nenhum item à venda no momento.")
            return
        msg = "**Itens/Jogadores à venda:**\n"
        for item in marketplace:
            if not item.get("vendido"):
                msg += f"ID: `{item['id']}` | {item['item_nome']} (R${item['preco']}) - {item.get('descricao','')}\n"
        await ctx.send(msg)

    @commands.command(name="vender")
    async def vender_item(self, ctx, preco: int, *, nome: str):
        """Adiciona um item/jogador ao mercado. Uso: !vender <preco> <nome do item>"""
        item = {
            "id": len(marketplace) + 1,
            "vendedor_id": ctx.author.id,
            "item_nome": nome,
            "preco": preco,
            "descricao": f"Vendedor: {ctx.author.display_name}",
            "tipo": "item",
            "vendido": False
        }
        marketplace.append(item)
        await ctx.send(f"Item '{nome}' adicionado ao mercado por R${preco}!")

    @commands.command(name="comprar")
    async def comprar_item(self, ctx, item_id: int):
        """Compra um item do mercado. Uso: !comprar <id do item>"""
        for item in marketplace:
            if item["id"] == item_id and not item["vendido"]:
                vendedor_id = item["vendedor_id"]
                preco = item["preco"]
                eco_comprador = economy.setdefault(ctx.author.id, {"moedas": 100, "banco": 0, "historico": []})
                eco_vendedor = economy.setdefault(vendedor_id, {"moedas": 100, "banco": 0, "historico": []})
                if eco_comprador["moedas"] < preco:
                    await ctx.send("Saldo insuficiente para compra.")
                    return
                eco_comprador["moedas"] -= preco
                eco_vendedor["moedas"] += preco
                eco_comprador["historico"].append({"tipo": "compra", "item": item["item_nome"], "valor": preco})
                eco_vendedor["historico"].append({"tipo": "venda", "item": item["item_nome"], "valor": preco})
                item["vendido"] = True
                item["comprador_id"] = ctx.author.id
                await ctx.send(f"Compra realizada! Você adquiriu '{item['item_nome']}' por R${preco}.")
                return
        await ctx.send("Item não encontrado ou já vendido.")

async def setup(bot):
    await bot.add_cog(Marketplace(bot))
