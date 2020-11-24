module.exports = {
  inputs: {
    token: { 
      type: 'string',
      required: true,
    },
  },

  exits: {
    success: { viewTemplatePath: 'pages/entrance/confirmed-email' },
    invalidOrExpiredToken: { viewTemplatePath: 'errors/498' },
  },

  fn: async function (inputs, exits) {
    let user = await module.exports.getUserByToken(inputs.token);
    await module.exports.checkUserAndTokenExpiration(user, exits);
    await module.exports.confirmUser(user);
    await sails.helpers.logUserIn(user, this.req.session);
    return exits.success({ page_name: 'Confirmed email' });
  },

  getUserByToken: async function (token) {
      return await User.findOne({ emailConfirmationToken: token });
  },

  checkUserAndTokenExpiration: async function (user, exits) {
    if (!user || user.emailConfirmationTokenExpiration <= Date.now() || user.emailConfirmedAt != 0){
      return exits.invalidOrExpiredToken({ page_name: 'Invalid, used or expired token' });
    }
  },

  confirmUser: async function (user) {
    await User.updateOne({ id: user.id }).set({
      emailConfirmedAt: Date.now(),
      emailConfirmationToken: '',
      emailConfirmationTokenExpiration: 0
    });
  },
};
