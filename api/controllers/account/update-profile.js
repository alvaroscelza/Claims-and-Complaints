module.exports = {
  friendlyName: 'Update profile',
  description: 'Update the profile for the logged-in user.',

  inputs: {
    fullName: {
      type: 'string'
    },
    email: {
      type: 'string'
    },
  },

  fn: async function ({fullName}) {
    await User.updateOne({id: this.req.me.id }).set({fullName});
  }
};
