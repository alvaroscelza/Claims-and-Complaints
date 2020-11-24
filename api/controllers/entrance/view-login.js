module.exports = {
  exits: {
    success: {
      viewTemplatePath: 'pages/entrance/login',
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
      page_name: 'Login'
    };
  }
};
