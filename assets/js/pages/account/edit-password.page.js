parasails.registerPage('edit-password', {
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

  methods: {
    submittedForm: async function() {
      this.syncing = true;
      window.location = '/';
    },
  }
});
