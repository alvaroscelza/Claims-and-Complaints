class CreateCompanies < ActiveRecord::Migration[5.1]
  def change
    create_table :companies do |t|
      t.string :name
      t.integer :reputation
      t.string :image
      t.references :business, foreign_key: true
      t.string :description

      t.timestamps
    end
  end
end
