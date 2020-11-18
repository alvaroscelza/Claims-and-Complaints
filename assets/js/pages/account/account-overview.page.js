parasails.registerPage('account-overview', {
  data: {
    syncingOpenCheckout: false,
    formData: {},
    formRules: {},
    formErrors: {},
    cloudError: '',
    syncing: '',
    modal: '',
  },

  methods: {
    closeModal: async function() {
      this.modal = '';
      await this._resetForms();
    },

    _resetForms: async function() {
      this.cloudError = '';
      this.formData = {};
      this.formRules = {};
      this.formErrors = {};
      await this.forceRender();
    },
  }
});
