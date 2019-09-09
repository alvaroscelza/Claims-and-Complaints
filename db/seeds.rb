# frozen_string_literal: true

# Seeds for any environment
User.create!(email: 'alvaroscelza@gmail.com',
             password: '123456',
             is_admin: true,
             confirmed_at: '2019-07-08 00:00:00.000')

if Rails.env.production?
end

if Rails.env.development?
  User.create!(email: 'user@gmail.com',
               password: '123456',
               is_admin: false,
               confirmed_at: '2019-07-08 00:00:00.000')
  Business.create!(id: 1,
                   name: 'Restaurante')
  Company.create!(name: "McDonald's",
                  reputation: 0,
                  business_id: 1)
end
