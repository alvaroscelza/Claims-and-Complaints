module.exports = {
  exits: {
    success: {
      statusCode: 200,
      description: 'Requesting user is a guest, so show the public landing page.',
      viewTemplatePath: 'welcome/index'
    },
  },

  fn: async function () {
    return {
      page_name: 'Welcome'
    };
  }
};
