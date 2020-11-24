module.exports = {
  inputs: { page_name: { type: 'string' } },

  fn: async function ({ page_name }) {
    base_title = sails.config.custom.appName
    return Boolean(page_name) ? `${page_name} | ${base_title}` : base_title
  }
};
