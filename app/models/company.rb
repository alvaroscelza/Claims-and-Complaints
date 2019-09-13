class Company < ApplicationRecord
  validates :name,
            presence: true,
            uniqueness: true
  validates :reputation,
            presence: true
  belongs_to :business
  has_many :judgements
  mount_uploader :image, ImageUploader
end
