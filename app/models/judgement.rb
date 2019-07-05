class Judgement < ApplicationRecord
  validates :opinion,
            presence: true
  validates :vote
  validates :user,
            presence: true
  validates :company,
            presence: true
end
