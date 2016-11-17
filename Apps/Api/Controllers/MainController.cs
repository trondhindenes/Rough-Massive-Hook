using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Web.Http;
using Api.Models;
using System.Configuration;

namespace Api.Controllers
{
    public class MainController : ApiController
    {
        public ServiceInfo Get()
        {
            // a change
            var client = new WebClient();
            client.Headers.Add("content-type", "applicaton/json");
            String url = ConfigurationManager.AppSettings["backend"];
            string backendServerNameUrl = String.Format("{0}/api/ServerName", url);
            var watch = System.Diagnostics.Stopwatch.StartNew();
            var webResult = client.DownloadString(backendServerNameUrl);

            Thing thisThing = Newtonsoft.Json.JsonConvert.DeserializeObject<Thing>(webResult);

            watch.Stop();
            var elapsedMs = watch.ElapsedMilliseconds;


            ServiceInfo thisServiceInfo = new ServiceInfo();
            thisServiceInfo.apiServer = System.Environment.GetEnvironmentVariable("computername");
            thisServiceInfo.backendServer = thisThing.localComputerName;
            thisServiceInfo.backendServerHostHeader = thisThing.localHostHeader;
            thisServiceInfo.backendServerUrl = url;
            thisServiceInfo.backendResponseTimeMs = elapsedMs.ToString();
            return thisServiceInfo;
        }
    }
}
