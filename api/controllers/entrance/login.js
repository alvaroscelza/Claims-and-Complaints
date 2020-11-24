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
    rememberMe: {
      type: 'boolean'
    }
  },

  exits: {
    success: {},
    emailOrPasswordIncorrect: { viewTemplatePath: 'pages/entrance/login' },
  },

  fn: async function ({email, password, rememberMe}) {
    let user = await module.exports.getUserByEmail(email.toLowerCase());
    await module.exports.checkUser(user, exits);
    await sails.helpers.passwords.checkPassword(password, user.password).intercept('incorrect', 'emailOrPasswordIncorrect');
    await module.exports.handleRememberMe(rememberMe, this.req.session.cookie.maxAge);
    await sails.helpers.logUserIn(user, this.req.session);
  },

  getUserByEmail: async function (email) {
    return await User.findOne({ email: email });
  },

  checkUser: async function (user, exits) {
    if(!user) return exits.emailOrPasswordIncorrect({ page_name: 'Email or password incorrect' });
  },

  handleRememberMe: async function (rememberMe, maxAgeCookie) {
    if (rememberMe) maxAgeCookie = sails.config.custom.rememberMeCookieMaxAge;
  },
};
