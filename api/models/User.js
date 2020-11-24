module.exports = {
  attributes: {
    profilePicture: { type: 'string', },
    isAdministrator: { type: 'boolean', defaultsTo: false, },
    email: { type: 'string', required: true, unique: true, isEmail: true, maxLength: 200, },
    emailConfirmationToken: { type: 'string', },
    emailConfirmationTokenExpiration: { type: 'number' },
    emailConfirmedAt: { type: 'number', defaultsTo: 0, },
    password: { type: 'string', required: true, protect: true, },
    passwordResetToken: { type: 'string', },
    passwordResetTokenExpiresAt: { type: 'number' },
    fullName: { type: 'string', required: true, maxLength: 120, },
    lastSeenAt: { type: 'number', },
  },
};
