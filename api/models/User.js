module.exports = {
  attributes: {
    profilePicture: { type: 'string', },
    isAdministrator: { type: 'boolean', defaultsTo: false, },
    email: {
      type: 'string',
      required: true,
      unique: true,
      isEmail: true,
      maxLength: 200,
      example: 'mary.sue@example.com'
    },
    emailConfirmationToken: { type: 'string', },
    emailConfirmationTokenExpiration: { type: 'number', example: 1502844074211 },
    emailConfirmedAt: { type: 'number', example: 1502844074211, defaultsTo: false, },
    password: {
      type: 'string',
      required: true,
      description: 'Securely hashed representation of the user\'s login password.',
      protect: true,
      example: '2$28a8eabna301089103-13948134nad'
    },
    passwordResetToken: { type: 'string', },
    passwordResetTokenExpiresAt: { type: 'number', example: 1502844074211 },
    fullName: {
      type: 'string',
      required: true,
      description: 'Full representation of the user\'s name.',
      maxLength: 120,
      example: 'Mary Sue van der McHenst'
    },
    lastSeenAt: {
      type: 'number',
      description: 'A JS timestamp (epoch ms) representing the moment at which this user most recently interacted with the backend while logged in (or 0 if they have not interacted with the backend at all yet).',
      example: 1502844074211
    },

    // Stripe data (TODO: check if necessary):

    stripeCustomerId: {
      type: 'string',
      protect: true,
      description: 'The id of the customer entry in Stripe associated with this user (or empty string if this user is not linked to a Stripe customer -- e.g. if billing features are not enabled).',
      extendedDescription:
      `Just because this value is set doesn't necessarily mean that this user has a billing card.
      It just means they have a customer entry in Stripe, which might or might not have a billing card.`
    },

    hasBillingCard: {
      type: 'boolean',
      description: 'Whether this user has a default billing card hooked up as their payment method.',
      extendedDescription:
      `More specifically, this indcates whether this user record's linked customer entry in Stripe has
      a default payment source (i.e. credit card).  Note that a user have a \`stripeCustomerId\`
      without necessarily having a billing card.`
    },

    billingCardBrand: {
      type: 'string',
      example: 'Visa',
      description: 'The brand of this user\'s default billing card (or empty string if no billing card is set up).',
      extendedDescription: 'To ensure PCI compliance, this data comes from Stripe, where it reflects the user\'s default payment source.'
    },

    billingCardLast4: {
      type: 'string',
      example: '4242',
      description: 'The last four digits of the card number for this user\'s default billing card (or empty string if no billing card is set up).',
      extendedDescription: 'To ensure PCI compliance, this data comes from Stripe, where it reflects the user\'s default payment source.'
    },

    billingCardExpMonth: {
      type: 'string',
      example: '08',
      description: 'The two-digit expiration month from this user\'s default billing card, formatted as MM (or empty string if no billing card is set up).',
      extendedDescription: 'To ensure PCI compliance, this data comes from Stripe, where it reflects the user\'s default payment source.'
    },

    billingCardExpYear: {
      type: 'string',
      example: '2023',
      description: 'The four-digit expiration year from this user\'s default billing card, formatted as YYYY (or empty string if no credit card is set up).',
      extendedDescription: 'To ensure PCI compliance, this data comes from Stripe, where it reflects the user\'s default payment source.'
    },
  },
};
