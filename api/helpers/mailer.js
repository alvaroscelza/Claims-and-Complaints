module.exports = {
  inputs: {
    destinatary: {
      required: true,
      type: 'string',
      isEmail: true,
    },
    subject: {
      required: true,
      type: 'string',
    },
    content: {
      required: true,
      type: 'string',
    },
  },

  fn: async function ({destinatary, subject, htmlContent}) {
    const nodemailer = require("nodemailer");
    let transporter = nodemailer.createTransport({
      host: 'smtp.gmail.com',
      port: 587,
      auth: {
        user: 
        pass: 
      },
    });

    await transporter.sendMail({
      from: sails.config.custom.appName,
      to: destinatary,
      subject: subject,
      html: htmlContent,
    });
  }
};
