module.exports = {
  sync: true,
  inputs: { page_name: { type: 'string' } },

  fn: function ({ page_name }) {
    base_title = sails.config.custom.appName
    return Boolean(page_name) ? `${page_name} | ${base_title}` : base_title
  }
};
