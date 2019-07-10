# Seeds for any environment
User.create!({ email: 'alvaroscelza@gmail.com',
               password: '123456',
               is_admin: true,
               confirmed_at: '2019-07-08 00:00:00.000' })

if Rails.env.production?
end

if Rails.env.development?
  User.create!({ email: 'user@gmail.com',
                 password: '123456',
                 is_admin: false,
                 confirmed_at: '2019-07-08 00:00:00.000'})
end