class Permit < ApplicationRecord
  validates :name,
            presence: true,
            uniqueness: true
end
