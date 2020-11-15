module.exports = {
  friendlyName: 'View privacy',
  description: 'Display "Privacy policy" page.',

  exits: {
    success: {
      viewTemplatePath: 'pages/legal/privacy'
    }
  },

  fn: async function () {
    return{
      page_name: 'Privacy'
    };
  }
};
