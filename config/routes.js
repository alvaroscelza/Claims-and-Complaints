module.exports.routes = {
  'GET    /':                             { action:  'welcome/index' },

  'GET    /forgot-password':              { action: 'account/get/forgot-password' },
  'GET    /login':                        { action: 'account/get/login' },
  'GET    /new-password':                 { action: 'account/get/new-password' },
  'GET    /profile':                      { action: 'account/get/profile' },
  'GET    /signup':                       { action: 'account/get/signup' },
  'GET    /confirm_email':                { action: 'account/confirm-email' },
  'POST   /login':                        { action: 'account/login' },
  'POST   /logout':                       { action: 'account/logout' },
  'POST   /send-password-recovery-email': { action: 'account/send-password-recovery-email' },
  'POST   /signup':                       { action: 'account/signup' },
  'POST   /update-password-and-login':    { action: 'account/update-password-and-login' },
  'PATCH  /update-profile':               { action: 'account/update-profile' },
  
  'GET    /privacy':                      { view:   'pages/legal/privacy',  locals: { page_name: 'Privacy' } },
  'GET    /terms':                        { view:   'pages/legal/terms',    locals: { page_name: 'Terms' } },

  'GET    /contact':                      { action: 'contact/view-contact' },
  'POST   /deliver-contact':              { action: 'contact/deliver' },
};
