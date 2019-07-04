class Company < ApplicationRecord
  validates :name,
            presence: true,
            uniqueness: true
  validates :reputation,
            presence: true
  validates :image
  validates :business
  validates :description
end
