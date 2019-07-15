class Company < ApplicationRecord
  validates :name,
            presence: true,
            uniqueness: true
  validates :reputation,
            presence: true
  belongs_to :business
end
