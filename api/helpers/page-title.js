module.exports = {
  friendlyName: 'Page title',
  description: 'Infers page title by concatenating app name with current page name.',
  sync: true,

  inputs: {
    page_name: {
      type: 'string'
    }
  },

  fn: function ({ page_name }) {
    base_title = sails.config.custom.appName
    return Boolean(page_name) ? `${page_name} | ${base_title}` : base_title
  }
};
