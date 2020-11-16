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
    emailConfirmedAt: { type: 'number', example: 1502844074211, defaultsTo: 0, },
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
  },
};
