module.exports = {
  exits: {
    success: { viewTemplatePath: 'pages/welcome/index' },
  },

  fn: async function (inputs, exits) {
    return exits.success({ page_name: 'Welcome' });
  }
};
