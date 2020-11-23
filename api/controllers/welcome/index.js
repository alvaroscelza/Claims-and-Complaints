module.exports = {
  exits: {
    success: { viewTemplatePath: 'welcome/index' },
  },

  fn: async function (inputs, exits) {
    return exits.success({ page_name: 'Welcome' });
  }
};
