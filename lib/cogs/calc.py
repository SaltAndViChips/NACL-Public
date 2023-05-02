from discord.ext.commands import Cog
from discord.ext.commands import command, has_permissions
from discord.utils import get
from discord.ext import commands
from discord import app_commands
from typing import Optional
from discord import Embed


class calc(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="htest")
    async def htest(self, ctx):
        await ctx.send("test")

    # @hybrid_command(name="RPM")
    # async def RPM(ctx, basestat: str, rpmstat: str, talent1: str, talent2: str):
    #     ctx.send("test")

    @commands.hybrid_command(name="damage")
    async def damage(self, ctx, base_damage: str, damage_stat: Optional[str], talent1: Optional[str], talent2: Optional[str], hsm: Optional[str], armor: Optional[bool], hardhat: Optional[str]):
      fields = [("Base Damage", base_damage, True)]
      if base_damage:
        try:
          base_damage = float(base_damage)
        except ValueError:
          base_damage = ""
          base_damage = False
      else:
        base_damage = False

      if damage_stat:
        try:
          stat = float(damage_stat)
          fields.append(("Damage Stat", damage_stat, True))
        except ValueError:
          damage_stat = ""
          stat = False
      else:
        stat = False

      if talent2:
        try:
          talent2 = float(talent2)
          fields.append(("Second Talent", talent2, True))
        except ValueError:
          talent2 = ""
          talent2 = False
      else:
        talent2 = False

      if talent1:
        try:
          talent = float(talent1)
          fields.append(("First Talent", talent1, True))
        except ValueError:
          talent1 = ""
          talent = False
      else:
        talent = False

      if hsm:
        try:
          hsm = float(hsm)
          fields.append(("Headshot Multiplier", hsm, True))
        except ValueError:
          hsm = ""
          hsm = False
      else:
        hsm = False

      if hardhat:
        try:
          HH = float(hardhat)
          fields.append(("Hard Hat", hardhat, True))
        except ValueError:
          hardhat = ""
          HH = False
      else:
        HH = False


      if talent2 and base_damage and stat and talent:
          output = (base_damage*(1+stat/100)*(1+talent/100)*(1+talent2/100))
      elif talent2 and talent and base_damage:
        output = (base_damage*(1+talent/100)*(1+talent2/100))
      elif base_damage and stat and talent:
        output = (base_damage*(1+stat/100)*(1+talent/100))
      elif base_damage and stat:
        output = (base_damage*(1+stat/100))
      elif base_damage and talent:
        output = (base_damage*(1+talent/100))
      elif base_damage:
        output = base_damage
      else:
        output = 0
      if str(output) == "0" or str(output) == "You need to input a base damage!":
        pass
      else:
        if armor:
          output = (f"{float(output)*0.7:.2f}")
        if hsm:
          output = (f"{float(output)*float(hsm):.2f}")
        if hardhat and HH:
          output = (f"{float(output)*(1-float(hardhat)/100):.2f}")
        if output is float:
          output = (f"{float(output):.2f}")
        if 100%(float(output)) == 0:
          shots = 100//(float(output))
          output = (f"{float(output):.2f} | Shots to kill: {shots}")
        else:
          shots = (100//(float(output)))+1
          output = (f"{float(output):.2f} | Shots to kill: {shots}")
        fields.append(("Damage", output, False))
        embed = Embed(
          title=f"Damage Calculator",
          color=0x00FA9A,
        )
        for name, value, inline in fields:
          embed.add_field(name=name, value=value, inline=inline)
        embed.set_footer(text="♥")
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="rpm")
    async def RPM(self,ctx, base_rpm: str, rpm_stat: Optional[str], talent: Optional[str]):
      fields = [("Base RPM", base_rpm, True)]
      output = ""
      RPMCaps = [72, 88, 90, 99, 110, 120, 132, 165, 180, 198, 220, 264, 360, 396, 440, 495, 565, 660, 792, 990, 1320,
                 1980, 3960]
      nextrpm = None
      output = ""
      if base_rpm:
        try:
          base_rpm = float(base_rpm)
        except ValueError:
          base_rpm = ""
          base_rpm = False
      else:
        base_rpm = False
      if rpm_stat:
        try:
          stat = float(rpm_stat)
          fields.append(("RPM Stat", rpm_stat, True))
        except ValueError:
          rpm_stat = ""
          stat = False
      else:
        stat = False
      if talent:
        try:
          talent = float(talent)
          fields.append(("Talent", talent, True))
        except ValueError:
          talent = ""
          talent = False
      else:
        talent = False
      if stat and stat >= 100 or talent and talent >= 100:
        output = "∞"
      elif base_rpm and stat and talent:
        output = ((base_rpm / (1 - stat / 100)) / (1 - talent / 100))
      elif base_rpm and stat:
        output = ((base_rpm / (1 - stat / 100)) / 1 - talent / 100)
      elif base_rpm and talent:
        output = base_rpm / (1 - talent / 100)
      elif base_rpm:
        output = base_rpm
      else:
        output = 0
      output = (f"{float(output):.2f}")
      if output.replace('.', '', 1).isdigit():
        truerpm = float(output)
        if float(output) < 72:
          nextrpm = float(output) + 1
          actual = output
          fields.append(("True RPM", output, False))
          fields.append(("Actual RPM", actual, True))
          fields.append(("Next RPM", nextrpm, True))
        else:
          for cap in RPMCaps:
            if not nextrpm:
              if float(output) >= cap:
                actual = cap
                pass
              else:
                nextrpm = cap
          fields.append(("True RPM", output, False))
          fields.append(("Actual RPM", actual, True))
          fields.append(("Next RPM", nextrpm, True))

      embed = Embed(
        title=f"RPM Calculator",
        color=0x00FA9A,
      )
      for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)
      embed.set_footer(text="♥")
      await ctx.send(embed=embed)








async def setup(bot):
    await bot.add_cog(calc(bot))