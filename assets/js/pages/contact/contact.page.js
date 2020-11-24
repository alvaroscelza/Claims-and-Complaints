parasails.registerPage('contact', {
  data: {
    syncing: false,
    formData: {},
    formErrors: {},
    formRules: {
      email: {isEmail: true, required: true},
      fullName: {required: true},
      topic: {required: true},
      message: {required: true},
    },
    cloudError: '',
    cloudSuccess: false,
  },

  methods: {
    submittedForm: async function() {
      this.cloudSuccess = true;
    },
  }
});
