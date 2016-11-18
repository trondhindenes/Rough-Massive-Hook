using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Web.Http;
using Models;

namespace Api.Profile.Controllers
{
    public class ProfileController : ApiController
    {
        public UserProfile Get()
        {
            var thisProfile = new UserProfile();
            thisProfile.userName = "This is the userProfile";
            return thisProfile;

        }
    }
}
