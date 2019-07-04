class User < ApplicationRecord
  validates :name,
            presence: true,
            uniqueness: true
  validates :reputation,
            presence: true
  validates :password,
            presence: true
  validates :email,
            presence: true,
            format: { with: URI::MailTo::EMAIL_REGEXP },
            uniqueness: true
  validates :image
  validates :role,
            presence: true
  validates :permits
end
