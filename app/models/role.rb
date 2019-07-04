class Role < ApplicationRecord
  validates :name,
            presence: true,
            uniqueness: true
  validates :needed_reputation,
            presence: true
end
