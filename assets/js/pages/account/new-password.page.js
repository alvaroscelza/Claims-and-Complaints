parasails.registerPage('new-password', {
  data: {
    syncing: false,
    formData: {},
    formErrors: {},

    formRules: {
      password: {required: true},
      confirmPassword: {required: true, sameAs: 'password'},
    },
    cloudError: '',
  },

  mounted: async function() {
    this.formData.token = this.token;
  },

  methods: {
    submittedForm: async function() {
      this.syncing = true;
      window.location = '/';
    },
  }
});
