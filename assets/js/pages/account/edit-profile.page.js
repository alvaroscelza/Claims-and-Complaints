parasails.registerPage('edit-profile', {
  data: {
    syncing: false,
    formData: {},
    formErrors: {},
    formRules: {
      fullName: {required: true},
      email: {required: true, isEmail: true},
    },
    cloudError: '',
  },

  beforeMount: function() {
    this.formData.fullName = this.me.fullName;
    this.formData.email = this.me.email;
  },

  methods: {
    submittedForm: async function() {
      this.syncing = true;
      window.location = '/account';
    },
  }
});
