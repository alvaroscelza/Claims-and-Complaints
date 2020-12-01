using Microsoft.AspNetCore.Identity.UI.Services;
using Microsoft.Extensions.Configuration;
using System.Net;
using System.Net.Mail;
using System.Threading.Tasks;

namespace claims_and_complaints.Services
{
    public class EmailSender : IEmailSender
    {
        private readonly IConfiguration _config;

        public EmailSender(IConfiguration config)
        {
            _config = config;
        }

        public Task SendEmailAsync(string email, string subject, string htmlMessage)
        {
            SmtpClient client = CreateSmtpClient();
            string skollarsEmail = "skollars.software.development@gmail.com";
            MailMessage message = new MailMessage(skollarsEmail, email, subject, htmlMessage){ IsBodyHtml = true };
            return client.SendMailAsync(message);
        }

        private SmtpClient CreateSmtpClient()
        {
            return new SmtpClient
            {
                Port = 587,
                Host = "smtp.gmail.com",
                EnableSsl = true,
                DeliveryMethod = SmtpDeliveryMethod.Network,
                UseDefaultCredentials = false,
                Credentials = new NetworkCredential("skollars.software.development@gmail.com", _config["GmailPassword"])
            };
        }
    }
}
