/**
 * cloud.setup.js
 *
 * Configuration for this Sails app's generated browser SDK ("Cloud").
 *
 * Above all, the purpose of this file is to provide endpoint definitions,
 * each of which corresponds with one particular route+action on the server.
 *
 * > This file was automatically generated.
 * > (To regenerate, run `sails run rebuild-cloud-sdk`)
 */

Cloud.setup({

  /* eslint-disable */
  methods: {"index":{"verb":"GET","url":"/","args":[]},"signup":{"verb":"POST","url":"/signup","args":["email","password","fullName"]},"confirmEmail":{"verb":"GET","url":"/email/confirm","args":["token"]},"login":{"verb":"POST","url":"/login","args":["email","password","rememberMe"]},"sendPasswordRecoveryEmail":{"verb":"POST","url":"/send-password-recovery-email","args":["email"]},"updatePasswordAndLogin":{"verb":"POST","url":"/update-password-and-login","args":["password","token"]},"logout":{"verb":"POST","url":"/account/logout","args":[]},"updatePassword":{"verb":"PUT","url":"/account/update-password","args":["password"]},"updateProfile":{"verb":"PUT","url":"/account/update-profile","args":["fullName","email"]},"deliverContactFormMessage":{"verb":"POST","url":"/deliver-contact-form-message","args":["email","topic","fullName","message"]}}
  /* eslint-enable */

});
