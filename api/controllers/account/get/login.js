module.exports = {
  fn: async function () {
    if (this.req.me) return this.res.redirect('/');
    return this.res.view('pages/account/login', { page_name: 'Login' });
  }
};
