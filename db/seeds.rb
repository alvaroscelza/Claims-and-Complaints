# Seeds for any environment

administrator_role = Role.create!({ name: 'administrator' })
common_user_role = Role.create!({ name: 'user' })

User.create!({ email: 'alvaroscelza@gmail.com',
               password: '123456',
               role: administrator_role,
               confirmed_at: '2019-07-08 00:00:00.000' })

if Rails.env.production?
end

if Rails.env.development?
  User.create!({ email: 'user@gmail.com',
                 password: '123456',
                 role: common_user_role,
                 confirmed_at: '2019-07-08 00:00:00.000'})
end