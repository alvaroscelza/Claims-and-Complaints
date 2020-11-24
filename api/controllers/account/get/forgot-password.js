module.exports = {
  exits: {
    success: { viewTemplatePath: 'pages/entrance/forgot-password', },
    redirect: { responseType: 'redirect', }
  },

  fn: async function () {
    if (this.req.me) throw {redirect: '/'};
    return { page_name: 'Forgot password' };
  }
};
