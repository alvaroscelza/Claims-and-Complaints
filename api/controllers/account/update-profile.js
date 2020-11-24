module.exports = {
  inputs: { 
    fullName: { type: 'string' },
    password: { type: 'string' }
  },

  fn: async function ({fullName, password}) {
    var hashed = await sails.helpers.passwords.hashPassword(password);
    await User.updateOne({id: this.req.me.id }).set({fullName, hashed});
  }
};
