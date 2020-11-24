parasails.registerPage('forgot-password', {
  data: {
    syncing: false,
    formData: {},
    formErrors: {},
    formRules: { email: {required: true, isEmail: true}, },
    cloudError: '',
    cloudSuccess: false,
  },
  methods: {
    submittedForm: async function() {
      this.cloudSuccess = true;
    },
  }
});
