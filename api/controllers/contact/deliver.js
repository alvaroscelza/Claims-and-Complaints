module.exports = {
  inputs: {
    email: {
      required: true,
      type: 'string',
    },
    topic: {
      required: true,
      type: 'string',
    },
    fullName: {
      required: true,
      type: 'string',
    },
    message: {
      required: true,
      type: 'string',
    }
  },

  exits: { success: {} },

  fn: async function({email, topic, fullName, message}) {
    let emailTemplatePath = 'emails/email-contact-form'
    let emailTemplateData = { contactName: fullName, contactEmail: email, topic, message, }
    let htmlEmailContents = await sails.renderView(emailTemplatePath, emailTemplateData);
    await sails.helpers.sendMail(sails.config.custom.emailUser, 'New contact form message', htmlEmailContents);
  }
};
