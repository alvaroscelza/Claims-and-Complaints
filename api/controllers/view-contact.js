module.exports = {
  friendlyName: 'View contact',
  description: 'Display "Contact" page.',

  exits: {
    success: {
      viewTemplatePath: 'pages/contact'
    }
  },

  fn: async function () {
    return {
      page_name: 'Contact'
    };
  }
};
