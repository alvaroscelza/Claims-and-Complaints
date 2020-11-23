module.exports.routes = {
  'GET    /':                { action: 'welcome/index' },

  'GET    /signup':          { action: 'entrance/view-signup' },
  'POST   /signup':          { action: 'entrance/signup' },
  'GET    /email/confirm':   { action: 'entrance/confirm-email' },


  'GET /login':              { action: 'entrance/view-login' },
  'GET /password/forgot':    { action: 'entrance/view-forgot-password' },
  'GET /password/new':       { action: 'entrance/view-new-password' },
  'PUT   /login':                        { action: 'entrance/login' },
  'POST  /send-password-recovery-email': { action: 'entrance/send-password-recovery-email' },
  'POST  /update-password-and-login':    { action: 'entrance/update-password-and-login' },

  'GET /account':            { action: 'account/view-account-overview' },
  'GET /account/password':   { action: 'account/view-edit-password' },
  'GET /account/profile':    { action: 'account/view-edit-profile' },
  
  'GET /legal/terms':        { action:   'legal/view-terms' },
  'GET /legal/privacy':      { action:   'legal/view-privacy' },
  'GET /contact':            { action:   'view-contact' },
  
  //  ╔═╗╔═╗╦  ╔═╗╔╗╔╔╦╗╔═╗╔═╗╦╔╗╔╔╦╗╔═╗
  //  ╠═╣╠═╝║  ║╣ ║║║ ║║╠═╝║ ║║║║║ ║ ╚═╗
  //  ╩ ╩╩  ╩  ╚═╝╝╚╝═╩╝╩  ╚═╝╩╝╚╝ ╩ ╚═╝
  // Note that, in this app, these API endpoints may be accessed using the `Cloud.*()` methods
  // from the Parasails library, or by using those method names as the `action` in <ajax-form>.
  'POST  /account/logout':                           { action: 'account/logout' },
  'PUT   /account/update-password':            { action: 'account/update-password' },
  'PUT   /account/update-profile':             { action: 'account/update-profile' },
  'POST  /deliver-contact-form-message':          { action: 'deliver-contact-form-message' },
};
