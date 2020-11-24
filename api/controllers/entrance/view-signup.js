module.exports = {
  exits: {
    success: {
      viewTemplatePath: 'pages/entrance/signup',
    },
    redirect: {
      description: 'The requesting user is already logged in.',
      responseType: 'redirect'
    }
  },

  fn: async function () {
    if (this.req.me) {
      throw {redirect: '/'};
    }
    return {
      page_name: 'Sign up'
    };
  }
};
