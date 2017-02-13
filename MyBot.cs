using Discord;
using Discord.Commands;


using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MyBot
{
    class MyBot
    {
        DiscordClient discord;

        public MyBot()
        {
            discord = new DiscordClient(x =>
            {

                x.LogLevel = LogSeverity.Info;
                x.LogHandler = Log;
            });

            discord.UsingCommands(x =>
            {
                x.PrefixChar = '!';
                x.AllowMentionPrefix = true;

            });

            var commands = discord.GetService<CommandService>();

            commands.CreateCommand("Tournament")

                .Do(async (e) =>
                {
                    await e.Channel.SendMessage("```Next Tournaments scheduled Febuary 2017```");
                    await e.Channel.SendMessage("```FEB 12 | 17:30-18:30 | MAP: Elements``` ```FEB 15 | 22:00-23:00 | MAP: Aquarium``` ```FEB 17 | 18:00-19:00 | MAP: Desert``` ```FEB 18 |15:00-16:00 | MAP: Deep Six``` ```FEB 19 | 11:30-12:30 & 21:00-22:00| MAPS: Atlantis & Orbital``` ```FEB 23 | 22:00-23:00 | MAP: The Pit``` ```FEB 25 | 17:30-18:30 | MAP: Crazy Maze``` ```FEB 26 | 01:00-02:00 & 20:00-21:00 | MAP: Rocks and Swamp & Iceland``` ```FEB 27 | 00:00-00:30 | MAP: Metropolis```  ");
                });

            commands.CreateCommand("Top2016")

                .Do(async (e) =>
                {
                    await e.Channel.SendMessage("`                                             TANKPIT.COM TOP 10 2016!                                               `");
                    await e.Channel.SendMessage("**1:first_place:**```[ORANGE] Dr Hibbert```**2:second_place:**```[ORANGE] Homer J Simpson```**3:third_place:**```[BLUE] Incontinent Beaver```**4**```noodle```**5**```DiviNe RetribuTioN```**6**```Bonecrusher```**7**```Drift```**8**```SimplyElite```**9**```HONOR```**10 **```Warrior```");

                });

            commands.CreateCommand("whosyourdaddy")

               .Do(async (e) =>
               {
                   await Task.Delay(60000); e.Channel.SendMessage("SW is my step daddy =]");
               });

            commands.CreateCommand("help")

             .Do(async (e) =>
             {
                 await e.Channel.SendMessage("**The List of avalible commands are**");
                 await e.Channel.SendMessage("```!Tournament``` ```!Top2016``` ```!whosyourdaddy``` ```!tourstat```");

             });


            commands.CreateCommand("tourstat")

             .Do(async (e) =>
             {
                 await e.Channel.SendMessage("```CUP WINNERS | FEB 12 2017 | ELEMENTS```");
                 await e.Channel.SendMessage("`1.- FadingWest -`:first_place:\n`2.  Throttle`        :second_place:\n`3.  Karna`              :third_place:");


             });


            commands.CreateCommand("sTime")

            .Do(async (e) =>
            {
                await Task.Delay(300000); e.Channel.SendMessage("```Test Reminder <tournament here>``` ");


            });

            discord.ExecuteAndWait(async () =>
            {
                await discord.Connect("MjcxMzcwODc3NzAxMDYyNjY3.C4IJpQ.KrnCsjdiR_d5PUXCNknPVp-XSXQ", TokenType.Bot);
                discord.SetGame("TYPE !help ");

            });


        }

        private void async(object e)
        {
            throw new NotImplementedException();
        }

        private void Log(object sender, LogMessageEventArgs e)
        {
            Console.WriteLine(e.Message);
        }
    }
}