module.exports = {
  friendlyName: 'View confirmed email',
  description: 'Display "Confirmed email" page.',

  exits: {
    success: {
      viewTemplatePath: 'pages/entrance/confirmed-email'
    }
  },

  fn: async function () {
    return{
      page_name: 'Confirmed email'
    };
  }
};
