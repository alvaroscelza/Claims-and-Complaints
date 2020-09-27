# frozen_string_literal: true

# Seeds for any environment
User.create!(id: 1,
             email: 'alvaroscelza@gmail.com',
             password: '123456',
             is_admin: true,
             confirmed_at: '2019-07-08 00:00:00.000')

if Rails.env.development?
  User.create!(id: 2,
               email: 'user@gmail.com',
               password: '123456',
               is_admin: false,
               confirmed_at: '2019-07-08 00:00:00.000')
  Business.create!(id: 1,
                   name: 'Restaurante')
  Company.create!(id: 1,
                  name: "McDonald's",
                  reputation: 0,
                  business_id: 1)
  Judgement.create!(opinion: 'Opinion de prueba',
                    vote: true,
                    user_id: 2,
                    company_id: 1)
end
