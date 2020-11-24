module.exports = {
  inputs: {
    user: { type: 'json', required: true, },
    session: { type: 'json', required: true, }
  },

  fn: async function ({ user, session }) { session.userId = user.id; }
};
