class Business < ApplicationRecord
  validates :name,
            presence: true,
            uniqueness: true
end
