class Judgement < ApplicationRecord
  validates :opinion,
            presence: true
  validates :user,
            presence: true
  validates :company,
            presence: true
  belongs_to :company
  belongs_to :user
end
