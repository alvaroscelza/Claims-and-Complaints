module.exports = {
  inputs: {
    email: { required: true, type: 'string', isEmail: true, },
    password: { required: true, type: 'string', maxLength: 200, },
    rememberMe: { type: 'boolean' }
  },

  exits: {
    success: {},
    emailOrPasswordIncorrect: { viewTemplatePath: 'pages/account/login' },
  },

  fn: async function (inputs, exits) {
    let user = await module.exports.getUserByEmail(inputs.email.toLowerCase());
    await module.exports.checkUser(user, exits);
    await module.exports.checkPassword(inputs, user, exits);
    await module.exports.handleRememberMe(inputs.rememberMe, this.req.session.cookie.maxAge);
    await sails.helpers.logUserIn(user, this.req.session);
    return exits.success({ page_name: 'Login' });
  },

  getUserByEmail: async function (email) {
    return await User.findOne({ email: email });
  },

  checkUser: async function (user, exits) {
    if(!user) return exits.emailOrPasswordIncorrect({ page_name: 'Email or password incorrect' });
  },

  checkPassword: async function (inputs, user, exits) {
    try {
      await sails.helpers.passwords.checkPassword(inputs.password, user.password);
    }
    catch(err) {
      return exits.emailOrPasswordIncorrect({ page_name: 'Email or password incorrect' });
    }
  },

  handleRememberMe: async function (rememberMe, maxAgeCookie) {
    if (rememberMe) maxAgeCookie = sails.config.custom.rememberMeCookieMaxAge;
  },
};
