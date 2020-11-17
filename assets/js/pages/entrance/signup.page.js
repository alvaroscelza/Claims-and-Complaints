parasails.registerPage('signup', {
  data: {
    formData: {},
    formErrors: {},
    formRules: {
      fullName: {required: true},
      email: {required: true, isEmail: true},
      password: {required: true},
      confirmPassword: {required: true, sameAs: 'password'},
      agreed: {required: true},
    },
    syncing: false,
    cloudError: '',
  },
  
  methods: {
    submittedForm: async function() {},
  }
});
