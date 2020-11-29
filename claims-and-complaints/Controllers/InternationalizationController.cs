using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Filters;
using System.Threading;

namespace claims_and_complaints.Controllers
{
    public class InternationalizationController : Controller
    {
        public override void OnActionExecuting(ActionExecutingContext context)
        {
            string languageCode = (string)ControllerContext.RouteData.Values["languageCode"];
            Thread.CurrentThread.CurrentCulture = new System.Globalization.CultureInfo(languageCode);
            Thread.CurrentThread.CurrentUICulture = Thread.CurrentThread.CurrentCulture;
            base.OnActionExecuting(context);
        }
    }
}