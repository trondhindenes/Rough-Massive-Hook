using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace Models
{
    public class ServiceInfo
    {
        public String controllerName { get; set; }
        public String requestPath { get; set; }
        public String apiVersionString { get; set; }
        public String apiServer { get; set; }
        public String backendServer { get; set; }
        public String backendServerUrl { get; set; }
        public String backendResponseTimeMs { get; set; }
        public String backendServerHostHeader { get; set; }
    }
}