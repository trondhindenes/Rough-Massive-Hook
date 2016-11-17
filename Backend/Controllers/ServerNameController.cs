using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Web.Http;
using Backend.Models;

namespace Backend.Controllers
{
    public class ServerNameController : ApiController
    {
        public Thing Get()
        {
            var thisThing = new Thing();
            var hostHeader = Request.RequestUri.Host;
            thisThing.localComputerName = System.Environment.GetEnvironmentVariable("computername");
            thisThing.localHostHeader = hostHeader;
            return thisThing;

        }
    }
}
