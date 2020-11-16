module.exports = {
  friendlyName: 'Update profile',
  description: 'Update the profile for the logged-in user.',

  inputs: {
    fullName: {
      type: 'string'
    },
    email: {
      type: 'string'
    },
  },

  exits: {
    emailAlreadyInUse: {
      statusCode: 409,
      description: 'The provided email address is already in use.',
    },
  },

  fn: async function ({fullName, email}) {
    var newEmail = email;
    if (newEmail !== undefined) {
      newEmail = newEmail.toLowerCase();
    }

    // Determine if this request wants to change the current user's email address,
    // revert her pending email address change, modify her pending email address
    // change, or if the email address won't be affected at all.
    var desiredEmailEffect;// ('change-immediately', 'begin-change', 'cancel-pending-change', 'modify-pending-change', or '')
    if (
      newEmail === undefined ||
      (this.req.me.emailStatus !== 'change-requested' && newEmail === this.req.me.email) ||
      (this.req.me.emailStatus === 'change-requested' && newEmail === this.req.me.emailChangeCandidate)
    ) {
      desiredEmailEffect = '';
    } else if (this.req.me.emailStatus === 'change-requested' && newEmail === this.req.me.email) {
      desiredEmailEffect = 'cancel-pending-change';
    } else if (this.req.me.emailStatus === 'change-requested' && newEmail !== this.req.me.email) {
      desiredEmailEffect = 'modify-pending-change';
    } else if (!sails.config.custom.verifyEmailAddresses || this.req.me.emailStatus === 'unconfirmed') {
      desiredEmailEffect = 'change-immediately';
    } else {
      desiredEmailEffect = 'begin-change';
    }

    // If the email address is changing, make sure it is not already being used.
    if (_.contains(['begin-change', 'change-immediately', 'modify-pending-change'], desiredEmailEffect)) {
      let conflictingUser = await User.findOne({
        or: [
          { email: newEmail },
          { emailChangeCandidate: newEmail }
        ]
      });
      if (conflictingUser) {
        throw 'emailAlreadyInUse';
      }
    }

    // Start building the values to set in the db.
    // (We always set the fullName if provided.)
    var valuesToSet = {
      fullName,
    };

    switch (desiredEmailEffect) {

      // Change now
      case 'change-immediately':
        _.extend(valuesToSet, {
          email: newEmail,
          emailChangeCandidate: '',
          emailConfirmationToken: '',
          emailConfirmationTokenExpiration: 0,
          emailStatus: this.req.me.emailStatus === 'unconfirmed' ? 'unconfirmed' : 'confirmed'
        });
        break;

      // Begin new email change, or modify a pending email change
      case 'begin-change':
      case 'modify-pending-change':
        _.extend(valuesToSet, {
          emailChangeCandidate: newEmail,
          emailConfirmationToken: await sails.helpers.strings.random('url-friendly'),
          emailConfirmationTokenExpiration: Date.now() + sails.config.custom.emailProofTokenTTL,
          emailStatus: 'change-requested'
        });
        break;

      // Cancel pending email change
      case 'cancel-pending-change':
        _.extend(valuesToSet, {
          emailChangeCandidate: '',
          emailConfirmationToken: '',
          emailConfirmationTokenExpiration: 0,
          emailStatus: 'confirmed'
        });
        break;

      // Otherwise, do nothing re: email
    }

    // Save to the db
    await User.updateOne({id: this.req.me.id })
    .set(valuesToSet);

    // If an email address change was requested, and re-confirmation is required,
    // send the "confirm account" email.
    if (desiredEmailEffect === 'begin-change' || desiredEmailEffect === 'modify-pending-change') {
      await sails.helpers.sendTemplateEmail.with({
        to: newEmail,
        subject: 'Your account has been updated',
        template: 'email-verify-new-email',
        templateData: {
          fullName: fullName||this.req.me.fullName,
          token: valuesToSet.emailConfirmationToken
        }
      });
    }
  }
};
