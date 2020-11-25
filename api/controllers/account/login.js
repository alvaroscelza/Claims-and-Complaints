module.exports = {
  inputs: {
    email: { required: true, type: 'string', isEmail: true, },
    password: { required: true, type: 'string', maxLength: 200, },
    rememberMe: { type: 'boolean' }
  },

  fn: async function ({ email, password, rememberMe }) {
    try{
      let user = await module.exports.getUserByEmail(email.toLowerCase());
      await module.exports.checkUser(user);
      await module.exports.checkPassword(password, user);
      await module.exports.handleRememberMe(rememberMe, this.req.session.cookie.maxAge);
      await sails.helpers.logUserIn(user, this.req.session);
      return this.res.redirect('/');
    } catch(ex) {
      return this.res.view('pages/account/login', { page_name: 'Login', me: undefined, syncing: false, cloudError: ex.message });
    }
  },

  getUserByEmail: async function (email) {
    return await User.findOne({ email: email });
  },

  checkUser: async function (user) {
    if(!user) throw 'invalidUser';
  },

  checkPassword: async function (password, user) {
    await sails.helpers.passwords.checkPassword(password, user.password);
  },

  handleRememberMe: async function (rememberMe, maxAgeCookie) {
    if (rememberMe) maxAgeCookie = sails.config.custom.rememberMeCookieMaxAge;
  },
};
