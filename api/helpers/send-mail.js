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
    htmlContent: {
      required: true,
      type: 'string',
    },
  },

  fn: async function ({destinatary, subject, htmlContent}) {
    let emailer = await module.exports.createEmailer();
    await emailer.sendMail({
      from: sails.config.custom.appName,
      to: destinatary,
      subject: subject,
      html: htmlContent,
    });
  },

  createEmailer: async function(){
    const nodemailer = require("nodemailer");
    return nodemailer.createTransport({
      host: sails.config.custom.emailHost,
      port: sails.config.custom.emailPort,
      auth: {
        user: sails.config.custom.emailUser,
        pass: sails.config.local.emailPassword,
      },
    });
  }
};
