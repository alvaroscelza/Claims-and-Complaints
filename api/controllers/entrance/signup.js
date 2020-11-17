module.exports = {
  inputs: {
    email: {
      required: true,
      type: 'string',
      isEmail: true,
    },
    password: {
      required: true,
      type: 'string',
      maxLength: 200,
    },
    fullName:  {
      required: true,
      type: 'string',
    }
  },

  exits: {
    success: {
      description: 'New user account was created successfully.'
    },
    invalid: {
      responseType: 'badRequest',
      description: 'The provided fullName, password and/or email address are invalid.',
      extendedDescription: `If this request was sent from a graphical user interface, the request parameters should 
      have been validated/coerced _before_ they were sent.`
    },
    emailAlreadyInUse: {
      statusCode: 409,
      description: 'The provided email address is already in use.',
    },
  },

  fn: async function ({email, password, fullName}) {
    var newUser = await module.exports.createUser(email, password, fullName, this.req.ip);
    this.req.session.userId = newUser.id;
    module.exports.sendEmailForAccountConfirmation(newUser);
  },

  createUser: async function (email, password, fullName, clientIp) {
    email = email.toLowerCase();
    emailConfirmationToken = sails.helpers.strings.random('url-friendly');
    emailConfirmationTokenExpiration = Date.now() + sails.config.custom.emailProofTokenTTL;
    password = await sails.helpers.passwords.hashPassword(password);

    return await User.create({ email: email, emailConfirmationToken: emailConfirmationToken,
      emailConfirmationTokenExpiration: emailConfirmationTokenExpiration,
      password: password, fullName: fullName, tosAcceptedByIp: clientIp})
    .intercept('E_UNIQUE', 'emailAlreadyInUse')
    .intercept({name: 'UsageError'}, 'invalid')
    .fetch();
  },

  sendEmailForAccountConfirmation: function(newUser){
    await sails.helpers.sendTemplateEmail.with({
      to: newUser.email,
      subject: 'Please confirm your account',
      template: 'email-verify-account',
      templateData: {
        fullName: newUser.fullName,
        token: newUser.emailConfirmationToken
      }
    });
  },
};
