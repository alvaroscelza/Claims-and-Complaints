module.exports = {
  inputs: {
    token: {
      description: 'The confirmation token from the email.',
      example: '4-32fad81jdaf$329'
    }
  },

  exits: {
    success: {
      description: 'Email address confirmed and requesting user logged in.'
    },
    redirect: {
      description: 'Email address confirmed and requesting user logged in.  Since this looks like a browser, redirecting...',
      responseType: 'redirect'
    },
    invalidOrExpiredToken: {
      responseType: 'expired',
      description: 'The provided token is expired, invalid, or already used up.',
    },
    emailAddressNoLongerAvailable: {
      statusCode: 409,
      viewTemplatePath: '500',
      description: 'The email address is no longer available.',
      extendedDescription: 'This is an edge case that is not always anticipated by websites and APIs.  Since it is pretty rare, the 500 server error page is used as a simple catch-all.  If this becomes important in the future, this could easily be expanded into a custom error page or resolution flow.  But for context: this behavior of showing the 500 server error page mimics how popular apps like Slack behave under the same circumstances.',
    }
  },

  fn: async function ({token}) {
    // If no token was provided, this is automatically invalid.
    if (!token) {
      throw 'invalidOrExpiredToken';
    }

    // Get the user with the matching email token.
    var user = await User.findOne({ emailConfirmationToken: token });

    // If no such user exists, or their token is expired, bail.
    if (!user || user.emailConfirmationTokenExpiration <= Date.now()) {
      throw 'invalidOrExpiredToken';
    }

    if (user.emailConfirmedAt === 0) {
      await User.updateOne({ id: user.id }).set({
        emailConfirmedAt: Date.now(),
        emailConfirmationToken: '',
        emailConfirmationTokenExpiration: 0
      });
      this.req.session.userId = user.id;

      if (this.req.wantsJSON) {
        return;
      } else {
        throw { redirect: '/email/confirmed' };
      }
    }
  }
};
