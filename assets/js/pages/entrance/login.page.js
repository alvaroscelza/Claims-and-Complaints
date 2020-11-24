parasails.registerPage('login', {
  data: {
    syncing: false,
    formData: { rememberMe: true },
    formErrors: {},
    formRules: {
      email: { required: true, isEmail: true },
      password: { required: true },
    },
    cloudError: '',
  },

  methods: {
    submittedForm: async function() {
      this.syncing = true;
      window.location = '/';
    },
  }
});
