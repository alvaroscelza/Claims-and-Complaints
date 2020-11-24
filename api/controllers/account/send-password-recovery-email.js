module.exports = {
  inputs: { email: { type: 'string', required: true } },

  exits: { success: {}, },

  fn: async function ({email}) {
    var userRecord = await User.findOne({ email });
    if (!userRecord) { return; }

    // Come up with a pseudorandom, probabilistically-unique token for use
    // in our password recovery email.
    var token = await sails.helpers.strings.random('url-friendly');

    // Store the token on the user record
    // (This allows us to look up the user when the link from the email is clicked.)
    await User.updateOne({ id: userRecord.id })
    .set({
      passwordResetToken: token,
      passwordResetTokenExpiresAt: Date.now() + sails.config.custom.passwordResetTokenTTL,
    });

    // Send recovery email
    await sails.helpers.sendTemplateEmail.with({
      to: email,
      subject: 'Password reset instructions',
      template: 'email-reset-password',
      templateData: {
        fullName: userRecord.fullName,
        token: token
      }
    });
  }
};
