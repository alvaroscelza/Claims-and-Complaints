module.exports = {
  friendlyName: 'Signup',
  description: 'Sign up for a new user account.',
  extendedDescription: `This creates a new user record in the database, signs in the requesting user agent by modifying 
  its [session](https://sailsjs.com/documentation/concepts/sessions), and (if emailing with Mailgun is enabled) sends 
  an account verification email. 
  
  If a verification email is sent, the new user's account is put in an "unconfirmed" state until they confirm they are 
  using a legitimate email address (by clicking the link in the account verification message.)`,

  inputs: {
    email: {
      required: true,
      type: 'string',
      isEmail: true,
      description: 'The email address for the new account, e.g. m@example.com.',
      extendedDescription: 'Must be a valid email address.',
    },
    password: {
      required: true,
      type: 'string',
      maxLength: 200,
      example: 'passwordlol',
      description: 'The unencrypted password to use for the new account.'
    },
    fullName:  {
      required: true,
      type: 'string',
      example: 'Frida Kahlo de Rivera',
      description: 'The user\'s full name.',
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
    var newUser = createUser(email, password, fullName);
    this.req.session.userId = newUser.id;
    sendEmailForAccountConfirmation(newUser);
  },

  createUser: function (email, password, fullName) {
    email = email.toLowerCase();
    emailConfirmationToken = sails.helpers.strings.random('url-friendly');
    emailConfirmationTokenExpiration = Date.now() + sails.config.custom.emailProofTokenTTL;
    password = sails.helpers.passwords.hashPassword(password);

    return User.create({ email: email, emailConfirmationToken: emailConfirmationToken,
      emailConfirmationTokenExpiration: emailConfirmationTokenExpiration,
      password: password, fullName: fullName, tosAcceptedByIp: this.req.ip})
    .intercept('E_UNIQUE', 'emailAlreadyInUse')
    .intercept({name: 'UsageError'}, 'invalid')
    .fetch();
  },

  sendEmailForAccountConfirmation: function(newUser){
    sails.helpers.sendTemplateEmail.with({
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
